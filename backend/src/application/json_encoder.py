import enum
from datetime import time

from flask import json
from sqlalchemy.ext.declarative import DeclarativeMeta


# Copied from http://stackoverflow.com/a/31569287/1508881
class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            data = {}
            fields = o.__json__() if hasattr(o, '__json__') else dir(o)
            for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
                value = o.__getattribute__(field)
                try:
                    json.dumps(value)
                    data[field] = value
                except TypeError:
                    data[field] = None
            return data

        elif isinstance(o, enum.Enum):
            return o.value

        elif isinstance(o, time):
            return o.strftime('%H:%M')

        return json.JSONEncoder.default(self, o)
