# -*- coding: utf-8 -*-

@auth.requires_membership('lekarz')
def index():
    redirect('wizyty')

@auth.requires_membership('lekarz')
def wizyty():
    # |
    grid = SQLFORM.grid(
        (db.visit.id_doctor == auth.user_id) & (db.visit.visit_day >= request.now.date),
        user_signature=False,
        editable=True,
        deletable=False,
        details=True,
        create=False,
        left=db.visit.on(db.visit.id_patient == db.auth_user.id),
        fields=[db.visit.visit_day, db.visit.visit_hour, db.auth_user.first_name,  db.auth_user.last_name, db.auth_user.pesel],
        orderby=db.visit.visit_day|db.visit.visit_hour,
        csv=False
    )
    return locals()

@auth.requires_membership('lekarz')
def my_form_processing(form):
    if form.vars.office_begin >= form.vars.office_end:
        form.errors.office_end = 'begin < end'
    else:
        # response.flash = 'in'
        rows = db(
            (db.office_hours.week_day == form.vars.week_day) & 
            (db.office_hours.id_doctor == auth.user_id)
        ).select()
        for row in rows:
            if not (form.vars.office_begin >= row.office_end or form.vars.office_end <= row.office_begin):
                form.errors.office_end = 'cwaniaczek...'
                break

@auth.requires_membership('lekarz')
def plan():
    db.office_hours.id_doctor.readable = db.office_hours.id_doctor.writable = False
    db.office_hours.id_doctor.default = auth.user_id
    grid = SQLFORM.grid(
        db.office_hours.id_doctor == auth.user_id,
        user_signature=False,
        details=False,
        editable=False,
        headers={'department.name': 'Poradnia'},
        onvalidation=my_form_processing,
        left=db.office_hours.on(db.office_hours.id_department == db.department.id),
        fields=[db.office_hours.week_day, db.office_hours.office_begin, db.office_hours.office_end, db.department.name],
        csv=False
    )
    return locals()
