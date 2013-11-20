# coding: utf8
GENRES=['Classic Rock', 'Rap', 'Pop', 'Classical', 'Blues', 'Jazz', 'Metal', 'Punk', 'Electronic']
RELATION=['friend', 'request', 'block']
GENDERS=['Male', 'Female']

db.define_table('post',
                Field('title', 'string', requires=IS_NOT_EMPTY()),
                Field('attachment', 'upload', requires=[IS_NOT_EMPTY(), IS_UPLOAD_FILENAME(extension='mp3|mp4|wmv|wav|avi|aac')]),
                Field('description', requires=IS_NOT_EMPTY()),
                Field('genre', 'string', requires=IS_IN_SET(GENRES)),
                auth.signature
)

db.define_table('comment_item',
                Field('body', 'text', requires=IS_NOT_EMPTY()),
                Field('item_id', 'integer', readable=False, writable=False),
                Field('item_type', 'text', readable=False, writable=False, requires=IS_IN_SET(['post','profile'])),
                Field('post', db.post, readable=False, writable=False),
                auth.signature
)

db.define_table('relationship',
                Field('person', 'reference auth_user'),
                Field('status', 'string', requires=IS_IN_SET(RELATION)),
                auth.signature
)

db.define_table('post_like',
                Field('post', db.post, readable=False, writable=False),
                 auth.signature
)

def fullname(user_id):
    if user_id is None:
        return "Unknown"
    return "%(first_name)s %(last_name)s" % db.auth_user(user_id)

def commentitem(comment):
    text = comment.body
    name = fullname(comment.created_by)
    date = prettydate(comment.created_on)
    userlink = str(A(name,_href=URL('profile',args=comment.created_by)))
    if db.auth_user(comment.created_by).picture:
        imageref = URL('download', args=db.auth_user(comment.created_by).picture)
    else:
        imageref = URL('static', 'images/user_placeholder.jpg')

    return XML("""
        <li class="media">
            <div class="pull-left">
                <img class="media-object" height="50" width="50" src=\"""" + imageref + """" />
            </div>
            <div class="media-body">
                """ + text + """
                <br />
                """ + userlink + " / " + date + """
            </div>
        </li>
    """)

def musicitem(post):

    name        = fullname(post.created_by)
    postref     = URL('post',args=post.id)
    imageref    = URL('static', 'images/tn_placeholder.png')
    genrelink   = str(A(post.genre, _href=URL('genre', args=post.genre)))
    postlink    = str(A(post.title, _href=postref))
    date        = prettydate(post.created_on)
    userlink    = str(A(name,_href=URL('profile',args=post.created_by)))
    description = post.description
    attachref   = URL('download',args=post.attachment)

    return XML("""
            <li class="media">
                <a class="pull-left" href=\"""" + postref + """">
                    <img class="media-object" src=\"""" + imageref + """">
                </a>
                <div class="media-body">
                    <h4 >""" + genrelink + " / " + postlink + """</h4>
                    <h5>""" + date + " | Posted by " + userlink + """</h5>
                    <p>""" + description + """</p>
                    <audio controls="controls" style="max-width:100%">
                        <source src=\"""" + attachref + """">
                    </audio>
                </div>
            </li>
    """)

def musicItemList(posts):
    x = '<ul class="media-list">'

    for post in posts:
        x += musicitem(post)

    x += '</ul>'

    return XML(x)

def commentItemList(comments):
    x = '<ul class="media-list">'

    for comment in comments:
        x += commentitem(comment)

    x += '</ul>'

    return XML(x)
