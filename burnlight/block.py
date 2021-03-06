import datetime
import itertools
import bisect


class Block:

    def __init__(self, state, duration=datetime.timedelta(0), items=None, iterations=1):
        self.iterations = iterations
        self.state = state
        self.duration = duration
        if items is None:
            self.items = []
        else:
            self.items = items

    def __iter__(self):
        for _ in range(self.iterations):
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

    def offsets(self):
        offsets = itertools.accumulate((x.duration for x in self.traverse()))
        states = (x.state for x in self.traverse())
        return zip(offsets, states)

    def state_at_time(self, time):
        offsets, state = zip(*self.offsets())
        i = bisect.bisect(offsets, time)
        return state[i]

    @property
    def length(self):
        length = datetime.timedelta(0)
        for each in self.items:
            length += each.length
        length *= self.iterations
        return length + self.duration

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
        print(self.state)


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
