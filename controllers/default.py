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

def search():
    query = request.args(0)  
    form = SQLFORM.factory(
                   Field('query','string', default = query),
                   submit_button='Search')

    if query:
        results = db(db.post.title.contains(query)|
                     db.post.description.contains(query)|
                     db.post.genre.contains(query)).select()
    else:
        results = None

    if form.process().accepted:
        redirect(URL("search", args=form.vars.query)) 

    return locals()

def profile():
    if request.args:
        user = request.args(0, cast=int)
    else:
        redirect(URL("profile", args=auth.user.id))

    uploads = db(db.post.created_by == user).select()
    friends = db(db.relationship.created_by == user).select()
    
    #fake fields
    totalLikes = 1337
    totalUploads = 69
    userStatus = "Today is a good day for music in the nude!"
    age = 25
    gender = "Male"
    location = "Chicago, IL"
    genres = "Rap, Electronic, Classic Rock, Blues"
    joined = "3/25/2013"
    #db.profile_comment.post.default = user
    #form = crud.create(db.profile_comment)
    #comments = db(db.profile_comment.post==user).select(db.profile_comment.ALL)

    return locals()

def genre():
    genre = request.args(0)
    posts = db(db.post.genre==genre).select(orderby=~db.post.created_on)

    if not posts:
        session.flash = "Genre '" + genre + "' does not exist"
        redirect(URL('index'))

    return locals()

@auth.requires_login()
def upload():
    form = SQLFORM(db.post).process()
    return locals()

def post():
    postId = request.args(0, cast=int)
    post = db.post(int(postId))

    if not post:
        session.flash = "Post does not exist"
        redirect(URL('index'))

    db.post_comment.post.default = post.id
    form = crud.create(db.post_comment)

    comments = db(db.post_comment.post==post.id).select(db.post_comment.ALL)
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
