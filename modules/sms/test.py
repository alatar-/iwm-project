#-*- coding: utf-8 -*-

import datetime

with open("/home/kam/web2py_test", "a") as f:
    f.write(datetime.datetime.now().isoformat())
    f.write("11111111")
    id_ = db(
        db.auth_user.email == "pacjent@ja.pl"
        ).select().first().id
    id_ = ''
    f.write("2222222")
    f.write(str(id_))
    f.write("\n   ")
