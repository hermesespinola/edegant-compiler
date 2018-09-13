from FuncSymTable import FunctionSymbolTable
from token import Token
from Symbol import *
from typing import Tuple, Dict
from syntax_tree import *
from keywords import data_types

def throwSyntaxError(msg):
    print(msg)
    print('incorrecto')
    exit()

def check_id(token: Token, dtype: int):
    if token.symbol.kind is not ID:
        value = token.symbol.value
        throwSyntaxError('Esperaba identificador pero se encontró: {} en linea {}, columna {} '.format(value, token.line, token.col))
    else:
        token.dtype = dtype

def check_token_type(token: Token, keyword_type) -> int:
    if token.symbol.value not in keyword_type:
        value = token.symbol.value
        throwSyntaxError('Esperaba un tipo de dato pero se encontró {} en linea {}, columna {}'.format(value, token.line, token.col))
    return token.symbol.kind

def check_token(token: Token, kind: int):
    if token.symbol.kind is not kind:
        throwSyntaxError('Esperaba {} pero se encontró {} en linea {}, columna {}'.format(SymEnum(kind).name, token.symbol.value, token.line, token.col))

def arg_def(start: int, tokens: list, func_symtable: FunctionSymbolTable) -> Tuple[int, DeclarationsNode]:
    i = start
    args_tree = []
    while tokens[i].symbol.kind is not RIGHT_PAR:
        dtype = check_token_type(tokens[i], data_types)
        check_id(tokens[i+1], dtype)
        func_symtable.put(tokens[i+1])
        args_tree.append(DeclarationNode(dtype, tokens[i+1]))
        if tokens[i+2].symbol.kind is RIGHT_PAR:
            return i + 2, DeclarationsNode(args_tree)
        check_token(tokens[i+2], COMMA)
        check_token_type(tokens[i+3], data_types)
        i += 3
    return i, DeclarationsNode(args_tree)

def parameters(start: int, tokens: List[Token], func_symtable: FunctionSymbolTable) -> Tuple[int, ParametersNode]:
    i = start
    parameters_tree = []
    while tokens[i].symbol.kind is not RIGHT_PAR:
        check_id(tokens[i], ID)
        token = func_symtable.get_token(tokens[i].symbol.value)
        dtype = None if token is None else token.dtype
        parameters_tree.append(IdNode(dtype, token.symbol.value))
        if tokens[i+1].symbol.kind is RIGHT_PAR:
            return i + 1, ParametersNode(parameters_tree)
        check_token(tokens[i+1], COMMA)
        check_token(tokens[i+2], ID)
        i += 2
    return i, ParametersNode(parameters_tree)

# Expression can be any of: literal (NUM or BOOL), id, function call, binary expression
def expression(start: int, tokens: List[Token], func_symtable: FunctionSymbolTable) -> Tuple[int, ExpressionNode]:
    i = start
    previous = None
    stack = []
    while tokens[i] is not SEMMI:
        # first construct literals, ids and function call tokens
        sym = tokens[i].symbol
        if sym.kind in LITERALS:
            # Check previous node is ok
            if previous is not None and (previous is not LEFT_PAR and previous not in OPERATORS):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            stack.append(tokens[i])
        elif sym.kind is ID:
            nextKind = tokens[i+1].symbol.kind
            if previous is not None and (previous is not LEFT_PAR and previous not in OPERATORS):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            if nextKind is LEFT_PAR:
                # Create function call node with parameters
                i, parameters_node = parameters(i + 2, tokens, func_symtable)
                check_token(tokens[i], RIGHT_PAR)
                stack.append(FuncCallNode(sym.value, parameters_node))
            else:
                token = func_symtable.get_token(sym.value)
                dtype = None if token is None else token.dtype
                stack.append(IdNode(dtype, sym.value))
        elif sym.kind in OPERATORS:
            if previous is None or (previous not in LITERALS and previous is not ID and previous is not RIGHT_PAR):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            stack.append(tokens[i])
        elif sym.kind is LEFT_PAR:
            if previous is not None and (previous is not LEFT_PAR and previous not in OPERATORS):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            stack.append(tokens[i])
        elif sym.kind is RIGHT_PAR:
            if previous is None or (previous not in LITERALS and previous is not ID and previous is not RIGHT_PAR):
                throwSyntaxError('Sintaxis invalida en linea {}, columna {}'.format(tokens[i].line, tokens[i].col))
            nested_expr = []
            x = stack.pop()
            while x.symbol.kind is not LEFT_PAR if type(x) is Token else True:
                nested_expr.append(x)
                if len(stack) == 0:
                    throwSyntaxError('Sintaxis invalida: falta parentesis izquierdo')
                x = stack.pop()
            stack.append(nested_expr)
        elif sym.kind is SEMMI:
            break
        else:
            throwSyntaxError('Sintaxis invalida: {} en linea {}, columna {}'.format(tokens[i].symbol.value, tokens[i].line, tokens[i].col))
        previous = sym.kind
        i += 1

    # Check balanced parenthesis
    for item in stack:
        if type(item) is Token and item.symbol.kind is LEFT_PAR:
            throwSyntaxError('Sintaxis invalida: parentesis no balanceados en linea {}, columna {}'.format(item.symbol.value, item.line, item.col))

    # TODO: parse intermediate stack to prefix expression
    expression_node = stack
    check_token(tokens[i], SEMMI)
    return i, expression_node

def ass_statement(start: int, tokens: List[Token], func_symtable: FunctionSymbolTable) -> Tuple[int, AssNode]:
    # Check assignment syntax
    check_token(tokens[start], ID)
    left = func_symtable.get_token(tokens[start+4])
    l_dtype = None if left is None else left.dtype
    id_node = IdNode(l_dtype, tokens[start].symbol.value)
    check_token(tokens[start+1], ASS)
    # first check for negation, only identifiers, no function calls
    if tokens[start+2].symbol.kind is NOT:
        check_token(tokens[start+3], ID)
        check_token(tokens[start+4], SEMMI)
        token = func_symtable.get_token(tokens[start+3])
        dtype = None if token is None else token.dtype
        rightNode = IdNode(dtype, tokens[start+3].symbol.value)
        return start+4, AssNode(id_node, UnaryExpressionNode(LOGICO, NOT, rightNode))

    i, expression_node = expression(start + 2, tokens, func_symtable)
    return i, AssNode(id_node, expression_node)

def if_statement(start: int, tokens: List[Token], func_symtable: FunctionSymbolTable) -> Tuple[int, IfNode]:
    # Check si syntax
    check_token(tokens[start], SI)
    check_token(tokens[start+1], LEFT_PAR)
    check_token(tokens[start+2], ID)
    # put if boolean datatype, leave this for later semantic check.
    token = func_symtable.get_token(tokens[start+2])
    id_node = IdNode(None if token is None else token.dtype, tokens[start+2].symbol.value)
    check_token(tokens[start+3], RIGHT_PAR)
    check_token(tokens[start+4], LEFT_CURL)
    i = start + 5
    statement_nodes = []
    while tokens[i].symbol.kind is not RIGHT_CURL:
        i, statement_node = statement(i, tokens, func_symtable)
        statement_nodes.append(statement_node)
        i += 1
    return i, IfNode(id_node, statement_nodes)

def while_statement(start: int, tokens: List[Token], func_symtable: FunctionSymbolTable) -> Tuple[int, WhileNode]:
    # Check while syntax
    check_token(tokens[start], MIENTRAS)
    check_token(tokens[start+1], LEFT_PAR)
    check_token(tokens[start+2], ID)
    # put if boolean datatype, leave this for later semantic check.
    token = func_symtable.get_token(tokens[start+2])
    id_node = IdNode(None if token is None else token.dtype, tokens[start+2].symbol.value)
    check_token(tokens[start+3], RIGHT_PAR)
    check_token(tokens[start+4], LEFT_CURL)
    i = start + 5
    statement_nodes = []
    while tokens[i].symbol.kind is not RIGHT_CURL:
        i, statement_node = statement(i, tokens, func_symtable)
        statement_nodes.append(statement_node)
        i += 1
    return i, WhileNode(id_node, statement_nodes)

def statement(start: int, tokens: List[Token], func_symtable: FunctionSymbolTable) -> Tuple[int, StatementNode]:
    if tokens[start].symbol.kind is SI:
        i, if_node = if_statement(start, tokens, func_symtable)
        return i, if_node
    if tokens[start].symbol.kind is MIENTRAS:
        i, while_node = while_statement(start, tokens, func_symtable)
        return i, while_node
    if tokens[start].symbol.kind is ID:
        i, ass_node = ass_statement(start, tokens, func_symtable)
        return i, ass_node
    else:
        throwSyntaxError('Esperaba una sentencia si, mientras o asignación, pero se encontró {}, linea {}, columna {}'.format(tokens[start].symbol.value, tokens[start].line, tokens[start].col))

# TODO: Identify function calls
def func_body(start: int, tokens: List[Token], func_symtable: FunctionSymbolTable) -> Tuple[int, BodyNode]:
    i = start
    statements = []
    while tokens[i].symbol.kind in STATEMENTS:
        i, statement_node = statement(i, tokens, func_symtable)
        statements.append(statement_node)
        i += 1
    return i, BodyNode(statements)


def func_declarations(start: int, tokens: List[Token], func_symtable: FunctionSymbolTable) -> Tuple[int, DeclarationsNode]:
    i = start
    declarations_tree = []
    while tokens[i].symbol.kind in DATA_TYPES:
        dtype = check_token_type(tokens[i], data_types)
        check_id(tokens[i+1], dtype)
        func_symtable.put(tokens[i+1])
        declarations_tree.append(DeclarationNode(dtype, tokens[i+1]))
        check_token(tokens[i+2], SEMMI)
        if tokens[i+3].symbol.kind not in DATA_TYPES:
            return i + 3, DeclarationsNode(declarations_tree)
        i += 3
    return i, DeclarationsNode(declarations_tree)

def func_def(start: int, tokens: list) -> Tuple[int, FunctionSymbolTable, FuncNode]:
    # Check and put function datatype
    dtype = check_token_type(tokens[start], data_types)
    check_id(tokens[start+1], dtype)
    func_symtable = FunctionSymbolTable(tokens[start+1].symbol.value, dtype)

    # Check function args
    check_token(tokens[start+2], LEFT_PAR)
    end_args, args_node = arg_def(start+3, tokens, func_symtable)
    check_token(tokens[end_args], RIGHT_PAR)

    # Check declarations
    check_token(tokens[end_args+1], LEFT_CURL)
    end_declarations, declarations_node = func_declarations(end_args+2, tokens, func_symtable)

    # Check function body
    end_body, body_node = func_body(end_declarations, tokens, func_symtable)

    # return statement
    check_token(tokens[end_body], REGRESA)
    check_token(tokens[end_body + 1], ID)
    id_name = tokens[end_body + 1].symbol.value
    token = func_symtable.get_token(id_name)
    dtype = None if token is None else token.dtype
    return_node = ReturnNode(dtype, id_name)
    
    # This is semantic!
    # inTable = func_symtable.contains(tokens[end_body + 2].symbol.value)
    # match_dtype = tokens[end_body + 2].dtype == func_symtable.dtype
    # if not inTable:
        # throwSyntaxError('variable no definida: ' + tokens[end_body + 2].symbol.vale)
    # if  not match_dtype:
    #     throwSyntaxError('el tipo de la funcion ' + func_symtable.name + ' y el tipo de la variable de retorno ' + tokens[end_body + 2].symbol.vale) + ' no coinciden'
    check_token(tokens[end_body + 2], SEMMI)
    check_token(tokens[end_body + 3], RIGHT_CURL)
    return end_body + 4, func_symtable, FuncNode(args_node, declarations_node, body_node, return_node)

def func_defs(tokens: list) -> Tuple[int, Dict[str, FunctionSymbolTable], List[FuncNode]]:
    if tokens[0].symbol.kind is PRINCIPAL:
        return 0, {}
    i = 0
    tables = {}
    functions_tree = []
    while tokens[i].symbol.kind is not PRINCIPAL:
        i, table, func_node = func_def(i, tokens)
        # This is semantic!
        # t = tables.get(table.name)
        # if t is not None:
        #     throwSyntaxError('función ya definida: ' + t.name)
        tables[table.name] = table
        functions_tree.append(func_node)
    return i, tables, functions_tree

# Transformaciones socioculturales en los cotos
# 1. Debate entre derechos y obligaciones, lo público y lo privado
# 2. Especie de pseudogobierno
# 3. Social agena a la sociedad cotidiana
# 4. Se desvinculan de la ciudad
# 5. los cotos cubren el 10% del tejido urbano, pero el 2% es gente que vive en coto
def principal_def(start: int, tokens: list, tables: Dict[str, FunctionSymbolTable]) -> MainNode:
    check_token(tokens[start], PRINCIPAL)
    check_token(tokens[start+1], LEFT_PAR)
    check_token(tokens[start+2], RIGHT_PAR)
    check_token(tokens[start+3], LEFT_CURL)
    principal_symtable = FunctionSymbolTable('principal', None)
    declarations_end, declarations_node = func_declarations(start+4, tokens, principal_symtable)
    body_end, body_node = func_body(declarations_end, tokens, principal_symtable)
    check_token(tokens[body_end], RIGHT_CURL)
    if body_end + 1 != len(tokens):
        throwSyntaxError('principal debe ser el último bloque de código')

def archivo(tokens: list) -> Tuple[FileNode, Dict[str, FunctionSymbolTable]]:
    last, tables, functions_tree = func_defs(tokens)
    main_tree = principal_def(last, tokens, tables)
    return FileNode(functions_tree, main_tree), tables

class Parser(object):
    def __init__(self, tokens: list, symtable: FunctionSymbolTable):
        self.tokens = tokens
        self.syntax_tree, self.functions_table = archivo(tokens)
        self.symtable = symtable

    def getSyntaxTree(self):
        return self.syntax_tree

    def getFunctionsSymbolTable(self):
        return self.functions_table
