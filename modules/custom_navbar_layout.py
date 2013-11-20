#!/usr/bin/env python
# coding: utf8
from gluon import *
def navbar(auth_navbar):
    bar = auth_navbar
    user = bar["user"]

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
                         current.T("Lost Password?"),
                         _href=URL('user/request_reset_password'), rel="nofollow")) #  ADD NEXT PARAMETER TO URL!!!
        li_login = LI(A(I(_class="icon-off"), ' ',
                         current.T("Login"),
                         _href=bar["login"], _rel="nofollow"))
        dropdown = UL(li_register,
                      li_password,
                      LI('', _class="divider"),
                      li_login,
                      _class="dropdown-menu", _role="menu")
    else:
        toggletext = "%s, %s" % (bar["prefix"], user)
        toggle = A(toggletext,
                   _href="#",
                   _class="dropdown-toggle",
                   _rel="nofollow",
                   **{"_data-toggle": "dropdown"})
        li_profile = LI(A(I(_class="icon-user"), ' ',
                          current.T("Profile"),
                          _href=URL("profile"), _rel="nofollow"))
        li_password = LI(A(I(_class="icon-book"), ' ',
                         current.T("Change Password"),
                         _href=URL('user/change_password'), rel="nofollow")) #  ADD NEXT PARAMETER TO URL!!!
        li_logout = LI(A(I(_class="icon-off"), ' ',
                         current.T("logout"),
                         _href=bar["logout"], _rel="nofollow"))
        dropdown = UL(li_profile,
                      li_password,
                      LI('', _class="divider"),
                      li_logout,
                      _class="dropdown-menu", _role="menu")
    return LI(toggle, dropdown, _class="dropdown")
