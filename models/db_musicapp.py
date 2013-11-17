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
          Field('person'),
          Field('status', 'string', requires=IS_IN_SET(RELATION)),
          auth.signature
)

def fullname(user_id):
    if user_id is None:
        return "Unknown"
    return "%(first_name)s %(last_name)s" % db.auth_user(user_id)
