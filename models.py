from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

ITEMS = 10


class TestModelPag(ndb.Model):
    number = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def cursor_pagination(cls, prev_cursor_str, next_cursor_str, direction):
        if not direction:
            objects, next_cursor, more = cls.query().order(cls.number).fetch_page(ITEMS)
            prev_cursor_str = ''
            next_cursor_str = next_cursor.urlsafe()
            prev = False
            next_ = True if more else False
        elif direction == 'fwd' and next_cursor_str:
            cursor = Cursor(urlsafe=next_cursor_str)
            objects, next_cursor, more = cls.query().order(cls.number).fetch_page(ITEMS, start_cursor=cursor)
            prev_cursor_str = cursor.urlsafe()
            next_cursor_str = next_cursor.urlsafe()
            prev = True if prev_cursor_str else False
            next_ = True if more else False
        elif direction == 'bwd':
            cursor = Cursor(urlsafe=prev_cursor_str)
            objects, next_cursor, more = cls.query().order(-cls.number).fetch_page(ITEMS, start_cursor=cursor)
            objects.reverse()
            next_cursor_str = cursor.urlsafe()
            prev_cursor_str = next_cursor.urlsafe()
            next_ = True if prev_cursor_str else False
            prev = True if more else False

        return {'objects': objects, 'next_cursor': next_cursor_str, 'prev_cursor': prev_cursor_str, 'prev': prev,
                'next': next_}

    @classmethod
    def offset_pagination(cls, offset):
        """Pagination through query offset"""

        if offset:
            try:
                offset = int(offset)
            except ValueError:
                offset = 0
        objects, next_cursor, more = cls.query().order(cls.number).fetch_page(ITEMS, offset=offset)
        prev_offset = max(offset - ITEMS, 0)
        prev = True if offset else False
        next_ = True if more else False
        next_offset = ''
        if next_:
            next_offset = offset + ITEMS
        return {'objects': objects, 'prev': prev, 'next': next_, 'prev_offset': prev_offset, 'next_offset': next_offset}

