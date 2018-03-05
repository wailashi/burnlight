import bisect
import itertools
from datetime import timedelta


class Program:
    def __init__(self, elements=None, parameters=None):
        self.elements = elements
        self.parameters = parameters
        self.name = parameters.get('name')
        self.offset_memoize = None

    def flatten(self):
        for e in self.elements:
            if isinstance(e, (Loop, Program)):
                yield from e.flatten()
            else:
                yield e

    def offsets(self):
        if self.offset_memoize is None:
            offsets = list(itertools.accumulate((x.duration for x in self.flatten())))
            states = [x.state for x in self.flatten()]
            self.offset_memoize = (offsets, states)
        return self.offset_memoize

    def state_at_time(self, time):
        offsets, state = self.offsets()
        i = bisect.bisect(offsets, time)
        return state[i]

    def state_at(self, time):
        offsets = list(itertools.accumulate((x.length for x in self.elements)))
        index = bisect.bisect(offsets, time)
        offset = offsets[index]
        element = self.elements[index]
        return element.state_at(time - offset)


    @property
    def length(self):
        return sum((e.length for e in self.elements ), timedelta(0))

    def to_bsl(self):
        return '{' + ','.join((x.to_bsl() for x in self.elements)) + '}'

    def __repr__(self):
        return '<Program {}, {}>'.format(self.name, self.elements)


class Transition:
    def __init__(self, state, duration):
        self.state = state
        self.duration = duration

    def __repr__(self):
        return "<Transition {}, {}>".format(self.state, self.duration)

    def state_at(self, time):
        if time > self.duration:
            print('Time {} exceeds duration {}'.format(time, self.duration))
        return self.state

    @property
    def length(self):
        return self.duration

    def to_bsl(self):
        return '({},{})'.format(self.state, self.duration)


class Loop:
    def __init__(self, iterations, program):
        self.iterations = int(iterations)
        self.program = program

    def __iter__(self):
        for _ in range(self.iterations):
            yield from self.program

    def state_at(self, time):
        time = time % self.program.length
        offsets = list(itertools.accumulate((x.length for x in self.program.elements)))
        index = bisect.bisect(offsets, time)
        offset = offsets[index]
        element = self.program.elements[index]
        return element.state_at(time - offset)

    @property
    def length(self):
        return self.iterations * self.program.length

    def flatten(self):
        for _ in range(self.iterations):
            yield from self.program.flatten()

    def to_bsl(self):
        return 'loop {}:{}'.format(self.iterations, self.program.to_bsl())

    def __repr__(self):
        return '<Loop {}, {}>'.format(self.iterations, self.program)
