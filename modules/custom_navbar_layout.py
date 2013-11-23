#!/usr/bin/env python
# coding: utf8
from gluon import *
def navbar(auth_navbar):
    bar = auth_navbar
    user = bar["user"]
    
    li_about = LI(A(I(_class="icon-info-sign"), ' ',
                          current.T("About"),
                          _href=URL("about"), _rel="nofollow"))
    li_search = LI(A(I(_class="icon-search"), ' ',
                          current.T("Search"),
                          _href=URL("search"), _rel="nofollow"))
    
    if not user:
        toggletext = "Login/Register"
        toggle = A(toggletext,
                   _href="#",
                   _class="dropdown-toggle",
                   _rel="nofollow",
                   **{"_data-toggle": "dropdown"})
        li_register = LI(A(I(_class="icon-user"), ' ',
                          current.T("Register"),
                          _href=URL("register"), _rel="nofollow"))
        li_password = LI(A(I(_class="icon-book"), ' ',
                         current.T("Forgot password?"),
                         _href="#resetModal", 
                         _role="Button",
                         _rel="nofollow",
                         **{'_data-toggle':'modal'}))
        li_login = LI(A(I(_class="icon-off"), ' ',
                         current.T("Login"),
                         _href="#loginModal", 
                         _role="Button",
                         _rel="nofollow",
                         **{'_data-toggle':'modal'}))
        dropdown = UL(li_register,
                      li_password,
                      LI('', _class="divider"),
                      li_about,
                      li_search,
                      LI('', _class="divider"),
                      li_login,
                      _class="dropdown-menu", _role="menu")
    else:
        toggletext = "%s %s" % (bar["prefix"], user)
        toggle = A(toggletext,
                   _href="#",
                   _class="dropdown-toggle",
                   _rel="nofollow",
                   **{"_data-toggle": "dropdown"})
        li_profile = LI(A(I(_class="icon-home"), ' ',
                          current.T("Profile"),
                          _href=URL("profile"), _rel="nofollow"))
        li_friends = LI(A(I(_class="icon-user"), ' ',
                          current.T("Friends"),
                          _href=URL("friends"), _rel="nofollow"))
        li_upload = LI(A(I(_class="icon-upload"), ' ',
                          current.T("Upload"),
                          _href="#uploadModal", 
                          _role="Button",
                          _rel="nofollow",
                          **{'_data-toggle':'modal'}))

        li_password = LI(A(I(_class="icon-book"), ' ',
                         current.T("Change password"),
                         _href="#passwordModal", 
                         _role="Button",
                         _rel="nofollow",
                         **{'_data-toggle':'modal'}))
        
        li_logout = LI(A(I(_class="icon-off"), ' ',
                         current.T("logout"),
                         _href=bar["logout"], _rel="nofollow"))
        dropdown = UL(li_profile,
                      li_friends,
                      li_password,
                      LI('', _class="divider"),
                      li_about,
                      li_search,
                      li_upload,
                      LI('', _class="divider"),
                      li_logout,
                      _class="dropdown-menu", _role="menu")
    return LI(toggle, dropdown, _class="dropdown")
