import datetime
from flask.json import JSONEncoder, JSONDecoder
from block import Block
from scheduler import Schedule


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.timedelta):
            return {
                '__type__': 'timedelta',
                'days': obj.days,
                'seconds': obj.seconds,
                'microseconds': obj.microseconds,
                }

        elif isinstance(obj, Block):
            d = {
                '__type__': 'block',
                }
            d.update(obj.__dict__)
            return d

        elif isinstance(obj, Schedule):
            return {
                '__type__': '__schedule__',
                'block': obj.block,
                'running': obj.running,
                }

        else:
            JSONEncoder.default(self, obj)


class CustomJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('object_hook', self.object_hook)
        JSONDecoder.__init__(self, *args, **kwargs)

    def object_hook(self, d):
        if '__type__' not in d:
            return d

        object_type = d.pop('__type__')
        if object_type == 'timedelta':
            return datetime.timedelta(**d)

        elif object_type == 'block':
            try:
                duration = d.pop('duration')
            except KeyError:
                duration = datetime.timedelta(0)
            state = d.pop('state')
            iterations = d.pop('iterations')
            items = self.object_hook(d.pop('items'))
            return Block(state, duration, items, iterations)

        else:
            d['__type__'] = object_type
            return d
