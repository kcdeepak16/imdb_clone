"""
WSGI config for imdb_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

"""import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imdb_api.settings')

application = get_wsgi_application()"""

path = '/home/deepakkc007/imdb_api'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'imdb_api.settings'


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

