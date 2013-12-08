# coding: utf8
# eventually we will need to convert these to proper ajax calls

def addFriend():
    db.relationship.insert(person=request.post_vars.person, status=request.post_vars.status)
    return locals()

def removeFriend():
    db(db.relationship.id == request.post_vars.rid).delete()
    return locals()

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
