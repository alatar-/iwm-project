# -*- coding: utf-8 -*-

from gluon.tools import Auth, Crud, Service, PluginManager, Mail, prettydate

db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
response.generic_patterns = ['*'] if request.is_local else []
response.optimize_css = 'concat,minify,inline'
response.optimize_js = 'concat,minify,inline'
response.static_version = '1.0.0'

auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

ISO_GENDER = ['mężczyzna', 'kobieta', 'nieznana', 'nie dotyczy']

# ----------
patient_extra_fields = [
    Field('pesel', length=16), #, requires=[IS_NOT_EMPTY(), IS_LENGTH(11, 11, error_message='pesel ma długość 11!')]),
    Field('address', length=128), #, requires=[IS_NOT_EMPTY()]),
    Field('city', length=128), #, requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC(error_message='tylko znaki alfanumeryczne!')]),
    Field('zip', length=8),#, requires=[IS_NOT_EMPTY(), IS_MATCH('^\d{2}-\d{3}?$', error_message='błędny kod pocztowy')]),
    Field('gender', length=20),#, requires=[IS_IN_SET(ISO_GENDER)]),
    Field('born_city', length=128),#, requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC(error_message='tylko znaki alfanumeryczne!')]),
    Field('identity_id', length=9),#, requires=[IS_NOT_EMPTY(), IS_MATCH('^[A-Z]{3}\d{6}?$', error_message='błędny number dowodu')]),
    Field('nip', length=13),#, requires=[IS_MATCH('^\d{3}-\d{3}-\d{2}-\d{2}?$', error_message='błędny number nip')]),
    Field('phone_number', length=15),#, requires=[IS_NOT_EMPTY(), IS_MATCH('^\d{11}?$', error_message='błędny number telefonu')]),
    Field('nn_patient', 'boolean')
    # dane kontaktowe, osobna tabela
]

doctor_extra_fields = [
    Field('PWZ', 'integer', length=7, requires=[IS_NOT_EMPTY(), IS_LENGTH(7, 7, error_message='długość pwz wynosi 7')])
]

auth.settings.extra_fields['auth_user'] = ([
    # Field('username', length=36, requires=IS_NOT_EMPTY()),
    # Field('first_name', length=36,
    # Field('last_name', length=36, requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
    Field('user_type', requires=IS_IN_SET(['pacjent', 'lekarz', 'admin']))] +
    patient_extra_fields +
    doctor_extra_fields
)
auth.define_tables(username=False, signature=False)

db.auth_user.pesel.label = T('Pesel')
db.auth_user.address.label = T('Adres')
db.auth_user.city.label = T('Miasto')
db.auth_user.zip.label = T('Kod pocztowy')
db.auth_user.gender.label = T('Płeć')
db.auth_user.born_city.label = T('Miejsce urodzenia')
db.auth_user.identity_id.label = T('Nr dowodu')
db.auth_user.phone_number.label = T('Telefon')
db.auth_user.nn_patient.label = T('Pancjent-NN')
#db.auth_user.first_name.requires=[IS_NOT_EMPTY(), IS_MATCH('^[A-Z][a-z]*$', error_message='jedno słowo, z dużej litery, alfanumeryczne')]
#db.auth_user.last_name.requires=[IS_NOT_EMPTY(), IS_MATCH('^[A-Z][A-z\-]*$', error_message='jedno słowo, z dużej litery, alfanumeryczne')]
#db.auth_user.pesel.requires.append(IS_NOT_IN_DB(db, db.auth_user.pesel))

auth.settings.create_user_groups = False
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

##################################################################
def create_hours(start, end):
    list = []
    # start = int(start[:2])
    # end = int(end[:2])
    # start = start.zfill(5)
    # end = end.zfill(5)
    while start < end :
        list.append(start)

        if start[3:5] == '30':
            start = str(int(start[0:2]) + 1) + ":00"
        else:
            start = start[0:2] + ":30"
    return list

db.define_table('contacts',
    Field('id_patient', 'reference auth_user'),
    Field('name', length=30), #, requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC(error_message='tylko znaki alfanumeryczne!')]),
    Field('surname', length=30), #, requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC(error_message='tylko znaki alfanumeryczne!')]),
    Field('phone_numer', length=15) #, requires=[IS_NOT_EMPTY(), IS_MATCH('^\d{11}?$', error_message='błędny number telefonu')]),
)
db.contacts.id_patient.label = T('Id pacjenta')
db.contacts.name.label = T('Imię')
db.contacts.surname.label = T('Nazwisko')
db.contacts.phone_numer.label = T('Telefon')


db.define_table('department',
    Field('name', requires=[IS_NOT_EMPTY()]),
    format='%(name)s'
)
db.department.name.requires.append(IS_NOT_IN_DB(db, db.department.name))

db.define_table('office_hours',
    Field('week_day', requires=IS_IN_SET(['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'])),
    Field('office_begin', length=5, requires=IS_IN_SET(create_hours('09:00', '12:00'))),
    Field('office_end', length=5, requires=IS_IN_SET(create_hours('09:00', '12:00'))),
    Field('id_doctor', 'reference auth_user'),
    Field('id_department', 'reference department')
)

db.office_hours.week_day.label = T('Dzień tygodnia')
db.office_hours.office_begin.label = T('Przyjmuje od')
db.office_hours.office_end.label = T('Przyjmuje do')
db.office_hours.id_doctor.label = T('Lekarz')
db.office_hours.id_department.label = T('Oddział')

db.define_table(
    'drug',
    Field('name'),
    Field('ingredients'),
    Field('form'),
    Field('dose'),
    Field('package_size'),
    Field('availability'),
    Field('ean'),
    Field('mah'),
    Field('authorization_number'),
    Field('producer'),
    Field('origin_country'),
    format = '%(name)s %(form)s %(dose)s'
) 
db.drug.name.label=T('Nazwa')
db.drug.ingredients.label=T('Składniki')
db.drug.form.label=T('Forma')
db.drug.dose.label=T('Dawka')
db.drug.package_size.label=T('Rozmiar opakowania')
db.drug.availability.label=T('Dostępność')
db.drug.ean.label=T('Kod EAN')
db.drug.mah.label=T('Mah')
db.drug.authorization_number.label=T('Nr pozwolenia')
db.drug.producer.label=T('Producent')
db.drug.origin_country.label=T('Kraj pochodzenia')


db.define_table(
    'med_procedure',
    Field('category', unique=True),
    Field('title'),
    format = '%(category)s %(title)s'
) 


db.define_table('visit',
    Field('id_patient', 'reference auth_user'),
    Field('id_doctor', 'reference auth_user'),
    Field('visit_day', 'date', requires=IS_NOT_EMPTY()),
    Field('visit_hour', length=5, requires=IS_NOT_EMPTY()),
    Field('reason'),
    Field('description', 'text', length=1000),
    Field('treatment', 'text', length=2000),
    Field('med_procedures', 'list:reference med_procedure'),
    Field('drugs', 'list:reference drug')
)
db.visit.drugs.widget = SQLFORM.widgets.multiple.widget
db.visit.med_procedures.widget = SQLFORM.widgets.multiple.widget

db.visit.id_patient.label = T('Pacjent')
db.visit.id_doctor.label = T('Lekarz')
db.visit.visit_day.label = T('Dzień wizyty')
db.visit.visit_hour.label = T('Godzina')
db.visit.reason.label = T('Powód wizyty')
db.visit.description.label = T('Opis przypadku')
db.visit.treatment.label = T('Zalecenia lekarskie')
db.visit.med_procedures.label = T('Procedury ICD-9')
db.visit.drugs.label = T('Zalecone leki')

db.define_table(
    'powiadomienia',
    Field('godzina'),# length=5, requires=[IS_NOT_EMPTY(), IS_MATCH('^\d{2}:\d{2}?$', error_message='błędny kod pocztowy')]),
    Field('wyprzedzenie', 'integer'),# length=2, requires=[IS_NOT_EMPTY()]),
    Field('status', 'integer'),
) 

# db.children.department.requires = IS_IN_DB(db, db.parent.id, '%(name)s')

# db.office_hours.office_end.requires.append()
# db.office_hours.office_end.requires.append(IS_NOT_IN_DB(db, db.office_hours.office_end))

###########################################################


mail = Mail()
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login
auth.settings.mailer = mail

## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield

##########################################################

def remove_extra_fields(type):
    rem_fields = {
        'pacjent': doctor_extra_fields + [db.auth_user.user_type],
        'lekarz': patient_extra_fields + [db.auth_user.user_type],
        'admin': patient_extra_fields + doctor_extra_fields + [db.auth_user.user_type]
    }
    for field in rem_fields[type]:
        field.readable = field.writable = False

auth.settings.login_next = URL('index')
auth.settings.register_next = URL('user', args='login')
auth.settings.register_onaccept.append(lambda form: auth.add_membership('pacjent', db(db.auth_user.email == form.vars.email).select().first().id))
