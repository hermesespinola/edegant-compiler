from Symbol import Sym, SymEnum

class Token(object):
    def __init__(self, symbol: Sym, line: int, col: int):
        self.symbol = symbol
        self.line = line
        self.col = col

    def __repr__(self):
        return '[{} {}]:{}:{}'.format(repr(SymEnum(self.symbol.kind)), self.symbol.value, self.line, self.col)
