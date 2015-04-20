
import os

import webapp2
import jinja2
from google.appengine.ext import ndb

from models import TestModelPag

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class CreateHandler(webapp2.RequestHandler):
    """Create items which we will use for pagination"""

    def get(self):
        entities = []
        for i in range(100):
            tm = TestModelPag(number=i)
            entities.append(tm)
        ndb.put_multi(entities)
        self.response.write('Done!!!')


class CursorPaginationHandler(webapp2.RequestHandler):
    """Display objects with cursor pagination"""

    def get(self):
        direction = self.request.get('direction', '')
        prev_cursor = self.request.get('prev_cursor', '')
        next_cursor = self.request.get('next_cursor', '')
        res = TestModelPag.cursor_pagination(prev_cursor, next_cursor, direction)
        template = JINJA_ENVIRONMENT.get_template('templates/cursor_pagination.html')
        self.response.write(template.render(res))


class OffsetPaginationHandler(webapp2.RequestHandler):
    """Display through query offset"""

    def get(self):
        offset = self.request.get('offset', '0')
        res = TestModelPag.offset_pagination(offset)
        template = JINJA_ENVIRONMENT.get_template('templates/offset_pagination.html')
        self.response.write(template.render(res))

app = webapp2.WSGIApplication([
    ('/create', CreateHandler),
    ('/cursor_pagination', CursorPaginationHandler),
    ('/offset_pagination', OffsetPaginationHandler),
], debug=True)
