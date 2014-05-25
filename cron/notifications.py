#-*- coding: utf-8 -*-
import datetime
sms = local_import('sms')

m = sms.sms.Sms()

with open("/home/kam/web2py_test", "a") as f:
    notifications = db(db.powiadomienia).select()

    for notification in notifications:
        now = datetime.datetime.now().hour * 100 + datetime.datetime.now().minute
        then = int(notification['godzina'][0:2]) * 100 + int(notification['godzina'][3:5])

        if now >= then:
            if not notification['status']: 
                date1 = (datetime.datetime.now().date() + datetime.timedelta(days=notification['wyprzedzenie'])).isoformat()
                f.write(date1 + "\n")
                rows = db(
                    (db.visit.visit_day == date1)
                ).select()
                for visit in rows:
                    patient = db(
                        (db.auth_user.id == visit.id_patient)
                    ).select().first()
                    m.send(patient['phone_number'], "Przypominamy o wizycie w dniu jutrzejszym o godzinie %s.".decode('utf-8') % visit['visit_hour'])
                    f.write("\t%s\n" %  str(patient['phone_number']))

                notification.update_record(status=1)
        else:
                notification.update_record(status=0)
