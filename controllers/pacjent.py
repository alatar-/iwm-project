# -*- coding: utf-8 -*-

import datetime

@auth.requires_membership('pacjent')
def index():
    redirect('moje_wizyty')

@auth.requires( auth.has_membership('pacjent') or auth.has_membership('admin') or auth.has_membership('lekarz'))
def dane_kontaktowe():
    if( auth.has_membership('pacjent') ):
        pacjentId = auth.user_id
    else:
        if request.args(0):
            pacjentId = request.args(0)
    session.patient = pacjentId
    db.contacts.id_patient.readable = db.contacts.id_patient.writable = False
    db.contacts.id.readable = db.contacts.id.writable = False
    db.contacts.id_patient.default = auth.user_id
    grid = SQLFORM.grid(
        db.contacts.id_patient == pacjentId,
        user_signature=False,
        editable=True,
        deletable=True,
        details=False,
        create=False,
        csv=False,
    )
    return locals()

@auth.requires( auth.has_membership('pacjent') or auth.has_membership('admin') or auth.has_membership('lekarz'))
def dodaj_kontakt():
    if (not session.patient):
        redirect(URL('dane_kontaktowe'))
    return locals() 

@auth.requires( auth.has_membership('pacjent') or auth.has_membership('admin') or auth.has_membership('lekarz'))
def save_contact():
    pacjentId = session.patient
    db.contacts.insert(
        id_patient=pacjentId,
        name=request.vars["name"],
        surname=request.vars["surname"],
        phone_numer=request.vars["phone_numer"]
    )
    redirect(URL("dane_kontaktowe", args=[pacjentId]))    


@auth.requires( auth.has_membership('pacjent') or auth.has_membership('admin') or auth.has_membership('lekarz'))
def moje_wizyty():
    if( auth.has_membership('pacjent') ):
        pacjentId = auth.user_id
    else:
        if request.args(0):
            pacjentId = request.args(0)
    db.visit.id_patient.writable = db.visit.id_doctor.writable = db.visit.visit_day.writable = db.visit.visit_hour.writable = False
    grid = SQLFORM.grid((db.visit.id_patient == pacjentId) & (db.visit.visit_day == request.now.date),
        user_signature=False,
        editable=False,
        deletable=False,
        details=True,
        create=False,
        left=db.visit.on(db.visit.id_doctor == db.auth_user.id),
        fields=[db.visit.visit_day, db.visit.visit_hour, db.auth_user.first_name,  db.auth_user.last_name, db.visit.reason],
        orderby=db.visit.visit_day|db.visit.visit_hour,
        csv=False,
    )
    if(not request.args(1)):
        grid1 = SQLFORM.grid((db.visit.id_patient == pacjentId) & (db.visit.visit_day > request.now.date),
            user_signature=False,
            editable=False,
            deletable=False,
            details=True,
            create=False,
            left=db.visit.on(db.visit.id_doctor == db.auth_user.id),
            fields=[db.visit.visit_day, db.visit.visit_hour, db.auth_user.first_name,  db.auth_user.last_name, db.visit.reason],
            orderby=db.visit.visit_day|db.visit.visit_hour,
            csv=False,
        )
        grid2 = SQLFORM.grid((db.visit.id_patient == pacjentId) & (db.visit.visit_day < request.now.date),
            user_signature=False,
            editable=False,
            deletable=False,
            details=True,
            create=False,
            left=db.visit.on(db.visit.id_doctor == db.auth_user.id),
            fields=[db.visit.visit_day, db.visit.visit_hour, db.auth_user.first_name,  db.auth_user.last_name, db.visit.reason],
            orderby=db.visit.visit_day|db.visit.visit_hour,
            csv=False,
        )
    return locals()

@auth.requires(auth.has_membership('pacjent') or auth.has_membership('admin') or auth.has_membership('lekarz'))
def nowa_wizyta():
    if not(session.patient) and not(auth.has_membership('pacjent')):
        if 'patient_id' in request.vars.keys():
            session.patient = int(request.vars['patient_id'])

    if(request.args(4)):
        reason = FORM(INPUT(_name='Reason', requires=IS_NOT_EMPTY()), INPUT(_type='submit', _value="Rejestruj"))
        a = request.args
        if reason.process().accepted:
            dodaj(a, request.vars["Reason"])
    ####### 4th level
    if request.args(2):
        grid3 = {}
        map = {'Monday': "Poniedziałek", "Tuesday": "Wtorek", "Wednesday": "Środa", "Thursday": "Czwartek",
         "Friday": "Piątek", "Saturday" : "Sobota", "Sunday" : "Niedziela"}
        for i in range(-2,5,1):
            dat = request.args(2)
            date = (datetime.date(int(dat[0:4]), int(dat[5:7]), int(dat[8:10])) + datetime.timedelta(days=i))
            day = map[date.strftime("%A")]

            rows = db(
                (db.office_hours.id_doctor == request.args(1)) & 
                (db.office_hours.week_day == day) & 
                (db.office_hours.id_department == request.args(0))
            ).select()
            key = (str(day), str(date), str(request.args(0)), str(request.args(1)))
            grid3[key] = []
            for row in rows:
                grid3[key].extend(create_hours(str(row.office_begin), str(row.office_end)))

            rows2 = db(
                (db.visit.visit_day == str(date)) & 
                (db.visit.id_doctor == request.args(1))
            ).select()

            for row in rows2:
                if row.visit_hour in grid3[key]:
                    grid3[key].remove(row.visit_hour)

    ####### 3rd level
    form = SQLFORM.factory(
        Field('data', 'date', label="", requires=[
            IS_DATE_IN_RANGE(
                minimum=(datetime.date.today() + datetime.timedelta(days=1)),
                maximum=(datetime.date.today() + datetime.timedelta(days=150)),
                error_message='maksymalnie 150 dni w przód'
            )
        ])
    )
    if form.process().accepted:
        response.flash = ''
        redirect(URL('nowa_wizyta', args=[request.args(0), request.args(1), form.vars.data]))

    ####### 2nd level
    if request.args(0):
        query1 = (db.department.id == request.args(0))
        query2 = (db.office_hours.id_department == request.args(0))

        if request.args(1):
            query2 = (
                (db.office_hours.id_department == request.args(0)) &
		(db.office_hours.id_doctor == request.args(1))
            )
        db.auth_user.id.readable = False
        grid2 = SQLFORM.grid(
            query=query2,
             user_signature=False,
             editable=False,
             deletable=False,
             details=False,
             create=False,
             left=db.office_hours.on(db.auth_user.id == db.office_hours.id_doctor),
             links=[dict(
                        header='Wybierz lekarza',
                        body=lambda row: A('wybierz',
                                           _href=URL(args=[request.args(0), row.auth_user.id]))
                    ),
                    dict(
                        header='Najbliższa wizyta',
                        body=lambda row: A('szukaj',
                                           _href=URL('szukaj', args=[request.args(0), row.auth_user.id]))
                    )
             ],
             fields=[
                 db.auth_user.last_name,
                 db.auth_user.first_name,
                 db.office_hours.week_day,
                 db.office_hours.office_begin,
                 db.office_hours.office_end,
                 db.auth_user.id
             ],
             orderby=db.office_hours.week_day|db.office_hours.office_begin,
             csv=False
        )

    ####### 1st level
    db.department.id.readable = False
    query1 = db.department if not request.args(0) else (db.department.id == request.args(0))
    grid1 = SQLFORM.grid(
        query=query1,
        user_signature=False,
        editable=False,
        deletable=False,
        details=False,
        create=False,
        links=[dict(
                    header='Wybierz poradnie',
                    body=lambda row: A(
                        'wybierz',
                         _href=URL(args=[row.id])
                    )
               ),
               dict(
                   header='Najbliższa wizyta',
                   body=lambda row: A('szukaj',
                                      _href=URL('szukaj', args=[row.id]))
               )
        ],
        csv=False
    )       

    return locals()


@auth.requires(auth.has_membership('pacjent') or auth.has_membership('admin') or auth.has_membership('lekarz'))
def szukaj():
    drugi = ''
    map = {'Monday': "Poniedziałek", "Tuesday": "Wtorek", "Wednesday": "Środa", "Thursday": "Czwartek",
           "Friday": "Piątek", "Saturday": "Sobota", "Sunday": "Niedziela"}
    date = ''

    if request.args(1):
        drugi = request.args(1)

        for i in xrange(1, 500):
            date = datetime.date.today() + datetime.timedelta(days=i)
            day = map[date.strftime("%A")]

            rows = db(
                (db.office_hours.id_doctor == request.args(1)) & 
                (db.office_hours.week_day == day) & 
                (db.office_hours.id_department == request.args(0))
            ).select()
            #

            list_ = []
            for row in rows:
                list_.extend(create_hours(str(row.office_begin), str(row.office_end)))

            rows2 = db(
                (db.visit.visit_day == str(date)) & 
                (db.visit.id_doctor == request.args(1))
            ).select()

            for row in rows2:
                if row.visit_hour in list_:
                    list_.remove(row.visit_hour)

            if len(list_):
                break

    else:
        for i in xrange(1, 500):
            date = datetime.date.today() + datetime.timedelta(days=i)
            day = map[date.strftime("%A")]

            rows = db(
                (db.office_hours.week_day == day) & 
                (db.office_hours.id_department == request.args(0))
            ).select()

            min_ = '20:00'
            d2 = ''
            for row in rows:
                doc_id = row.id_doctor
                list2 = (create_hours(str(row.office_begin), str(row.office_end)))

                rows2 = db(
                    (db.visit.visit_day == str(date)) & 
                    (db.visit.id_doctor == doc_id)
                ).select()

                for row in rows2:
                    if row.visit_hour in list2:
                        list2.remove(row.visit_hour)

                if len(list2) and min_ > list2[0]:
                    drugi = doc_id
                    min_ = list2[0]

            if min_ != '20:00':
                break

    redirect(URL('nowa_wizyta', args=[request.args(0), drugi, date]))

@auth.requires(auth.has_membership('pacjent') or auth.has_membership('admin') or auth.has_membership('lekarz'))
def dodaj(in_a, in_reason):
    db.visit.insert(
        id_patient=session.patient if session.patient else auth.user_id,
        id_doctor=in_a(1),
        visit_day=in_a(2),
        visit_hour=(in_a(3) + ':' + in_a(4)),
        reason=in_reason
    )
    patient_id = session.patient
    session.patient = None
    redirect(URL('moje_wizyty', args=patient_id))
