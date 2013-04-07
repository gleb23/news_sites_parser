from lexer import Lexer

__author__ = 'gleb23'

class Constant:
    pass

class Variable:
    pass

class Expression(object):
    def value(self):
        return 0; #stub

class Condition(object):
    def value(self):
        return True; #stub

# FLOW

class WhileLoop(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class If(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Context(object):
    variables = []
    functions = []

class Function(object):
    args = []
    context = None
    instructions = []


class Syntan(object):
    basic_data_types = []

    def __init__(self, source):
        self.source = source

    def parse(self):
        mainFunction = Function()
        lexer = Lexer()
        while lexer.next_available():
            new_token = lexer.next_token()
        #
        #
        #
        return mainFunction

