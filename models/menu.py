response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

response.menu = []

if auth.user:
    if auth.has_membership(1):
        response.menu = [
            ('Umów wizytę', False, URL('pacjent', 'nowa_wizyta')),
            ('Moje wizyty', False, URL('pacjent', 'moje_wizyty')),
            ('Osoby kontaktowe', False, URL('pacjent', 'dane_kontaktowe')),
        ]
    elif auth.has_membership(2):
        response.menu = [
            ('Najbliższe wizyty', False, URL('lekarz', 'wizyty')),
            ('Plan pracy', False, URL('lekarz', 'plan'))
        ]
    elif auth.has_membership(3):
        response.menu = [
            ('Aktywacja', False, URL('admin', 'index')),
            ('Poradnie', False, URL('admin', 'poradnie')),
            ('Pacjenci', False, URL('admin', 'konta', args='pacjent')),
            ('Lekarze', False, URL('admin', 'konta', args='lekarz')),
            ('Admini', False, URL('admin', 'konta', args='admin'))
        ]
