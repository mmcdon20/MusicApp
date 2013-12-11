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
    posts = recent_posts(0,5)
    return locals()

def about():
    return locals()

def search():
    query   = request.vars.query or ""
    results = search_jams(query)
    people  = search_jammers(query)
    results_count = count_search_jams(query)
    people_count  = count_search_jammers(query)
    search_form.custom.widget.query['_value']= query
    return locals()

# This func is getting ugly, prob want to break it down eventually
def profile():
    ############################################################
    #### Handle request and set the profile userId
    if request.args:
        user_id = request.args(0, cast=int)
        if db.auth_user(user_id) is None:
            session.flash = "User not found"
            redirect(URL('index'))
    elif auth.user:
        redirect(URL("profile", args=auth.user.id))
    else:
        session.flash = "Must login to view your profile"
        redirect(URL("index"))
    #### END handle request
    ############################################################

    user      = user_account(user_id)
    info      = user_info(user_id)
    uploads   = user_uploads(user_id)
    status    = user_status(user_id)
    relations = friend_relations(user_id)
    score     = user_jams(user_id) - user_cans(user_id)
    age       = prettydate(info.birthdate).replace(' years ago', '') # TODO: better!

    # Create edit profile form TODO: move to a function  PLEASE DO NOT EDIT BELOW THIS LINE FOR NOW
    if auth.user and auth.user.id == user_id:
        # TODO, make double table form for user name edit right here!
        edit_form = SQLFORM(db.profile_info,
                            record = db(db.profile_info.person==user_id).select().first(),
                            fields = ['birthdate', 'gender', 'user_location', 'genres', 'picture'],
                            submit_button = 'Save Changes')
        status_form = SQLFORM(db.user_status,
                              record = db(db.user_status.person==user_id).select().first(),
                              fields = ['body'],
                              submit_button='Update Status')
        
        edit_form.custom.submit['_class'] = 'btn-primary'
        status_form.custom.submit['_class'] = 'btn-primary'
        
        if edit_form.process().accepted:
            redirect(URL('profile', args=auth.user.id))
            
        if status_form.process().accepted:
            redirect(URL('profile', args=auth.user.id))
            
    # IF this profile is not mine, find if we have a relation
    relation_id = None
    if auth.user and user_id != auth.user.id:
        rows = db(((db.relationship.person==user_id) & (db.relationship.created_by==auth.user.id))|
                  ((db.relationship.person==auth.user.id) & (db.relationship.created_by==user_id))).select()
        if len(rows) > 0:
            relation_id = rows[0].id

    return locals()

@auth.requires_login()
def friends():
    user_id   = auth.user.id
    relations = friend_relations(user_id)
    uploads   = friend_uploads(user_id)
    comments  = friend_comments(user_id)
    return locals()

def genre():
    genre = request.args(0).replace('_',' ')
    posts = db(db.post.genre==genre).select(orderby=~db.post.created_on)
    return locals()

def post():
    post_id = request.args(0, cast=int)
    post = db.post(post_id)

    if not post:
        session.flash = "Post does not exist"
        redirect(URL('index'))

    db.comment_item.item_id.default = post_id
    form = crud.create(db.comment_item)
    comments = post_comments(post_id)
    
    edit_form = SQLFORM(db.post,
            record = db(db.post.id == post_id).select().first(),
            submit_button = 'Save Changes')
    edit_form.custom.submit['_class'] = 'btn-primary'
    
    if edit_form.process().accepted:
        redirect(URL('post', args=post_id))
    
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
