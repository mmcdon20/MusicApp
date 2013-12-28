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

def search():
    query   = request.vars.query or ""
    results = search_jams(query)
    people  = search_jammers(query)
    results_count = count_search_jams(query)
    people_count  = count_search_jammers(query)
    # Not sure is hacky
    showPeopleTab = False
    if results_count == 0 and people_count != 0:
        showPeopleTab = True
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
    followers = user_followers(user_id)
    following = user_following(user_id)
    relations = friend_relations(user_id)
    score     = user_jams(user_id) - user_cans(user_id)
    age       = prettydate(info.birthdate).replace(' years ago', '')

    if auth.user and auth.user.id == user_id:
        users_favorites   = user_favorites(user_id)
        friends_uploads   = friend_uploads(user_id)
        friends_comments  = friend_comments(user_id)
        friends_statuses  = friend_statuses(user_id)

        edit_form = SQLFORM(db.profile_info,
                            record = db(db.profile_info.created_by==user_id).select().first(),
                            fields = ['birthdate', 'gender', 'user_location', 'genres', 'picture'],
                            submit_button = 'Save Changes')
        status_form = SQLFORM(db.user_status,
                              fields = ['body'],
                              submit_button='Update Status')
        status_form.custom.widget.body['_value']= status
        edit_form.custom.submit['_class'] = 'btn-primary'
        status_form.custom.submit['_class'] = 'btn-primary'
        
        if edit_form.process().accepted:
            redirect(URL('profile', args=auth.user.id))
            
        if status_form.process().accepted:
            redirect(URL('profile', args=auth.user.id))
            
    if auth.user and user_id != auth.user.id:
        relation = user_relation(user_id)
    else:
        relation = None
        
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
