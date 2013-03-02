import webapp2

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import site, api, admin

API = [
    # (r'/api/.*', api.NotFoundHandler),
    ]

SITE = [
    (r'/*$', site.RootHandler),
    (r'/403.html', site.UnauthorizedHandler),
    (r'/404.html', site.NotFoundHandler),
    ]

ADMIN = [
    # (r'/admin', admin.RootHandler),
    ]

ROUTES = []
ROUTES.extend(SITE)
ROUTES.extend(ADMIN)
ROUTES.append((r'/.*$', site.NotFoundHandler))

app = webapp2.WSGIApplication(ROUTES, debug=True)
