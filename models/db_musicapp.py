# coding: utf8
GENRES=['Classic Rock', 'Rap', 'Pop', 'Classical', 'Blues', 'Jazz', 'Metal', 'Punk', 'Electronic']
RELATION=['friend', 'request', 'block']

db.define_table('post',
                Field('title', 'string', requires=IS_NOT_EMPTY()),
                Field('attachment', 'upload', requires=[IS_NOT_EMPTY(), IS_UPLOAD_FILENAME(extension='mp3|mp4|wmv|wav|avi|aac')]),
                Field('description', requires=IS_NOT_EMPTY()),
                Field('genre', 'string', requires=IS_IN_SET(GENRES)),
                auth.signature
)

db.define_table('post_comment',
                Field('body', 'text', requires=IS_NOT_EMPTY()),
                Field('post', db.post, readable=False, writable=False),
                auth.signature
)

db.define_table('relationship',
          Field('person', 'reference auth_user'),
          Field('status', 'string', requires=IS_IN_SET(RELATION)),
          auth.signature
)

def fullname(user_id):
    if user_id is None:
        return "Unknown"
    return "%(first_name)s %(last_name)s" % db.auth_user(user_id)

def musicitem(post):
    if post is None:
        return None
    
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
    <div class="row">
        <div class="span12 post-container">
            <ul class="media-list">
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
            </ul>
        </div>
    </div>
    """)
