import json
import datetime


class Block(object):

    def __init__(self, state, duration=0, items=None, iterations=1):
        self.iterations = iterations
        self.state = state
        self.duration = duration
        if items is None:
            self.items = []
        else:
            self.items = items

    def __iter__(self):
        for i in range(self.iterations):
            for item in self.items:
                yield item

    def __repr__(self):
        return "<block, %s>" % self.state

    def add(self, item):
        self.items.append(item)
        return self

    def structure(self):
        yield [0, self]
        for item in self.items:
            if item.items:
                for sub in item.structure():
                    sub[0] += 1
                    yield sub
            else:
                yield [1, item]

    def traverse(self):
        for item in self:
            if item.items:
                for sub in item.traverse():
                    yield sub
            else:
                yield item

    def print_structure(self):
        for indent, block in self.structure():
            output = ""
            output += '   ' * indent + '|-- '
            if block.items:
                output += "Loop %s times" % block.iterations
            else:
                output += "Turn %s for %s" % (block.state, block.duration)
            print(output)

    def trigger(self):
        print self.state

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class BlockJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.timedelta):
            return {
                '__type__' : 'timedelta',
                'days' : obj.days,
                'seconds' : obj.seconds,
                'microseconds' : obj.microseconds,
                }

        elif isinstance(obj, Block):
            d = {
                '__type__' : 'block',
                }
            d.update(obj.__dict__)
            return d

class BlockJSONDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        if type == 'timedelta':
            return datetime.timedelta(**d)

        elif type == 'block':
            duration = d.pop('duration')
            state = d.pop('state')
            iterations = d.pop('iterations')
            items = self.dict_to_object(d.pop('items'))
            return Block(state, duration, items, iterations)

        else:
            d['__type__'] = type
            return d


root = Block('root')
root.add(Block('1', duration=datetime.timedelta(seconds=3)))
loop = Block('loop')
loop.add(Block('2', duration=datetime.timedelta(seconds=3)))
loop.add(Block('3', duration=datetime.timedelta(seconds=3)))
loop.iterations = 3
inner_loop = Block('inner loop')
inner_loop.add(Block('4', duration=datetime.timedelta(seconds=3)))
loop.add(inner_loop)
root.add(loop)
