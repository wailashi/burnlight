from lark import Lark, Transformer
from burnlight.program import Program, Transition, Loop
from datetime import timedelta
from collections import namedtuple

schedule_grammar = r"""
    ?start: program
    
    program: "{" [_element ("," _element)*] "}"
    
    _element: transition
            | loop
    
    transition: "(" CNAME "," duration ")"
    loop: "loop" INT ":" program
    
    ?duration: INT -> number
    
    %import common.CNAME
    %import common.INT
    %import common.WS
    
    %ignore WS
    """
Parameter = namedtuple('Parameter', 'name value')


class ProgramTransformer(Transformer):
    def program(self, children):
        params = {x.name: x.value for x in children if type(x) is Parameter}
        elements = [x for x in children if type(x) is not Parameter]
        return Program(elements=elements, parameters=params)

    def transition(self, children):
        state, duration = children
        return Transition(state, duration)

    def loop(self, children):
        iterations, program = children
        return Loop(iterations, program)

    def number(self, count):
        return timedelta(seconds=float(count[0]))

    def parameter(self, children):
        name, value = children
        return Parameter(name, value)

    def string(self, children):
        return children[0][1:-1]

    def CNAME(self, children):
        return children[0][1:-1]

test_program = """
{
    (On, 10),
    (Off, 20),
    loop 3:
    {
        (On, 1),
        (Off, 2)
    }
}
"""


def loadBSL(program):
    """Parses a Burnlight Scheduling Language string into a Program"""
    parser = Lark(schedule_grammar)
    return ProgramTransformer().transform(parser.parse(program))


if __name__ == '__main__':
    parser = Lark(schedule_grammar)
    tree = parser.parse(test_program)
    print(tree.pretty())
    program = ProgramTransformer().transform(tree)
    print(program)
