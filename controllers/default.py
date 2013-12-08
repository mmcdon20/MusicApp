# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    posts = db(db.post).select(orderby=~db.post.created_on)
    return locals()

def about():
    
    return locals()

def search():
    query = request.vars.query

    if query:
        results = db(db.post.title.contains(query.split())|
                     db.post.description.contains(query.split())|
                     db.post.artist.contains(query.split())|
                     db.post.genre.contains(query.split())).select()
        people = db(db.auth_user.first_name.contains(query.split())|
                    db.auth_user.last_name.contains(query.split())).select()
    else:
        results = None
        people = None

    searchForm.custom.widget.query['_value']= query
    return locals()

# This func is getting ugly, prob want to break it down eventually
def profile():
    ############################################################
    #### Handle request and set the profile userId
    if request.args:
        userId = request.args(0, cast=int)
        if db.auth_user(userId) is None:
            session.flash = "User not found"
            redirect(URL('index'))
    elif auth.user:
        redirect(URL("profile", args=auth.user.id))
    else:
        session.flash = "Must login to view your profile"
        redirect(URL("index"))
    #### END handle request
    ############################################################
    
    # If user has no profile, create one.
    if db(db.profile_info.person==userId).select().first() is None:
        db.profile_info.insert(person=userId)
    if db(db.user_status.person==userId).select().first() is None:
        db.user_status.insert(person=userId, body="Some things are better left unsaid")
    
    user = db.auth_user(userId)
    info = db(db.profile_info.person==userId).select().first()
    uploads = db(db.post.created_by == userId).select()
    status =  db(db.user_status.person==userId).select().first().body
    friendRelations = db(db.relationship.created_by == userId).select()
    friendRelations = friendRelations & db(db.relationship.person == userId).select()

    # Calculated Profile Fields
    age = prettydate(info.birthdate).replace(' years ago', '') # TODO: better!

    jams = db((db.post_like.post==db.post.id)&
              (db.post.created_by==userId)&
              (db.post_like.status=='Like')).count()
    
    cans = db((db.post_like.post==db.post.id)&
              (db.post.created_by==userId)&
              (db.post_like.status=='Dislike')).count()
    
    score = jams - cans

    # Create edit profile form TODO: move to a function  PLEASE DO NOT EDIT BELOW THIS LINE FOR NOW
    if auth.user and auth.user.id == userId:
        # TODO, make double table form for user name edit right here!
        editForm = SQLFORM(db.profile_info,
            record = db(db.profile_info.person==userId).select().first(),
            fields = ['birthdate', 'gender', 'user_location', 'genres', 'picture'],
            submit_button = 'Save Changes'
        )
        editForm.custom.submit['_class'] = 'btn-primary'
        if editForm.process().accepted:
            redirect(URL('profile', args=auth.user.id))

        statusForm = SQLFORM(db.user_status,
                            record = db(db.user_status.person==userId).select().first(),
                            fields = ['body'],
                            submit_button='Update Status')
        statusForm.custom.submit['_class'] = 'btn-primary'
        if statusForm.process().accepted:
            redirect(URL('profile', args=auth.user.id))
            
    # IF this profile is not mine, find if we have a relation
    relationId = None
    if auth.user and userId != auth.user.id:
        rows = db((db.relationship.person==userId) & (db.relationship.created_by==auth.user.id)).select()
        rows = rows & db((db.relationship.person==auth.user.id) & (db.relationship.created_by==userId)).select()
        if len(rows) > 0:
            relationId = rows[0].id

    return locals()

@auth.requires_login()
def friends():
    userId = auth.user.id
    
    friendRelations = db((db.relationship.created_by == userId) | 
                         (db.relationship.person == userId)).select()
    
    friendUploads = db(((db.relationship.person == db.post.created_by)|(db.relationship.created_by == db.post.created_by)) &
                       ((db.relationship.person == userId)|(db.relationship.created_by == userId)) &
                       (db.post.created_by != userId)
                       ).select(db.post.ALL, orderby=~db.post.created_on, distinct=True)
    
    friendComments = db(((db.relationship.person == db.comment_item.created_by)|(db.relationship.created_by == db.comment_item.created_by)) &
                        ((db.relationship.person == userId)|(db.relationship.created_by == userId)) &
                        (db.comment_item.created_by != userId)
                        ).select(db.comment_item.ALL, orderby=~db.comment_item.created_on, distinct=True) #, limitby=(0, 5))
    
    return locals()

def genre():
    genre = request.args(0).replace('_',' ')
    posts = db(db.post.genre==genre).select(orderby=~db.post.created_on)
    return locals()

def post():
    postId = request.args(0, cast=int)
    post = db.post(int(postId))

    if not post:
        session.flash = "Post does not exist"
        redirect(URL('index'))

    db.comment_item.item_id.default = post.id
    form = crud.create(db.comment_item)

    comments = db(db.comment_item.item_id==post.id).select()
    
    editForm = SQLFORM(db.post,
            record = db(db.post.id == postId).select().first(),
            submit_button = 'Save Changes')
    editForm.custom.submit['_class'] = 'btn-primary'
    
    if editForm.process().accepted:
        redirect(URL('post', args=postId))
    
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def friendly():
    
    return locals()

def addFriend():
    db.relationship.insert(person=request.post_vars.person, status=request.post_vars.status)
    return locals()

def removeFriend():
    db(db.relationship.id == request.post_vars.rid).delete()
    return locals()

def changeStatus():
    id = request.post_vars.commentid
    post = db.post(id)
    new_status = request.post_vars.status
    
    record = db((db.post_like.post == id) & (db.post_like.created_by == auth.user.id)).select()

    if not record:
        db.post_like.insert(post=id, status=new_status)
    elif record[0].status == new_status:
        db((db.post_like.post==id) & (db.post_like.created_by==auth.user.id)).delete()
    else:
        db((db.post_like.post==id) & (db.post_like.created_by==auth.user.id)).update(status=new_status)
    
    redirect(URL('index'))
    return locals()
