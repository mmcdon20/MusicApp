# coding: utf8

def profileButtons():
    user_id = request.vars.user_id
    relation = user_relation(user_id)
    
    if relation:
        db(db.relationship.id == relation.id).delete()
    else:
        db.relationship.insert(person=user_id, status='request')
        
    return profile_buttons(user_id)

def postButtons(post_id,action):
    post    = db.post(post_id)
    record  = post_like_status(int(post_id))
    faves   = post_fave_status(int(post_id))
    
    if action == 'Fave' and faves:
        db((db.post_fave.post==post_id) & (db.post_fave.created_by==auth.user.id)).delete()
    elif action == 'Fave':
        db.post_fave.insert(post=post_id)
    elif not record: # checks for Like/Dislike
        db.post_like.insert(post=post_id, status=action)
    elif record[0].status == action:
        db((db.post_like.post==post_id) & (db.post_like.created_by==auth.user.id)).delete()
    else:
        db((db.post_like.post==post_id) & (db.post_like.created_by==auth.user.id)).update(status=action)

    return music_item_status_buttons(post)

def likeButton():
    return postButtons(request.vars.post_id, 'Like')
 
def dislikeButton():
    return postButtons(request.vars.post_id, 'Dislike')

def faveButton():
    return postButtons(request.vars.post_id, 'Fave')
