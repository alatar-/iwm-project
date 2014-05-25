# -*- coding: utf-8 -*-


@auth.requires_membership('admin')
def index():
    type_ = 'pacjent'

    remove_extra_fields(type_)
    grid = SQLFORM.grid(
        db.auth_user.user_type == type_ and db.auth_user.registration_key == 'pending',
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

@auth.requires(auth.has_membership('admin') or auth.has_membership('lekarz'))
def osoby_kontaktowe():
    if not request.args(0):
        redirect('konta', 'pacjent')
    rows = db(db.auth_user.id == str(request.args(0))).select()
    try:
        pacjent = "%s %s" % (rows[0].first_name, rows[0].last_name)
    except IndexError:
        redirect('konta', 'pacjent')

    db.contacts.id_patient.readable = db.contacts.id_patient.writable = False
    db.contacts.id.readable = db.contacts.id.writable = False
    db.contacts.id_patient.default = request.args(0)
    grid = SQLFORM.grid(
        db.contacts.id_patient == request.args(0),
        user_signature=False,
        editable=True,
        deletable=True,
        details=False,
        create=True,
        csv=True,
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

@auth.requires(auth.has_membership('admin') or auth.has_membership('lekarz'))  
def konta():
    type_ = request.args(0)
    db.auth_user.user_type.default = type_
    remove_extra_fields(type_)

    if type_ == 'pacjent':
        db.auth_user.nn_patient.readable = db.auth_user.nn_patient.readable = False
        grid = SQLFORM.grid(
            db.auth_user.user_type == type_,
            user_signature=False, 
            args=[type_],
            oncreate=lambda form: auth.add_membership(type_, db(db.auth_user.email == form.vars.email).select().first().id),
            links=[
                dict(
                    header='Osoby kontaktowe',
                    body=lambda row: A('osoby kontaktowe', _href=URL('pacjent', 'dane_kontaktowe', args=[row.id]))
                ),
                dict(
                    header='Historia wizyt',
                    body=lambda row: A('historia', _href=URL("pacjent", "moje_wizyty", args=[row.id]))
                ),
                dict(
                    header='Dodaj wizytę',
                    body=lambda row: A('dodaj', _href=URL("pacjent", "nowa_wizyta", vars={'patient_id':row.id}))
                )
            ]
        )
    else:
        grid = SQLFORM.grid(
            db.auth_user.user_type == type_,
            user_signature=False, args=[type_],
            oncreate=lambda form: auth.add_membership(type_, db(db.auth_user.email == form.vars.email).select().first().id)
        )
    return locals()