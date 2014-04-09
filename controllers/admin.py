# -*- coding: utf-8 -*-


@auth.requires_membership('admin')
def index():
    type_ = 'pacjent'

    remove_extra_fields(type_)
    grid = SQLFORM.grid(db.auth_user.user_type == type_ and db.auth_user.registration_key == 'pending',
                        user_signature=False,
                        editable=False,
                        deletable=False,
                        details=False,
                        create=False,
                        links=[dict(
                            header='Aktywacja',
                            body=lambda row: A('aktywuj', _href=URL("admin", "activate", args=[row.id]))
                        )]
                        )
    return locals()

@auth.requires_membership('admin')
def activate():
    if request.args(0) != '':
        db(db.auth_user.id == request.args(0)).update(registration_key='')
    session.flash = 'Konto zostało aktywowane.'

    redirect(URL('index'))

@auth.requires_membership('admin')
def poradnie():
    grid = SQLFORM.grid(db.department)
    return locals()

@auth.requires_membership('admin')
def konta():
    type_ = request.args(0)
    db.auth_user.user_type.default = type_
    remove_extra_fields(type_)

    grid = SQLFORM.grid(db.auth_user.user_type == type_,
                        user_signature=False, args=[type_],
                        oncreate=lambda form: auth.add_membership(type_, db(db.auth_user.email == form.vars.email).select().first().id)
                        )
    return locals()