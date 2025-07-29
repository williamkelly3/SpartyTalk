
# Student name: Will Kelly

from rply import LexerGenerator, ParserGenerator
from rply.errors import LexingError
import json

def check_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def check_int(num):
    first = False
    try:
        int(num)
        return True
    except ValueError:
        return False

class ParserState(object):
    def __init__(self, id):
        self.id = id

class RunTimeState:
    def __init__(self):
        self.sso = []
        self.pc = 0
        self.scache = {}
        self.som = {}
        self.symtable = {}

def parse_spartytalk(program):
    # Implement this function
    lexgen = LexerGenerator()

    lexgen.add('AND', r'and')
    lexgen.add('OR', r'or')
    lexgen.add('NOT', r'not')
    lexgen.add('TRUE', r'true')
    lexgen.add('FALSE', r'false')
    lexgen.add('IF', r'if')
    lexgen.add('ELSE', r'else')
    lexgen.add('WHILE', r'while')
    lexgen.add('FUNCTION', r'function')
    lexgen.add('RETURN', r'return')
    lexgen.add('CALL', r'call')
    lexgen.add('BEGIN', r'\{')
    lexgen.add('END', r'\}')
    lexgen.add('GOGREEN', r'gogreen')
    lexgen.add('GOWHITE', r'gowhite')
    lexgen.add('SPARTYSAYS', r'spartysays')
    lexgen.add('SEMICOLON', r';')
    lexgen.add('NVAR', r'nvar')
    lexgen.add('SVAR', r'svar')
    lexgen.add('IDENTIFIER', r'[a-zA-Z]+[0-9]*[a-zA-Z]*')
    lexgen.add('NUMBER', r'[+\-]?[0-9]+(\.[0-9]+)?')
    lexgen.add('STRING', r'"[^"]*"')
    lexgen.add('PLUS', r'\+')
    lexgen.add('MINUS', r'\-')
    lexgen.add('MUL', r'\*')
    lexgen.add('DIV', r'/')
    lexgen.add('LESSEQ', r'<=')
    lexgen.add('GREATEREQ', r'>=')
    lexgen.add('NOTEQ', r'!=')
    lexgen.add('LESS', r'<')
    lexgen.add('GREATER', r'>')
    lexgen.add('EQUAL', r'==')
    lexgen.add('ASSIGNMENT', r'=')
    lexgen.add('OPEN_PARENS', r'\(')
    lexgen.add('CLOSE_PARENS', r'\)')
    lexgen.add('COMMA', r',')

    lexgen.ignore(r'[ \t\n]+')

    lexer = lexgen.build()
    try:
        token_iter = lexer.lex(program)
    except LexingError as e:
        return (None, e.getsourcepos().lineno, e.getsourcepos().colno)

    pg = ParserGenerator(
        ['GOGREEN', 'GOWHITE', 'SPARTYSAYS', 'SEMICOLON', 'NVAR', 'SVAR', 'IDENTIFIER',
         'NUMBER', 'STRING', 'PLUS', 'MINUS', 'MUL', 'DIV', 'ASSIGNMENT', 'OPEN_PARENS', 'CLOSE_PARENS',
         'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'LESSEQ', 'GREATEREQ', 'NOTEQ', 'LESS', 'GREATER', 'EQUAL',
         'IF', 'ELSE', 'BEGIN', 'END', 'WHILE', 'FUNCTION', 'RETURN', 'COMMA', 'CALL'],
        precedence=[
            ('left', ['PLUS', 'MINUS']),
            ('left', ['MUL', 'DIV']),
            ('left', ['LESS', 'GREATER', 'EQUAL', 'LESSEQ', 'GREATEREQ', 'NOTEQ']),
            ('left', ['AND', 'OR', 'NOT'])
        ]
    )

    @pg.production('program : scope')
    def program_procedure(state, p):
        return {
            "type": "program",
            "scope": p[0]
        }
    @pg.production('scope : GOGREEN SEMICOLON statements GOWHITE SEMICOLON')
    def program_(state, p):
        return {
            "type": "scope",
            "statements": p[2]
        }

    @pg.production('statements : statement')
    def statements_1(state, p):
        list_s = []
        list_s.append(p[0])
        return list_s

    @pg.production('statements : statements statement')
    def statements_2(state, p):
        p[0].append(p[1])
        return p[0]

    @pg.production('statement : IF boolexp scope')
    def statement_if(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "if",
            "boolexp": p[1],
            "scope": p[2]
        }

    @pg.production('statement : WHILE boolexp scope')
    def statement_while(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "while",
            "boolexp": p[1],
            "scope": p[2]
        }

    @pg.production('statement : FUNCTION IDENTIFIER OPEN_PARENS parameters CLOSE_PARENS scope')
    def statement_function(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "function",
            "name": p[1].value,
            "parameters": p[3],
            "scope": p[5]
        }

    @pg.production('statement : FUNCTION IDENTIFIER OPEN_PARENS CLOSE_PARENS scope')
    def statement_function_noparam(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "function",
            "name": p[1].value,
            "parameters": [],
            "scope": p[4]
        }

    @pg.production('statement : CALL IDENTIFIER OPEN_PARENS arguments CLOSE_PARENS SEMICOLON')
    def statement_call(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "call",
            "name": p[1].value,
            "arguments": p[3]
        }

    @pg.production('statement : CALL IDENTIFIER OPEN_PARENS CLOSE_PARENS SEMICOLON')
    def statement_call_empty(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "call",
            "name": p[1].value,
            "arguments": []
        }

    @pg.production('arguments : argument')
    def arguments_argument(state, p):
        return [p[0]]

    @pg.production('arguments : arguments COMMA argument')
    def arguments_arguments_argument(state, p):
        p[0].append(p[2])
        return p[0]

    @pg.production('argument : expression')
    def argument_identifier(state, p):
        return p[0]

    @pg.production('statement : RETURN expression SEMICOLON')
    def statement_return(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "return",
            "expression": p[1]
        }

    @pg.production('parameters : parameter')
    def parameters_parameter(state, p):
        return [p[0]]

    @pg.production('parameters : parameters COMMA parameter')
    def parameters_parameter_parameter(state, p):
        p[0].append(p[2])
        return p[0]

    @pg.production('parameter : IDENTIFIER')
    def parameters_identifier(state, p):
        return p[0].value

    @pg.production('statement : IF boolexp scope ELSE scope')
    def statement_if_else(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "ifelse",
            "boolexp": p[1],
            "truescope": p[2],
            "falsescope": p[4]
        }

    @pg.production('statement : SPARTYSAYS expression SEMICOLON')
    def statement_1(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "spartysays",
            "expression": p[1]
        }

    @pg.production('statement : NVAR IDENTIFIER ASSIGNMENT expression SEMICOLON')
    def statement_2(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "nvar",
            "identifier": p[1].value,
            "expression": p[3]
        }

    @pg.production('statement : SVAR IDENTIFIER ASSIGNMENT expression SEMICOLON')
    def statement_3(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "svar",
            "identifier": p[1].value,
            "expression": p[3]
        }

    @pg.production('statement : IDENTIFIER ASSIGNMENT expression SEMICOLON')
    def statement_4(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "statement",
            "statement_type": "assignment",
            "identifier": p[0].value,
            "expression": p[2]
        }

    @pg.production('expression : IDENTIFIER')
    def expression_1(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "identifier",
            "identifier": p[0].value
        }

    @pg.production('expression : NUMBER')
    def expression_2(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "number",
            "value": p[0].value
        }

    @pg.production('expression : STRING')
    def expression_3(state, p):
        state.id += 1
        temp = p[0].value
        val = temp.strip("\"")
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "string",
            "value": val
        }

    @pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
    def expression_4(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "parentheses",
            "expression": p[1]
        }

    @pg.production('boolexp : boolexp AND boolexp')
    @pg.production('boolexp : boolexp OR boolexp')
    def boolexp_boolexp_andor_boolexp(state, p):
        state.id += 1
        if p[1].value == 'and':
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "and",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == 'or':
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "or",
                "left": p[0],
                "right": p[2]
            }
        else:
            return None

    @pg.production('boolexp : NOT boolexp')
    def boolexp_not_boolexp(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "boolexp",
            "expression_type": "not",
            "boolexp": p[1]
        }

    @pg.production('boolexp : expression GREATER expression')
    @pg.production('boolexp : expression LESS expression')
    @pg.production('boolexp : expression EQUAL expression')
    @pg.production('boolexp : expression GREATEREQ expression')
    @pg.production('boolexp : expression LESSEQ expression')
    @pg.production('boolexp : expression NOTEQ expression')
    def boolexp_exp_op_exp(state, p):
        state.id += 1
        if p[1].value == ">":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "greater",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == "<":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "less",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == "==":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "eq",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == ">=":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "greater or equal",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == "<=":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "less or equal",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == "!=":
            return {
                "id": state.id,
                "type": "boolexp",
                "expression_type": "not equal",
                "left": p[0],
                "right": p[2]
            }

    @pg.production('expression : expression PLUS expression')
    @pg.production('expression : expression MINUS expression')
    @pg.production('expression : expression MUL expression')
    @pg.production('expression : expression DIV expression')
    def expression_5(state, p):
        state.id += 1
        if p[1].value == '+':
            return {
                "id": state.id,
                "type": "expression",
                "expression_type": "plus",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == '-':
            return {
                "id": state.id,
                "type": "expression",
                "expression_type": "minus",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == '*':
            return {
                "id": state.id,
                "type": "expression",
                "expression_type": "mul",
                "left": p[0],
                "right": p[2]
            }
        elif p[1].value == '/':
            return {
                "id": state.id,
                "type": "expression",
                "expression_type": "div",
                "left": p[0],
                "right": p[2]
            }

    @pg.production('expression : CALL IDENTIFIER OPEN_PARENS arguments CLOSE_PARENS')
    def expression_call(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "call",
            "name": p[1].value,
            "arguments": p[3]
        }

    @pg.production('expression : CALL IDENTIFIER OPEN_PARENS CLOSE_PARENS')
    def expression_call_empty(state, p):
        state.id += 1
        return {
            "id": state.id,
            "type": "expression",
            "expression_type": "call",
            "name": p[1].value,
            "arguments": []
        }

    @pg.error
    def error_handle(state, tok):
        raise Exception({
            "id": state.id,
            "type": "error",
            "tokentype": tok.gettokentype(),
            "line": tok.getsourcepos().lineno,
            "column": tok.getsourcepos().colno
        })

    parser = pg.build()
    return (parser.parse(token_iter, state=ParserState(0)))

def evaluate_expression(expression, rts):
    if expression["expression_type"] == "string":
        return str(expression["value"])
    elif expression["expression_type"] == "number":
        num = expression["value"]
        if check_int(num):
            return int(num)
        elif check_float(num):
            return float(num)
    elif expression["expression_type"] == "identifier":
        return(rts.symtable[expression["identifier"]]["value"])
    elif expression["expression_type"] == "parentheses":
        return evaluate_expression(expression["expression"], rts)
    elif expression["expression_type"] == "plus":
        if type(evaluate_expression(expression["left"], rts)) == str or type(evaluate_expression(expression["right"], rts)) == str:
            return str(evaluate_expression(expression["left"], rts)) + \
               str(evaluate_expression(expression["right"], rts))
        return evaluate_expression(expression["left"], rts) + \
               evaluate_expression(expression["right"], rts)
    elif expression["expression_type"] == "minus":
        if type(evaluate_expression(expression["left"], rts)) == str or type(evaluate_expression(expression["right"], rts)) == str:
            return str(evaluate_expression(expression["left"], rts)) + \
               str(evaluate_expression(expression["right"], rts))
        return evaluate_expression(expression["left"], rts) - \
               evaluate_expression(expression["right"], rts)
    elif expression["expression_type"] == "mul":
        if type(evaluate_expression(expression["left"], rts)) == str or type(evaluate_expression(expression["right"], rts)) == str:
            return str(evaluate_expression(expression["left"], rts)) + \
               str(evaluate_expression(expression["right"], rts))
        return evaluate_expression(expression["left"], rts) * \
               evaluate_expression(expression["right"], rts)
    elif expression["expression_type"] == "div":
        if type(evaluate_expression(expression["left"], rts)) == str or type(evaluate_expression(expression["right"], rts)) == str:
            return str(evaluate_expression(expression["left"], rts)) + \
               str(evaluate_expression(expression["right"], rts))
        return evaluate_expression(expression["left"], rts) / \
               evaluate_expression(expression["right"], rts)
    elif expression["expression_type"] == "call":
        scoperts = RunTimeState()
        params = rts.symtable[expression["name"]]["parameters"]

        for k in rts.symtable.keys():
            if "type" in rts.symtable[k]:
                if rts.symtable[k]["type"] == "function":
                    scoperts.symtable[k] = rts.symtable[k]

        for i in range(len(expression["arguments"])):
            argexpr = expression["arguments"][i]
            scoperts.symtable[params[i]] = {
                "type": "identifier",
                "value": evaluate_expression(argexpr, rts)
            }
        return interpret_scope(rts.symtable[expression["name"]]["scope"], scoperts)
    else:
        print("Expression evaluation error: unknown expression type.")

def evaluate_boolean_expression(boolexp, rts):
    if boolexp["expression_type"] == "and":
        return evaluate_boolean_expression(boolexp["left"], rts) and evaluate_boolean_expression(boolexp["right"], rts)
    elif boolexp["expression_type"] == "or":
        return evaluate_boolean_expression(boolexp["left"], rts) or evaluate_boolean_expression(boolexp["right"], rts)
    elif boolexp["expression_type"] == "not":
        return not evaluate_boolean_expression(boolexp["boolexp"], rts)
    elif boolexp["expression_type"] == "eq":
        return evaluate_expression(boolexp["left"], rts) == evaluate_expression(boolexp["right"], rts)
    elif boolexp["expression_type"] == "less":
        return evaluate_expression(boolexp["left"], rts) < evaluate_expression(boolexp["right"], rts)
    elif boolexp["expression_type"] == "greater":
        return evaluate_expression(boolexp["left"], rts) > evaluate_expression(boolexp["right"], rts)
    elif boolexp["expression_type"] == "greater or equal":
        return evaluate_expression(boolexp["left"], rts) >= evaluate_expression(boolexp["right"], rts)
    elif boolexp["expression_type"] == "less or equal":
        return evaluate_expression(boolexp["left"], rts) <= evaluate_expression(boolexp["right"], rts)
    elif boolexp["expression_type"] == "not equal":
        return evaluate_expression(boolexp["left"], rts) != evaluate_expression(boolexp["right"], rts)
    else:
        print("Boolean expression evaluat error.")
        return None

def interpret_scope(scope, rts):
    count = 0
    for statement in scope["statements"]:
        rts.sso.append(statement["id"])
        rts.som[statement["id"]] = count
        rts.scache[statement["id"]] = statement
        count += 1

    while True:
        # print("EXECUTING STATEMENT:")
        # print(rts.scache[rts.sso[rts.pc]],"HERE")

        statement = rts.scache[rts.sso[rts.pc]]

        if statement["statement_type"] == "assignment":
            rts.symtable[statement["identifier"]] = {
                "type": "identifier",
                "value": evaluate_expression(statement["expression"], rts)
            }

        if statement["statement_type"] == "svar":
            rts.symtable[statement["identifier"]] = {
                "value": evaluate_expression(statement["expression"], rts)
            }
        if statement["statement_type"] == "nvar":
            rts.symtable[statement["identifier"]] = {
                "value": evaluate_expression(statement["expression"], rts)
            }
        if statement["statement_type"] == "spartysays":
            print(evaluate_expression(statement["expression"], rts))

        if statement["statement_type"] == "if":
            scoperts = RunTimeState()
            scoperts.symtable = rts.symtable
            if evaluate_boolean_expression(statement["boolexp"], rts):
                interpret_scope(statement["scope"], scoperts)

        if statement["statement_type"] == "while":
            scoperts = RunTimeState()
            scoperts.symtable = rts.symtable
            while evaluate_boolean_expression(statement["boolexp"], rts):
                scoperts.sso = []
                scoperts.pc = 0
                scoperts.scache = {}
                scoperts.som = {}
                scoperts.symtable = rts.symtable
                interpret_scope(statement["scope"], scoperts)

        if statement["statement_type"] == "ifelse":
            scoperts = RunTimeState()
            scoperts.symtable = rts.symtable
            if evaluate_boolean_expression(statement["boolexp"], rts):
                interpret_scope(statement["truescope"], scoperts)
            else:
                interpret_scope(statement["falsescope"], scoperts)

        if statement["statement_type"] == "function":
            rts.symtable[statement["name"]] = {
                "type": "function",
                "scope": statement["scope"],
                "parameters": statement["parameters"]
            }

        if statement["statement_type"] == "call":
            scoperts = RunTimeState()
            params = rts.symtable[statement["name"]]["parameters"]

            for k in rts.symtable.keys():
                if "type" in rts.symtable[k]:
                    if rts.symtable[k]["type"] == "function":
                        scoperts.symtable[k] = rts.symtable[k]

            for i in range(len(statement["arguments"])):
                argexpr = statement["arguments"][i]
                scoperts.symtable[params[i]] = {
                    "type": "identifier",
                    "value": evaluate_expression(argexpr, rts)
                }

            interpret_scope(rts.symtable[statement["name"]]["scope"], scoperts)

        if statement["statement_type"] == "return":
            return evaluate_expression(statement["expression"], rts)

        if rts.pc == len(rts.sso) - 1:
            break

        rts.pc = rts.som[rts.sso[rts.pc]] + 1

def interpret_spartytalk(program):
    # Implement this function
    rts = RunTimeState()
    ir = parse_spartytalk(program)
    interpret_scope(ir["scope"], rts)