from errors import UnexpectedIdentifierError, ErrorInExpression, UnknownIdentifierError, VariableNotInitializedError, IndexOutOfBoundsError
from lexer import Lexer

__author__ = 'gleb23'

class Type(object):
    def __init__(self):
        super(Type, self).__init__()

class SimpleType(Type):
    def __init__(self, value):
        super(SimpleType, self).__init__()
        self.value = value

    def execute(self):
        return self.value

class Int(SimpleType):
    def __init__(self, value):
        super(Int, self).__init__(value)

class Bool(Type):
    def __init__(self, value):
        super(Bool, self).__init__(value)

class String(Type):
    def __init__(self, value):
        super(String, self).__init__(value)

class Array(Type):
    def __init__(self, baseType, size):
        super(Array, self).__init__()
        self.baseType = baseType
        self.buffer = []
        for i in range(size):
            self.buffer.append(baseType())

    def get(self, ind):
        if (ind > 0 and ind < self.buffer.__len__()):
            raise IndexOutOfBoundsError(position, ind)
        return self.buffer[ind]

class Expression(object):
    def __init__(self):
        super(object, self).__init__()

    def execute(self):
        return 0; #stub

class Constant(Expression):
    def __init__(self, type, value):
        super(Constant, self).__init__()
        self.type = type(value)
        self.value = value

    def execute(self):
        return self.value

class Variable(Expression):
    def __init__(self, type, name):
        super(Variable, self).__init__()
        self.type = type
        self.name = name
        self.value = None

    def execute(self):
        if self.value is None:
            raise VariableNotInitializedError(position, self.name)
        return self.value

class FunctionCall(Expression):
    def __init__(self, function, args):
        super(FunctionCall, self).__init__()
        self.function = type(function)
        self.args = args

    def execute(self):
        for i in range (len(self.function.params)):
            self.function.param.value[i] = self.args[i]
        return self.function.execute()

class ReturnExpression(object):
    def __init__(self):
        self.exp = None

    def execute(self):
        self.exp.execute()

class BinaryOperator(Expression):
    def __init__(self, exp1, exp2):
        super(BinaryOperator, self).__init__()
        self.exp1 = exp1
        self.exp2 = exp2

class Sum(BinaryOperator):
    def __init__(self, exp1, exp2):
        super(Sum, self).__init__(exp1, exp2)

    def execute(self):
        pass

class Condition(object):
    def execute(self):
        return True; #stub

# FLOW

class Instruction(object):
    pass

class Block(object):
    def __init__(self, parentBlock):
        super(Block, self).__init__()
        self.context = Context()
        self.instructions = []
        self.parentBlock = parentBlock

    def execute(self):
        for instruction in self.instructions:
            res = instruction.execute()
            if res is not None:
                return res
        return None

class WhileLoop(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def execute(self):
        while self.condition.execute() == True:
            self.body.execute

class If(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def execute(self):
        if self.condition == True:
            self.body.execute()


class Context(object):
    variables = []
    functions = []

class Function(object):
    def __init__(self, name, parentBlock = None):
        self.name = name
        self.params = []
        self.returnType
        self.block = Block(parentBlock)

    def execute(self):
        for param in self.params:
            assert param.value is not None
        return self.block.execute()


class AssignmentOperator(object):
    def __init__(self):
        self.variable = None
        self.exp = None

    def execute(self):
        self.variable.value = self.exp.execute()


class Syntan(object):
    basic_data_types = ['int', 'bool', 'String']

    def __init__(self, source):
        self.source = source

    def parse(self):
        mainFunction = Function()
        lexer = Lexer()

        state = 0
        currentBlock = mainFunction.block
        currentFlowObject = None
        varName = None
        currentFuncCall = None

        #state = 0 # START
        #state = 1 # wait for bracket ( before condition (after if, while)
        #state = 2 # wait for bracket ) before condition (after if, while)
        #state = 3 # wait for logical expression
        #state = 10 # after type is given: wait for identifier
        #state = 11 # after variable name : only assignment
        #state = 12 # bracket after func name for
        #state = 14 # after bracket in function call: wait for argument
        #state = 50 # wait for comma after the end of instruction

        while lexer.next_available():
            new_token, position = lexer.next_token()

            if new_token == "{":
                if state == 0:
                    newBlock =  Block(currentBlock)
                    currentBlock.instructions.append(newBlock)
                    currentBlock = newBlock
                elif state == 3:
                    raise ErrorInExpression(position, '{')
                else: # state == 1:
                    raise UnexpectedIdentifierError(position, '{')
            elif new_token == '}':
                if state == 0:
                    currentBlock = currentBlock.parentBlock
                    if currentBlock is None:
                        raise UnexpectedIdentifierError(position, '}')
                else: # state == 1:
                    raise UnexpectedIdentifierError(position, '}')
            elif new_token == 'if':
                if state == 0:
                    state = 1
                    currentFlowObject = If()
                    currentBlock.instructions.append(currentFlowObject)
                elif state == 3:
                    raise ErrorInExpression(position, 'if')
                else: # state == 1:
                    raise UnexpectedIdentifierError(position, 'if')
            elif new_token == ';':
                if state == 50:
                    state = 0
            elif new_token == 'while':
                if state == 0:
                    state = 1
                    currentFlowObject = WhileLoop()
                    currentBlock.instructions.append(currentFlowObject)
                elif state == 3:
                    raise ErrorInExpression(position, 'while')
                else: # state == 1:
                    raise UnexpectedIdentifierError(position, 'while')
            elif new_token == '(':
                if state == 1:
                    expressionBuffer = self.getExpression(lexer, ')')
                    currentFlowObject.condition = self.parseExpression(expressionBuffer)
                    state = 0
                elif state == 12:
                    state == 14
                else: # state = 0
                    raise UnexpectedIdentifierError(position, '(')
            elif new_token == ')':
                if state == 2:
                    state = 0
                if state == 14:
                    state = 50
            elif new_token in self.basic_data_types:
                if state == 0:
                    #declaration
                    state = 10
            elif new_token == '=':
                if state == 11:
                    assOp = AssignmentOperator()
                    currentBlock.instructions.append(assOp)
                    assOp.variable = varName
                    exp = self.parseExpression(self.getExpression(lexer, ';'))
                    assOp.exp = exp
                    state = 0
                else: #state = 0
                    raise UnexpectedIdentifierError(position, '=')
            else: #any identifier
                if state == 0:
                    # this identifier is earlier declared: it must be function or variable in the
                    # current scope or higher
                    obj = self.searchIdentifier(new_token)
                    if obj is None:
                        raise UnknownIdentifierError(position, new_token)
                    if isinstance(obj, Variable):
                        # assignment
                        state == 11
                        varName = new_token
                    elif isinstance(obj, Function):
                        #function call
                        state = 12
                        currentFuncCall = FunctionCall()
                        currentBlock.instructions.append(currentFuncCall)
                elif state == 14:
                    currentFuncCall.args.append(self.parseExpression(self.getExpression(lexer, ',')))









        return mainFunction

    def getExpression(self, lexer, endSign):
        pass

    def parseExpression(self, expressionBuffer):
        pass

    def searchIdentifier(self, currentBlock, identifier):
        '''
        searches for identifier <code>identifier</code> in current scope or higher
        '''
        for function in currentBlock.context.functions:
            if function.name == identifier:
                return function
        for var in currentBlock.context.variables:
            if var.name == identifier:
                return var
        return self.searchIdentifier(currentBlock.parentBlock, identifier)


