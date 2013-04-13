from errors import IndexOutOfBoundsError

__author__ = 'gleb23'

class Type(object):
    def __init__(self):
        super(Type, self).__init__()

class SimpleType(Type):
    _value = None
    def __init__(self, value):
        super(SimpleType, self).__init__()
        self.value = value

    def getx(self):
        return self._value

    def execute(self):
        return self.value

class Int(SimpleType):
    def __init__(self, value):
        super(Int, self).__init__(value)

    def setx(self, value):
        if isinstance(value, int):
            SimpleType._value = value
        else:
            raise TypeError


    value = property(SimpleType.getx, setx)


class Bool(SimpleType):
    def __init__(self, value):
        super(Bool, self).__init__(value)

    def setx(self, value):
        try:
            SimpleType._value = bool(value)
        except ValueError:
            raise TypeError

    value = property(SimpleType.getx, setx)

class String(SimpleType):
    def __init__(self, value):
        super(String, self).__init__(value)
        self._x = None

    def setx(self, value):
        if isinstance(value, basestring):
            SimpleType._value = value
        else:
            raise TypeError()

    value = property(SimpleType.getx, setx)

class Array(Type):
    def __init__(self, baseType, size):
        super(Array, self).__init__()
        self.baseType = baseType
        self.buffer = []
        for i in range(size):
            self.buffer.append(baseType(None))

    def get(self, ind):
        if (ind > 0 and ind < len(self.buffer)):
            return self.buffer[ind]
        raise IndexOutOfBoundsError(ind)


    def set(self, ind, value):
        if (ind > 0 and ind < len(self.buffer)):
            self.buffer[ind] = value
        raise IndexOutOfBoundsError(ind)

    def __str__(self):
        return 'base: ' + str(self.base) + ' size: ' + 'str(self.buffer.size)'


class Expression(object):
    parent_expression = None
    bracket_state = 0
    def __init__(self):
        super(Expression, self).__init__()

    def execute(self):
        return 0; #stub

class FunctionCall(Expression):
    def __init__(self, function, args):
        super(FunctionCall, self).__init__()
        self.function = type(function)
        self.args = args

    def execute(self):
        for i in range (len(self.function.params)):
            self.function.param.value[i] = self.args[i]
        return self.function.execute()

    def __str__(self):
        str = 'Function call(function: ' + str(self.function) + ';'
        for arg in self.args:
            str += (str(arg) + ', ')
        str += ')'

class ReturnExpression(object):
    def __init__(self, exp):
        self.exp = exp

    def execute(self):
        self.exp.execute()

    def __str__(self):
        return 'Return expression(' + self.exp + ')'

class BinaryOperator(Expression):
    exp1 = None
    exp2 = None
    def __init__(self):
        super(BinaryOperator, self).__init__()


class Sum(BinaryOperator):
    def __init__(self):
        super(Sum, self).__init__()

    def execute(self):
        pass

    def __str__(self):
        return '(' + str(self.exp1) + '+' + str(self.exp2) + ')'

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

    def __str__(self):
        s = 'Block {\n'
        s += 'Context:\n'
        s += str(self.context)
        s += '\n'
        for instr in self.instructions:
            s += str(instr)
            s += '\n'
        s += '}'
        return s

class WhileLoop(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def execute(self):
        while self.condition.execute() == True:
            self.body.execute

    def __str__(self):
        str = 'While {\n'
        str += 'CONDITION: '
        str += str(self.condition)
        str += str(self.body)
        str += '}'

class If(object):
    def __init__(self, condition = None, body = None):
        self.condition = condition
        self.body = body

    def execute(self):
        if self.condition == True:
            self.body.execute()

    def __str__(self):
        str = 'If {\n'
        str += 'CONDITION: '
        str += str(self.condition)
        str += str(self.body)
        str += '}'


class Context(object):
    constants = {}
    variables = {}
    functions = {}

    def __str__(self):
        return 'Context'

class Function(object):
    def __init__(self, name = None, parentBlock = None):
        self.name = name
        self.params = []
        self.returnType = None
        self.block = Block(parentBlock)

    def execute(self):
        for param in self.params:
            assert param.value is not None
        return self.block.execute()

    def __str__(self):
        s = "Function {\n"
        s += ("Name: " + str(self.name) + "\n")
        s += ("Returns: " + str(self.returnType) + "\n")
        for param in self.params:
            s += str(param) + " "
        s += "\n"
        s += str(self.block)
        s += "}"
        return s


class AssignmentOperator(object):
    def __init__(self):
        self.variable = None
        self.exp = None

    def execute(self):
        self.variable.value = self.exp.execute()
