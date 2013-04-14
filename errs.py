__author__ = 'gleb23'

class CompileError(BaseException):
    def __init__(self, position):
        self.position = position


class UnexpectedIdentifierError(CompileError):
    def __init__(self, wrongSymbol = None, position = None ):
        super(UnexpectedIdentifierError, self).__init__(position)
        self.wrongSymbol = wrongSymbol

    def __str__(self):
        return 'Unexpected identifier ' + str(self.wrongSymbol) + ' ;'

class ErrorInExpression(UnexpectedIdentifierError):
    pass

class UnknownIdentifierError(CompileError):
    def __init__(self, value = None, position = None):
        super(UnknownIdentifierError, self).__init__(position)
        self.value = value

    def __str__(self):
        return 'Unknown identifier ' + str(self.value) + ';'


class FunctionMustReturnSomethingError(object):
    pass

class EmptyBracketsAreNotAllowedError(object):
    pass

class ArrayMustHaveFixedSizeError(object):
    pass

class IdentifierAlreadyExistsError(object):
    pass

class RuntimeError(object):
    pass

class VariableNotInitializedError(RuntimeError):
    pass

class IndexOutOfBoundsError(RuntimeError):
    pass
