PRINCIPAL = 0
REGRESA = 1
SI = 2
MIENTRAS = 3
ENTERO = 4
REAL = 5
LOGICO = 6
VERDADERO = 7
FALSO = 8
PLUS = 9
MINUS = 10
TIMES = 11
DIV = 12
POWER = 13
GT = 14
LT = 15
EQ = 16
AND = 17
OR = 18
NOT = 19
ASS = 20
COMMA = 21
SEMMI = 22
LEFT_PAR = 23
RIGHT_PAR = 24
LEFT_CURL = 25
RIGHT_CURL = 26
ID = 27
NUM = 28

DATA_TYPES = { ENTERO, REAL, LOGICO }
ARITHMETIC_OPERATORS = { PLUS, MINUS, TIMES, DIV, POWER }
BOOLEAN_OPERATORS = { OR, AND } # only binary
COMPARISON_OPERATORS = { GT, LT, EQ }
OPERATORS = ARITHMETIC_OPERATORS.union(BOOLEAN_OPERATORS).union(COMPARISON_OPERATORS)
STATEMENTS = { MIENTRAS, SI, ID }

BOOLEAN_LITERALS = { VERDADERO, FALSO }
LITERALS = { NUM }.union(BOOLEAN_LITERALS)

from enum import Enum
class SymEnum(Enum):
    PRINCIPAL = 0
    REGRESA = 1
    SI = 2
    MIENTRAS = 3
    ENTERO = 4
    REAL = 5
    LOGICO = 6
    VERDADERO = 7
    FALSO = 8
    PLUS = 9
    MINUS = 10
    TIMES = 11
    DIV = 12
    POWER = 13
    GT = 14
    LT = 15
    EQ = 16
    AND = 17
    OR = 18
    NOT = 19
    ASS = 20
    COMMA = 21
    SEMMI = 22
    LEFT_PAR = 23
    RIGHT_PAR = 24
    LEFT_CURL = 25
    RIGHT_CURL = 26
    ID = 27
    NUM = 28

class Sym(object):
    def __init__(self, kind: int, value: str):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return repr(SymEnum(self.kind))
