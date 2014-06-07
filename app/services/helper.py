import json
import datetime
from google.appengine.ext.ndb import Key
from google.appengine.ext.ndb import Model


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int((obj - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
        if isinstance(obj, Key):
            return obj.urlsafe()
        if isinstance(obj, Model):
            return obj.to_dict()
        return None