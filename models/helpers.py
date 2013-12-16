# coding: utf8
###############################################################################
#                   Helper Functions                                          #
###############################################################################

def profile_buttons(user_id):
    edit = status = friend = uid = ctype = ''
    
    if auth.user and auth.user.id == user_id:
        edit = '<a href="#editModal" class="btn" role="button" data-toggle="modal">edit info</a>'
        status = '<a href="#statusModal" class="btn" role="button" data-toggle="modal">edit status</a>'
        ctype = 'btn-group'
    elif auth.user and auth.user.id != user_id:
        uid = '<INPUT type="hidden" id="user_id" name="user_id" value="{user_id}"/>'.format(**locals())
        aj = "ajax('/{app}/ajax/profileButtons', ['user_id'], 'target');".format(app=request.application)
        if user_relation(user_id):
            friend = '<a class="btn" role="button" onclick="{aj}">Remove friend</a>'.format(**locals())
        else:
            friend = '<a class="btn btn-primary" role="button" onclick="{aj}">Add friend</a>'.format(**locals())
    
    return XML("""
    <div id="target">
        <div id="buttons" class="{ctype}">
            {edit}
            {status}
            {uid}
            {friend}
        </div>    
    </div>
    """.format(**locals()))


def fullname(user_id):
    if user_id is None:
        return "Unknown"
    return "%(first_name)s %(last_name)s" % db.auth_user(user_id)

def comment_item(comment):
    text = comment.body
    name = fullname(comment.created_by)
    date = prettydate(comment.created_on)
    userlink = A(name,_href=URL('profile',args=comment.created_by))
    postlink = A("link",_href=URL('post',args=comment.item_id))
    info = db(db.profile_info.person==comment.created_by).select().first()

    if info.picture:
        imageref = URL('download', args=info.picture)
    else:
        imageref = URL('static', 'images/user_placeholder.jpg')

    return XML("""
        <li class="media">
            <div class="pull-left">
                <img class="media-object" height="50" width="50" src="{imageref}" />
            </div>
            <div class="media-body">
                {text}
                <br />
                {userlink} / {date} / {postlink}
            </div>
        </li>
    """.format(**locals()))

def music_item(post):

    name        = fullname(post.created_by)
    postref     = URL('post',args=post.id)
    genrelink   = A(post.genre, _href=URL('genre', args=post.genre))
    postlink    = A(post.title + " by " + post.artist, _href=postref)
    date        = prettydate(post.created_on)
    userlink    = A(name,_href=URL('profile',args=post.created_by))
    description = post.description
    attachref   = URL('download',args=post.attachment)

    if post.album_art:
        imageref = URL('download',args=post.album_art)
    else:
        imageref = URL('static', 'images/tn_placeholder.png')

    if auth.user:
        buttons = music_item_status_buttons(post)
    else:
        buttons = ""

    return XML("""
            <li class="media">
                <div class="pull-left center">
                    <img class="media-object" width="150px" src="{imageref}">
                    {buttons}
                </div>
                <div class="media-body">
                    <h4 >{genrelink} / {postlink}</h4>
                    <h5>{date} | Posted by {userlink}</h5>
                    <p>{description}</p>
                    <audio controls="controls" style="max-width:100%">
                        <source src="{attachref}">
                    </audio>
                </div>
            </li>
            
    """.format(**locals()))

def music_item_status_buttons(post):
    record = db((db.post_like.post == post.id) & (db.post_like.created_by == auth.user.id)).select()
    
    if not record:
        likestyle    = 'btn'
        dislikestyle = 'btn'
    elif record[0].status == 'Like':
        likestyle    = 'btn btn-primary'
        dislikestyle = 'btn'
    else:
        likestyle    = 'btn'
        dislikestyle = 'btn btn-primary'
    
    like_icon = I(_class='icon-thumbs-up')
    dislike_icon = I(_class='icon-thumbs-down')
    fave_icon = I(_class='icon-heart')
    
    like_btn = str(A(like_icon, _class=likestyle, _onclick='changeStatus(' + str(post.id) + ',' + '"Like"' + ');'))
    dislike_btn = str(A(dislike_icon, _class=dislikestyle, _onclick='changeStatus(' + str(post.id) + ',' + '"Dislike"' + ');'))
    fave_btn = str(A(fave_icon, _class='btn'))
    btn_id = 'button' + str(post.id)

    return '<div id="' + btn_id + '" class="btn-group">' + like_btn + dislike_btn + fave_btn + '</div>'

def music_item_list(posts):
    x = '<div class="post-container"><ul class="media-list">'

    for post in posts:
        x += music_item(post)

    x += '</ul></div>'

    return XML(x)

def comment_item_list(comments):
    x = '<div class=""><ul class="media-list">'

    for comment in comments:
        x += comment_item(comment)

    x += '</ul></div>'

    return XML(x)

def person_item_list_no_relation(people):
    x = '<div class="friend-container"><ul class="media-list">'

    for person in people:
        x += person_item(person)

    x += '</ul></div>'

    return XML(x)

def person_item_list(relations, user_id):
    x = '<div class="friend-container"><ul class="media-list">'

    for relation in relations:
        # Create a LI with the correct person
        if relation.created_by == user_id:
            x += person_item(db.auth_user(relation.person))
        else:
            x += person_item(db.auth_user(relation.created_by))

    x += '</ul></div>'

    return XML(x)

def person_item(person):
    # If user has no profile, create one.
    info = db(db.profile_info.person==person.id).select().first()
    if info is None:
        db.profile_info.insert(person=person.id)
        info = db(db.profile_info.person==person.id).select().first()

    name        = fullname(person.id)
    profileRef  = URL('profile', args=person.id)
    location    = info.user_location or 'N/A'
    gender      = info.gender or 'N/A'
    age         = prettydate(info.birthdate).replace(' years ago', '') or 'N/A'
    genres      = info.genres or 'N/A'
    if info.picture:
        imageref = URL('download', args=info.picture)
    else:
        imageref = URL('static', 'images/user_placeholder.jpg')

    return XML("""
            <li class="media">
                <a class="pull-left" href="{profileRef}">
                    <img class="media-object" src="{imageref}">
                </a>
                <div class="media-body">
                    <div class="person-info">
                        <h5>{name}</h5>
                        <table>
                            <tr>
                                <td>Location:</td>
                                <td>{location}</td>
                            </tr>
                            <tr>
                                <td>Gender:</td>
                                <td>{gender}</td>
                            </tr>
                            <tr>
                                <td>Age:</td>
                                <td>{age}</td>
                            </tr>
                            <tr>
                                <td>Genres:</td>
                                <td>{genres}</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </li>
    """.format(**locals()))
