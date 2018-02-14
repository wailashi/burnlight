from collections import Iterable

class Program:
    def __init__(self, elements=None, parameters=None):
        self.elements = elements
        self.parameters = parameters
        self.name = parameters.get('name')

    def flatten(self):
        for e in self.elements:
            if isinstance(e, (Loop, Program)):
                yield from e.flatten()
            else:
                yield e

    def __repr__(self):
        return f'<Program {self.name}, {self.elements}>'


class Transition:
    def __init__(self, state, duration):
        self.state = state
        self.duration = duration

    def __repr__(self):
        return f"<Transition {self.state}, {self.duration}>"


class Loop:
    def __init__(self, iterations, program):
        self.iterations = int(iterations)
        self.program = program

    def __iter__(self):
        for _ in range(self.iterations):
            yield from self.program

    def flatten(self):
        for _ in range(self.iterations):
            yield from self.program.flatten()

    def __repr__(self):
        return f"<Loop {self.iterations}, {self.program}>"
