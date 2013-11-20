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

def register():

    form = auth.register()

    return locals()

def search():
    query = request.args(0)

    if query:
        query = query.replace('_',' ')
        results = db(db.post.title.contains(query)|
                     db.post.description.contains(query)|
                     db.post.genre.contains(query)).select()
    else:
        results = None

    form = SQLFORM.factory(
                   Field('query','string', default = query),
                   submit_button='Search')
        
    if form.process().accepted:
        redirect(URL("search", args=form.vars.query))

    return locals()

def profile():
    userId = 0
    if request.args:
        userId = request.args(0, cast=int)
        if db.auth_user(userId) is None:
            session.flash = "User not found!"
            redirect(URL('index'))
    else:
        redirect(URL("profile", args=auth.user.id))

    user = db.auth_user(userId)
    uploads = db(db.post.created_by == userId).select()
    friends = db(db.relationship.created_by == userId).select()

    # Calculated Profile Fields
    age = prettydate(user.birthdate).replace(' years ago', '') # TODO: better!

    #fake fields
    totalLikes = 1337

    #db.profile_comment.post.default = user
    #form = crud.create(db.profile_comment)
    #comments = db(db.profile_comment.post==user).select(db.profile_comment.ALL)

    return locals()

def genre():
    genre = request.args(0).replace('_',' ')
    posts = db(db.post.genre==genre).select(orderby=~db.post.created_on)

    if not posts:
        session.flash = "Genre '" + genre + "' does not exist"
        redirect(URL('index'))

    return locals()

@auth.requires_login()
def upload():
    form = SQLFORM(db.post)
    
    if form.process().accepted:
        redirect(URL("post", args=form.vars.id)) 
    
    return locals()

def post():
    postId = request.args(0, cast=int)
    post = db.post(int(postId))

    if not post:
        session.flash = "Post does not exist"
        redirect(URL('index'))

    db.comment_item.item_id.default = post.id
    db.comment_item.item_type.default = 'post'
    form = crud.create(db.comment_item)

    comments = db((db.comment_item.item_id==post.id) & (db.comment_item.item_type=='post')).select()
    return locals()

@auth.requires_login()
def edit_post():
    postId = request.args(0, cast=int)
    post = db.post(int(postId)) or redirect(URL('index'))
    #post = db(db.post.id == postId).select() or redirect(URL('index'))

    if post.created_by != auth.user.id:
        redirect(URL('index'))

    form = SQLFORM(db.post, post).process()
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
