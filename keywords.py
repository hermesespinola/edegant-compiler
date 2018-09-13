from Symbol import *
from typing import Dict

statements = {
    'principal': Sym(PRINCIPAL, 'principal'),
    'regresa': Sym(REGRESA, 'regresa'),
    'si': Sym(SI, 'si'),
    'mientras': Sym(MIENTRAS, 'mientras')
}
data_types = {
    'entero': Sym(ENTERO, 'entero'),
    'real': Sym(REAL, 'real'),
    'logico': Sym(LOGICO, 'logico')
}
booleans = {
    'verdadero': Sym(VERDADERO, 'verdadero'),
    'falso': Sym(FALSO, 'false')
}
arithmetic_ops = {
    '+': Sym(PLUS, '+'),
    '-': Sym(MINUS, '-'),
    '*': Sym(TIMES, '*'),
    '/': Sym(DIV, '/'),
    '^': Sym(POWER, '^')
}
relational_ops = {
    '>': Sym(GT, '>'),
    '<': Sym(LT, '<'),
    '==': Sym(EQ, '==')
}
boolean_ops = {
    '&': Sym(AND, '&'),
    '|': Sym(OR, '|'),
    '!': Sym(NOT, '!')
}
assignment = {
    '=': Sym(ASS, '=')
}
punctuation = {
    ',': Sym(COMMA, ','),
    ';': Sym(SEMMI, ';'),
    '(': Sym(LEFT_PAR, '('),
    ')': Sym(RIGHT_PAR, ')'),
    '{': Sym(LEFT_CURL, '{'),
    '}': Sym(RIGHT_CURL, '}')
}

KeywordType = Dict[str, Sym]
not_ids = statements.copy()
not_ids.update(data_types)
not_ids.update(booleans)
__all__ = not_ids.copy()
__all__.update(arithmetic_ops)
__all__.update(relational_ops)
__all__.update(boolean_ops)
__all__.update(assignment)
__all__.update(punctuation)
