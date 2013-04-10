__author__ = 'gleb23'

class CompileError(object):
    def __init__(self, position):
        self.position = position

class UnexpectedIdentifierError(CompileError):
    def __init__(self, position, wrongSymbol):
        super(UnexpectedIdentifierError, self).__init__(position)
        self.wrongSymbol = wrongSymbol

class ErrorInExpression(UnexpectedIdentifierError):
    pass

class UnknownIdentifierError(CompileError):
    pass

class RuntimeError(object):
    pass

class VariableNotInitializedError(RuntimeError):
    pass

class IndexOutOfBoundsError(RuntimeError):
    pass
