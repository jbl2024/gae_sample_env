import logging
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import webapp
import settings
import webapp2

def default_context():
    data = {
        "title": settings.SITE_NAME,
    }

    user = users.get_current_user()
    if user is not None:
        data["user"] = user
        data["logout_url"] = users.create_logout_url("/")
        data["admin"] = users.is_current_user_admin()

    return data


class BaseHandler(webapp2.RequestHandler):

    def render(self, context, template_name):
        template = settings.template_env.get_template(template_name)
        self.response.out.write(template.render(context))

    def retrieve(self, key):
        """ Helper for loading data from memcache """
        all_pages = memcache.get("__all_pages__")
        if all_pages is None:
            all_pages = {}

        item = memcache.get(key) if key in all_pages else None

        if item is not None:
            return item
        else:
            item = self.data()
            if not memcache.set(key, item):
                logging.error("Memcache set failed on %s" % key)
            else:
                all_pages[key] = 1
                if not memcache.set("__all_pages__", all_pages):
                    logging.error("Memcache set failed on __all_pages__")
        return item

    def not_found(self):
        self.error(404)
        self.render(default_context(), "404.html")


class NotFoundHandler(BaseHandler):

    def get(self):
        self.error(404)
        self.render(default_context(), "404.html")


class UnauthorizedHandler(webapp.RequestHandler):
    def get(self):
        self.error(403)
        self.render(default_context(), "403.html")


class RootHandler(BaseHandler):

    def get(self):
        context = default_context()
        self.render(context, 'index.html')
