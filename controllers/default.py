# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    if auth.has_membership(1):
        redirect(URL('pacjent', 'index'))
    elif auth.has_membership(2):
        redirect(URL('lekarz', 'index'))
    elif auth.has_membership(3):
        redirect(URL('admin', 'index'))

    return dict('błąd')

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0) == 'register':
        remove_extra_fields('admin')
        db.auth_user.user_type.default = 'admin'

    if request.args(0) ==  'profile':
        remove_extra_fields(auth.user.user_type)

    return dict(form=auth())
