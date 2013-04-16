from errs import IndexOutOfBoundsError, TypeMismatch

__author__ = 'gleb23'

class Type(object):
    def __init__(self):
        super(Type, self).__init__()

    def to_Bool(self):
        raise TypeMismatch()

    def to_Int(self):
        raise TypeMismatch()

class SimpleType(Type):
    def __init__(self, value):
        super(SimpleType, self).__init__()
        self.value = value

    def getx(self):
        return self._value

    def execute(self):
        return self


class Int(SimpleType):
    def __init__(self, value = 0):
        super(Int, self).__init__(value)
        #self.value = property(SimpleType.getx, self.setx)
    #TODO TYPE CHECKING!!! PyC is not that fucking python
    def setx(self, value):
        if isinstance(value, int):
            SimpleType._value = value
        else:
            raise TypeError

    def to_Bool(self):
        return Bool(self.value != 0)

    def to_Int(self):
        return self


class Bool(SimpleType):
    def __init__(self, value = False):
        super(Bool, self).__init__(value)
        #self.value = property(SimpleType.getx, self.setx)

    def setx(self, value):
        try:
            SimpleType._value = bool(value)
        except ValueError:
            raise TypeError

    def to_Bool(self):
        return self

    def to_Int(self):
        if self.value:
            return Int(1)
        else:
            return Int(0)


class String(SimpleType):
    def __init__(self, value = ""):
        super(String, self).__init__(value)
        self._x = None
        #self.value = property(SimpleType.getx, self.setx)

    def setx(self, value):
        if isinstance(value, basestring):
            SimpleType._value = value
        else:
            raise TypeError()

    def to_Bool(self):
        return Bool(self.value != "")


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
    def __init__(self):
        super(Expression, self).__init__()
        # self.parent_expression = None
        # self.bracket_state = 0

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
        s = 'Function call(function: ' + str(self.function) + ';'
        for arg in self.args:
            s += (str(arg) + ', ')
        s += ')'
        return s

class ReturnExpression(object):
    def __init__(self, exp):
        self.exp = exp

    def execute(self):
        self.exp.execute()

    def __str__(self):
        return 'Return expression(' + self.exp + ')'

class BinaryOperator(Expression):
    def __init__(self):
        super(BinaryOperator, self).__init__()
        self.exp1 = None
        self.exp2 = None


class Sum(BinaryOperator):
    def __init__(self):
        super(Sum, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if isinstance(a, String) and isinstance(b, String):
            return String(a + b)
        elif isinstance(a, String) or isinstance(b, String):
            raise TypeMismatch()
        else:
            return Int(a.to_Int().value + b.to_Int().value)

    def __str__(self):
        return '(' + str(self.exp1) + '+' + str(self.exp2) + ')'

class Minus(BinaryOperator):
    def __init__(self):
        super(Minus, self).__init__()

    def execute(self):
        a = self.exp1.execute()
        b = self.exp2.execute()
        if isinstance(a, String) or isinstance(b, String):
            raise TypeMismatch()
        else:
            return Int(a.to_Int().value - b.to_Int().value)

    def __str__(self):
        return '(' + str(self.exp1) + '-' + str(self.exp2) + ')'

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
    def __init__(self, condition = None, body = None):
        self.condition = condition
        self.body = body

    def execute(self):
        while self.condition.execute().to_Bool().value:
            self.body.execute()

    def __str__(self):
        s = 'While {\n'
        s += 'CONDITION: '
        s += str(self.condition)
        s += str(self.body)
        s += '}'
        return s

class If(object):
    def __init__(self, condition = None, body = None):
        self.condition = condition
        self.body = body

    def execute(self):
        if self.condition.execute().to_Bool().value:
            self.body.execute()

    def __str__(self):
        s = 'If {\n'
        s += 'CONDITION: '
        s += str(self.condition)
        s += str(self.body)
        s += '}'
        return s


class Context(object):
    def __init__(self):
        self.constants = {}
        self.variables = {}
        self.functions = {}

    def __str__(self):
        s = 'Context:{'
        s += '\nConstants: '
        for con in self.constants.keys():
            s += (con + " : " + str(self.constants[con]))
        s += '\nVariables: '
        for v in self.variables.keys():
            s += (v + " : " + str(self.variables[v]))
        s += '\nFunctions: '
        for f in self.functions.keys():
            s += (f + " : " + str(self.functions[f]))
        s += '\n}'
        return s

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
        if isinstance(self.variable, String) and isinstance(self.exp, String):
            self.variable.value = self.exp.execute().value
        elif isinstance(self.variable, String) or isinstance(self.exp, String):
            raise TypeMismatch()
        elif isinstance(self.variable, Int):
            self.variable.value = self.exp.execute().to_Int().value
        elif isinstance(self.variable, Bool):
            self.variable.value = self.exp.execute().to_Bool().value

class PrintOperator(object):
    def __init__(self):
        self.value = None

    def execute(self):
        print self.value.execute().value
