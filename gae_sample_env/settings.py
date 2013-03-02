import os
import jinja2

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

SITE_NAME = 'Google App Engine Sample Env'

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(PROJECT_PATH, 'templates')))
