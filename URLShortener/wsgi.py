"""
WSGI config for URLShortener project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import sys
reload(sys)     
sys.setdefaultencoding("utf-8")
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "URLShortener.settings")

application = get_wsgi_application()

from dj_static import Cling
application = get_wsgi_application()


application = Cling(get_wsgi_application())