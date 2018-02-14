from lark import Lark, Transformer
from burnlight.program import Program, Transition, Loop

schedule_grammar = r"""
    ?start: program
    
    program: "{" [element ("," element)*] "}"
    
    ?element: transition
            | parameter
            | loop
    
    transition: "(" CNAME "," duration ")"
    parameter: name ":" string
    loop: "loop" number ":" program
    
    ?duration: number
    string: ESCAPED_STRING
    name: CNAME
    ?number: DECIMAL | INT
    
    %import common.ESCAPED_STRING
    %import common.CNAME
    %import common.DECIMAL
    %import common.INT
    %import common.WS
    
    %ignore WS
    """
from collections import namedtuple
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

    def duration(self, count):
        return float(count)

    def parameter(self, children):
        name, value = children
        return Parameter(name, value)

    def string(self, children):
        return children[0][1:-1]

    def name(self, children):
        return children[0][:]

    def number(self, count):
        return int(count)

test_program = """
{
    name: "A schedule",
    unit: "minute",

    (On, 10),
    (Off, 20),
    loop 3:
    {
        (On, 1),
        (Off, 2)
    }
}
"""

parser = Lark(schedule_grammar)
tree = parser.parse(test_program)
program = ProgramTransformer().transform(tree)
print(tree.pretty())
print(program)
for x in program.flatten():
    print(x)