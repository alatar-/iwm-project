#-*- coding: utf-8 -*-
import datetime
sms = local_import('sms')

m = sms.sms.Sms()

with open("/home/kam/web2py_test", "a") as f:
    date1 = (datetime.datetime.now().date() + datetime.timedelta(days=1)).isoformat()
    f.write(date1 + "\n")
    rows = db(
        (db.visit.visit_day == date1)
    ).select()
    for visit in rows:
        patient = db(
            (db.auth_user.id == visit.id_patient)
        ).select().first()
        m.send(patient['phone_number'], "Przypominamy o wizycie w dniu jutrzejszym o godzinie %s.".decode('utf-8') % visit['visit_hour'])
        f.write("\ttomorrow: %s\n" %  str(patient['phone_number']))

    date7 = (datetime.datetime.now().date() + datetime.timedelta(days=7)).isoformat()
    f.write(date7 + "\n")
    rows2 = db(
        (db.visit.visit_day == date7)
    ).select()
    for visit in rows2:
        patient = db(
            (db.auth_user.id == visit.id_patient)
        ).select().first()
        m.send(patient['phone_number'], "Przypominamy o wizycie w dniu %s o godzinie %s.".decode('utf-8') % (visit['visit_day'], visit['visit_hour']))
        f.write("\tweek: %s\n" %  str(patient['phone_number']))

    # return locals()
