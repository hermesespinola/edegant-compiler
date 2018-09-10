import sys
from lexer import Lexer
import fileinput
from fileinput import FileInput
from pprint import pprint

def main(file: FileInput):
    lexer = Lexer(file)
    tkns = lexer.get_tokens()
    pprint(tkns)
    pprint(lexer.get_symtable())

if __name__ == '__main__':
    main(fileinput.input())
    fileinput.close()
