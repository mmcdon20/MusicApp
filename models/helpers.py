# coding: utf8
###############################################################################
#                   Helper Functions                                          #
###############################################################################

def fullname(user_id):
    if user_id is None:
        return "Unknown"
    return "%(first_name)s %(last_name)s" % db.auth_user(user_id)

def commentitem(comment):
    text = comment.body
    name = fullname(comment.created_by)
    date = prettydate(comment.created_on)
    userlink = str(A(name,_href=URL('profile',args=comment.created_by)))
    postlink = str(A("link",_href=URL('post',args=comment.item_id)))
    info = db(db.profile_info.person==comment.created_by).select().first()

    if info.picture:
        imageref = URL('download', args=info.picture)
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
                """ + userlink + " / " + date + " / " + postlink + """
            </div>
        </li>
    """)

def musicitem(post):

    name        = fullname(post.created_by)
    postref     = URL('post',args=post.id)
    genrelink   = str(A(post.genre, _href=URL('genre', args=post.genre)))
    postlink    = str(A(post.title + " by " + post.artist, _href=postref))
    date        = prettydate(post.created_on)
    userlink    = str(A(name,_href=URL('profile',args=post.created_by)))
    description = post.description
    attachref   = URL('download',args=post.attachment)

    #Count the number of likes and the number of dislikes
    likes = str(db((db.post_like.status == 'Like') & (db.post_like.post==post.id)).count())
    dislikes = str(db((db.post_like.status == 'Dislike') & (db.post_like.post==post.id)).count())
    
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
                <a class="pull-left" href=\"""" + postref + """">
                    <img class="media-object" width="150px" src=\"""" + imageref + """">
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
            <h6>Likes/dislikes</h6>
            <h6>"""+likes+"/"+dislikes+"""</h6>
            """+buttons+"""
    """)

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
    
    like_btn = str(A(like_icon+'Jam It', _class=likestyle, _onclick='changeStatus(' + str(post.id) + ',' + '"Like"' + ');'))
    dislike_btn = str(A(dislike_icon+'Can It', _class=dislikestyle, _onclick='changeStatus(' + str(post.id) + ',' + '"Dislike"' + ');'))

    return like_btn + dislike_btn

def musicItemList(posts):
    x = '<div class="post-container"><ul class="media-list">'

    for post in posts:
        x += musicitem(post)
        #x += music_item_status_buttons(post)

    x += '</ul></div>'

    return XML(x)

def commentItemList(comments):
    x = '<div class=""><ul class="media-list">'

    for comment in comments:
        x += commentitem(comment)

    x += '</ul></div>'

    return XML(x)

def personItemListNoRelation(people):
    x = '<div class="friend-container"><ul class="media-list">'

    for person in people:
        x += personItem(person)

    x += '</ul></div>'

    return XML(x)

def personItemList(relations, userId):
    x = '<div class="friend-container"><ul class="media-list">'

    for relation in relations:
        # Create a LI with the correct person
        if relation.created_by == userId:
            x += personItem(db.auth_user(relation.person))
        else:
            x += personItem(db.auth_user(relation.created_by))

    x += '</ul></div>'

    return XML(x)

def personItem(person):
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
                <a class="pull-left" href=\"""" + profileRef + """">
                    <img class="media-object" src=\"""" + imageref + """">
                </a>
                <div class="media-body">
                    <div class="person-info">
                        <h5>""" + name + """</h5>
                        <table>
                            <tr>
                                <td>Location:</td>
                                <td>""" + location + """</td>
                            </tr>
                            <tr>
                                <td>Gender:</td>
                                <td>""" + gender + """</td>
                            </tr>
                            <tr>
                                <td>Age:</td>
                                <td>""" + age + """</td>
                            </tr>
                            <tr>
                                <td>Genres:</td>
                                <td>""" + genres + """</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </li>
    """)

def userBar():
    action = '/user'
    if auth.user:
        logout=A('logout', _href=action+'/logout')
        profile=A('profile', _href=action+'/profile')
        password=A('change password', _href=action+'/change_password')
        bar = SPAN(auth.user.email, ' | ', profile, ' | ', password, ' | ', logout, _class='auth_navbar')
    else:
        login=A('login', _href=action+'/user/login')
        register=A('register',_href=action+'/register')
        lost_password=A('lost password', _href=action+'/request_reset_password')
        bar = SPAN(' ', login, ' | ', register, ' | ', lost_password, _class='auth_navbar')
    return bar