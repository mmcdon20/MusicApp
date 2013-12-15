# coding: utf8
# eventually we will need to convert these to proper ajax calls

def changeStatus():
    id = request.post_vars.commentid
    post = db.post(id)
    new_status = request.post_vars.status
    
    record = db((db.post_like.post == id) & (db.post_like.created_by == auth.user.id)).select()

    if not record:
        db.post_like.insert(post=id, status=new_status)
    elif record[0].status == new_status:
        db((db.post_like.post==id) & (db.post_like.created_by==auth.user.id)).delete()
    else:
        db((db.post_like.post==id) & (db.post_like.created_by==auth.user.id)).update(status=new_status)

    return locals()

def profileButtons():
    user_id = request.vars.user_id
    relation = user_relation(user_id)
    
    if relation:
        db(db.relationship.id == relation.id).delete()
    else:
        db.relationship.insert(person=user_id, status='request')
        
    return profile_buttons(user_id)
