#!/usr/bin/env python

from smsapi.client import SmsAPI
from smsapi.responses import ApiError

class Carrier:
    def __init__(self, username, password):
        self.api = SmsAPI()
        self.api.set_username(username)
        self.api.set_password(password)

class Sms:
    def __init__(self):
        self.carrier = Carrier("pat.karolak@gmail.com", "smsiwm2014")
    
    def send(self, reciever, message):
        try:
            self.carrier.api.service('sms').action('send')
            self.carrier.api.set_to(reciever)
            self.carrier.api.set_content(message.encode('utf-8'))
            # self.carrier.api.set_params(*self.params)
            status = self.carrier.api.execute()
            for s in status:
                print s.id, s.points, s.status
        except ApiError, e:
            print '%s - %s' % (e.code, e.message)
