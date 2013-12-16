# coding: utf8
###########################################################################
#                        Table Definitions                                #
###########################################################################
GENRES=['Classic Rock', 'Rap', 'Pop', 'Classical', 'Blues', 'Jazz', 'Metal', 'Punk', 'Electronic']
RELATION=['friend', 'request', 'block']
GENDERS=['Male', 'Female']
STATUS=['Like', 'Dislike']

db.define_table('post',
                Field('title', 'string', requires=IS_NOT_EMPTY()),
                Field('attachment', 'upload', requires=[IS_NOT_EMPTY(), IS_UPLOAD_FILENAME(extension='mp3|mp4|wmv|wav|avi|aac')]),
                Field('album_art', 'upload', requires=IS_NULL_OR(IS_IMAGE(extensions=('jpeg', 'png')))),
                Field('description', requires=IS_NOT_EMPTY()),
                Field('genre', 'string', requires=IS_IN_SET(GENRES)),
                Field('artist', 'string', requires=IS_NOT_EMPTY()),
                auth.signature
)

db.define_table('comment_item',
                Field('body', 'text', requires=IS_NOT_EMPTY()),
                Field('item_id', db.post, readable=False, writable=False),
                Field('post', db.post, readable=False, writable=False),
                auth.signature
)

db.define_table('relationship',
                Field('person', db.auth_user),
                Field('status', 'string', requires=IS_IN_SET(RELATION)),
                auth.signature
)

db.define_table('post_like',
                Field('post', db.post, readable=False, writable=False),
                Field('status', 'string', requires=IS_IN_SET(STATUS)),
                auth.signature
)

db.define_table('post_fave',
                Field('post', db.post, readable=False, writable=False),
                auth.signature
)

db.define_table('profile_info',
                 Field('person', db.auth_user, readable=False, writable=False),
                 Field('gender', 'string', requires=IS_NULL_OR(IS_IN_SET(GENDERS))),
                 Field('birthdate', 'date'),
                 Field('user_location', 'string'),
                 Field('genres', 'string'),
                 Field('picture', 'upload', requires=IS_NULL_OR(IS_IMAGE(extensions=('jpeg', 'png'))))
)

db.define_table('user_status',
                Field('person', db.auth_user, readable=False, writable=False),
                Field('created_on', 'datetime', default=request.now),
                Field('body', 'string', requires=IS_NOT_EMPTY())
)

###############################################################################
#                   Populate DEVELOPMENT ONLY!                                #
###############################################################################
#from gluon.contrib.populate import populate
#if not db(db.auth_user).count():
#    populate(db.auth_user,50)
#if not db(db.post).count():
#    populate(db.post,100)
