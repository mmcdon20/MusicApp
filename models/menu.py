# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('jam',SPAN('Tunes')),
                  _class="brand",_href=URL('index'))
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

def setup_tune_menu():
    # shortcuts
    app = request.application
    ctr = request.controller

    genre_list = []

    for genre in GENRES:
        to_add = (genre, False, URL('genre', args=genre))
        genre_list.append(to_add)

    response.menu += [(SPAN('Tunes', _class='highlighted'), False, URL('index'), genre_list)]

setup_tune_menu()

auth.settings.login_next = URL('profile')
auth.settings.register_next = URL('profile')

search_form  = SQLFORM.factory(Field('query','string'), _class='navbar-search pull-left')
search_form.custom.widget.query['_placeholder']= 'Search for jams and jammers'

upload_form  = SQLFORM(db.post)

if search_form.process().accepted:
    redirect(URL("search", vars=dict(query=search_form.vars.query)))

if upload_form.process().accepted:
    redirect(URL("post", args=upload_form.vars.id))

if not auth.user:
    register_form = auth.register()

if "auth" in locals(): auth.wikimenu()
