import keywords
from Symbol import Sym, ID
from pprint import pprint

class SymbolTable(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.identifiers = {}

    def lookup(self, value):
        tkn = self.identifiers.get(value)
        if tkn is not None:
            return tkn
        kwd = keywords.__all__.get(value)
        if kwd is not None:
            return kwd
        new_tkn = self.identifiers[value] = Sym(ID, value)
        return new_tkn

    def get_identifiers(self):
        return self.identifiers.keys()

    def get_symbols(self):
        return self.identifiers.values()

    def print_table(self):
        print(self.identifiers)
    
    def __repr__(self):
        return self.filename + 'symtable: ' + self.identifiers.__str__()
