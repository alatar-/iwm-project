from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Medibox'
settings.subtitle = 'system e-rejestracji'
settings.author = 'Kam & Pat'
settings.author_email = 'you@example.com'
settings.keywords = 'medibox, system, rejestracja, e-rejestracja'
settings.description = 'medibox'
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '393e0957-ed87-453f-a0dc-de0fe87cea24'
settings.email_server = 'smtp.gmail.com:587'
settings.email_sender = 'medibox@medibox.com'
settings.email_login = 'calendar0017@gmail.com:#calendar0017'
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []


