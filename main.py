import sys
from lexer import Lexer
from parser import Parser
import fileinput
from fileinput import FileInput

def main(file: FileInput):
    lexer = Lexer(file)
    tkns = lexer.get_tokens()
    print('Lista de tokens', tkns)
    parser = Parser(tkns, lexer.get_symtable())
    print('symbol table', parser.getFunctionsSymbolTable())
    print('syntax tree', parser.getSyntaxTree())
    print('correcto')

if __name__ == '__main__':
    main(fileinput.input())
    fileinput.close()
