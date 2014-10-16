"""
WSGI config for myhouserent project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhouserent.settings")
os.environ.setdefault("ALLOWED_INCLUDE_ROOTS", "myhouserent.settings")
#''' RunLocaly Comment and  Uncomment Run Heroku(Do not change this comment line)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

'''

#To run on local machine just comment below line and un comment above two lines

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
#'''