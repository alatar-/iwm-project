# -*- coding: utf-8 -*-

import datetime

@auth.requires_membership('pacjent')
def index():
    redirect('moje_wizyty')


@auth.requires_membership('pacjent')
def moje_wizyty():

    grid = SQLFORM.grid((db.visit.id_patient == auth.user_id) & (db.visit.visit_day >= request.now.isoformat()),
                        user_signature=False,
                        editable=False,
                        deletable=False,
                        details=False,
                        create=False,
                        left=db.visit.on(db.visit.id_doctor == db.auth_user.id),
                        fields=[db.visit.visit_day, db.visit.visit_hour, db.auth_user.first_name,  db.auth_user.last_name],
                        orderby=db.visit.visit_day|db.visit.visit_hour,
                        csv=False
    )
    return locals()

@auth.requires_membership('pacjent')
def nowa_wizyta():

    db.department.id.readable = False
    query1 = db.department

    form = SQLFORM.factory(
        Field('data', 'date', label="", requires=[
            IS_DATE_IN_RANGE(
                minimum=(datetime.date.today() + datetime.timedelta(days=1)),
                maximum=(datetime.date.today() + datetime.timedelta(days=730)),
                error_message='w sensownym zakresie kolego...')])
    )

    grid3 = {}
    if form.process().accepted:
        response.flash = ''
        redirect(URL('nowa_wizyta', args=[request.args(0), request.args(1), form.vars.data]))

    if request.args(2):
        # form.vars.data.default = form.vars.data
        # grid3 = ''
        map = {'Monday': "Poniedziałek", "Tuesday": "Wtorek", "Wednesday": "Środa", "Thursday": "Czwartek",
         "Friday": "Piątek", "Saturday" : "Sobota", "Sunday" : "Niedziela"}
        for i in range(-2,3,1):
            dat = request.args(2)
            date = (datetime.date(int(dat[0:4]), int(dat[5:7]), int(dat[8:10])) + datetime.timedelta(days=i))
            day = map[date.strftime("%A")]

            rows = db((db.office_hours.id_doctor == request.args(1)) & (db.office_hours.week_day == day) & (db.office_hours.id_department == request.args(0))).select()
            #
            key = (str(day), str(date), str(request.args(0)), str(request.args(1)))
            grid3[key] = []
            for row in rows:
                grid3[key].extend(create_hours(str(row.office_begin), str(row.office_end)))

            rows2 = db((db.visit.visit_day == str(date)) & (db.visit.id_doctor == request.args(1))).select()

            # grid3[key] = []
            for row in rows2:
                # try:
                #     grid3[key].append(row.visit_hour)
                if row.visit_hour in grid3[key]:
                    grid3[key].remove(row.visit_hour)
                # except:
                #     pass



    # elif form.errors:
    #     response.flash = 'form has errors'

    if request.args(0):
        query1 = (db.department.id == request.args(0))
        query2 = (db.office_hours.id_department == request.args(0))

        if request.args(1):
            query2 = (db.office_hours.id_department == request.args(0)) & (db.office_hours.id_doctor == request.args(1))

        db.auth_user.id.readable = False
        grid2 = SQLFORM.grid(query=query2,
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

    grid1 = SQLFORM.grid(query=query1,
                        user_signature=False,
                        editable=False,
                        deletable=False,
                        details=False,
                        create=False,
                        links=[dict(
                                    header='Wybierz poradnie',
                                    body=lambda row: A('wybierz',
                                                       _href=URL(args=[row.id]))
                               ),
                               dict(
                                   header='Najbliższa wizyta',
                                   body=lambda row: A('szukaj',
                                                      _href=URL('szukaj', args=[row.id]))
                               )
                        ],
                        csv=False
    )
    #
    # if not request.args(0):
    #     db.department.id.readable = False
    #     grid1 = SQLFORM.grid(db.department.id == 0,
    #                          user_signature=False,
    #                          editable=False,
    #                          deletable=False,
    #                          details=False,
    #                          create=False,
    #                          links=[dict(
    #                              header='Wybierz poradnie',
    #                              body=lambda row: A('wybierz', _href=URL(args=[row.id]))
    #                          )],
    #                          csv=False
    #     )
    #
    #     grid2 = 'taf'
    return locals()


@auth.requires_membership('pacjent')
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

            rows = db((db.office_hours.id_doctor == request.args(1)) & (db.office_hours.week_day == day) & (
                db.office_hours.id_department == request.args(0))).select()
            #

            list_ = []
            for row in rows:
                list_.extend(create_hours(str(row.office_begin), str(row.office_end)))

            rows2 = db((db.visit.visit_day == str(date)) & (db.visit.id_doctor == request.args(1))).select()

            for row in rows2:
                if row.visit_hour in list_:
                    list_.remove(row.visit_hour)

            if len(list_):
                break

    else:


        for i in xrange(1, 500):
            date = datetime.date.today() + datetime.timedelta(days=i)
            day = map[date.strftime("%A")]

            rows = db((db.office_hours.week_day == day) & (
                db.office_hours.id_department == request.args(0))).select()
            #

            min_ = '20:00'
            d2 = ''
            for row in rows:
                doc_id = row.id_doctor
                list2 = (create_hours(str(row.office_begin), str(row.office_end)))

                rows2 = db((db.visit.visit_day == str(date)) & (db.visit.id_doctor == doc_id)).select()

                for row in rows2:
                    if row.visit_hour in list2:
                        list2.remove(row.visit_hour)


                if len(list2) and min_ > list2[0]:
                    drugi = doc_id
                    min_ = list2[0]

            if min_ != '20:00':
                break


    redirect(URL('nowa_wizyta', args=[request.args(0), drugi, date]))

@auth.requires_membership('pacjent')
def dodaj():
    if not session.visit:
        session.visit = []

    # session.visit.append((request.args(0), request.args(1), request.args(2), request.args(3) + ':' + request.args(4)))
    session.visit.append((request.args(0), request.args(1), request.args(2), request.args(3) + ':' + request.args(4), datetime.datetime.now()))

    redirect(URL('moje_wizyty'))

@auth.requires_membership('pacjent')
def zatwierdz():

    if request.args(0):
        try:
            db.visit.insert(id_patient=auth.user_id,
                        id_doctor=int(session.visit[int(request.args(0))][1]),
                        visit_day=session.visit[int(request.args(0))][2],
                        visit_hour=session.visit[int(request.args(0))][3]
                        )
            session.visit.remove(session.visit[int(request.args(0))])
        except:
            pass
            # return {"a": (type((session.visit[int(request.args(0))][1])), (session.visit[int(request.args(0))][1]).isdigit())}
            # return {["a" : (type(request.args(0)), request.args(0).isdigit())}

    redirect(URL('moje_wizyty'))
