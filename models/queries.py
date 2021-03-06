# coding: utf8

def count_users():
    return db(db.auth_user).count()

def count_posts():
    return db(db.post).count()

def count_comments():
    return db(db.comment_item).count()

def count_statuses():
    return db(db.user_status).count()

def count_search_jams(query):
    return db(query_jams(query)).count()

def count_search_jammers(query):
    return db(query_jammers(query)).count()

def search_jams(query):
    return db(query_jams(query)).select()

def search_jammers(query):
    return db(query_jammers(query)).select()

def query_jams(query):
    return (db.post.title.contains(query) |
            db.post.description.contains(query) |
            db.post.artist.contains(query) |
            db.post.genre.contains(query))

def query_jammers(query):
    return (db.auth_user.first_name.contains(query.split()) |
            db.auth_user.last_name.contains(query.split()))

def user_account(user_id):
    return db.auth_user(user_id)

def user_info(user_id):
    return db(db.profile_info.created_by==user_id).select().first()

def user_uploads(user_id):
    return db(db.post.created_by == user_id).select()

def user_status(user_id):
    return db(db.user_status.created_by==user_id).select(orderby=~db.user_status.created_on).first().body

def user_jams(user_id):
    return db((db.post_like.post==db.post.id) &
              (db.post.created_by==user_id) &
              (db.post_like.status=='Like')).count()

def user_cans(user_id):
    return db((db.post_like.post==db.post.id) &
              (db.post.created_by==user_id) &
              (db.post_like.status=='Dislike')).count()

def user_relation(user_id):
    return db((db.relationship.person==user_id)&
              (db.relationship.created_by==auth.user.id)
              ).select().first() or None

def user_following(user_id):
    return db(db.relationship.created_by==user_id).count()

def user_followers(user_id):
    return db(db.relationship.person==user_id).count()

def user_favorites(user_id):
    return db((db.post_fave.created_by == user_id)&
              (db.post_fave.post == db.post.id)).select(db.post.ALL)

def friend_relations(user_id):
    return db(db.relationship.created_by == user_id).select()

def friend_uploads(user_id):
    return db((db.relationship.created_by == user_id)&
              (db.relationship.person == db.post.created_by)
              ).select(db.post.ALL, orderby=~db.post.created_on, distinct=True)

def friend_comments(user_id):
    return db((db.relationship.created_by == user_id)&
              (db.relationship.person == db.comment_item.created_by)
              ).select(db.comment_item.ALL, orderby=~db.comment_item.created_on, distinct=True)

def friend_statuses(user_id):
    return db((db.relationship.created_by == user_id)&
              (db.relationship.person == db.user_status.created_by)
              ).select(db.user_status.ALL, orderby=~db.user_status.created_on, distinct=True)

def post_comments(post_id):
    return db(db.comment_item.item_id==post_id).select()

def post_like_status(post_id):
    return db((db.post_like.post == post_id) & (db.post_like.created_by == auth.user.id)).select()

def post_fave_status(post_id):
    return db((db.post_fave.post == post_id) & (db.post_fave.created_by == auth.user.id)).select()

def recent_posts(start, count):
    return db(db.post).select(orderby=~db.post.created_on, limitby=(start,start+count))
