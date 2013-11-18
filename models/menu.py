# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('jam',SPAN('Tunes')),
                  _class="brand",_href='index')
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

def _setupTuneMenu():
    # shortcuts
    app = request.application
    ctr = request.controller
    
    genreList = []
    
    for genre in GENRES:
        toAdd = (genre, False, URL('default', 'genre', args=genre))
        genreList.append(toAdd)
    
    response.menu += [(SPAN('Tunes', _class='highlighted'), False, 'index', genreList)]

def _setupMainMenu():
    response.menu += [
        (T('Search'), False, URL('default', 'search'), []),
        (T('About'), False, URL('default', 'about'), [])
    ]

def _setupAuthMenu():
    response.menu += [
        ('|', False, '', []),
        (T('Profile'), False, URL('default', 'profile'), []),
        (T('Friends'), False, URL('default', 'friends'), []),
        (T('Upload'), False, URL('default', 'upload'), [])
    ]

_setupTuneMenu()
_setupMainMenu()
if auth.user:
    _setupAuthMenu()
if "auth" in locals(): auth.wikimenu()
