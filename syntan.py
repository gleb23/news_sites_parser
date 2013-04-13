from bricks import If, WhileLoop, ReturnExpression, Array, SimpleType, AssignmentOperator, Function, FunctionCall, Block, Expression, BinaryOperator, Sum
from errors import UnexpectedIdentifierError, ErrorInExpression, UnknownIdentifierError, VariableNotInitializedError, IndexOutOfBoundsError, FunctionMustReturnSomethingError, EmptyBracketsAreNotAllowedError, ArrayMustHaveFixedSizeError, IdentifierAlreadyExistsError
from lexer import Lexer

__author__ = 'gleb23'

# = 3
# if (a) {
#     int myprint(int a) {
# return a * a;
# }
# myprint(a);
# }

source = '''
int a
'''

operator_priorities = [
    ['+', '-'],
    ['*', '/', '%']
]

def searchIdentifier(currentBlock, identifier):
    '''
    searches for identifier <code>identifier</code> in current scope or higher
    '''
    if currentBlock is None:
        return None
    if currentBlock.context.functions.has_key(identifier):
        return currentBlock.context.functions[identifier]
    if currentBlock.context.variables.has_key(identifier):
        return currentBlock.context.variables[identifier]
    return searchIdentifier(currentBlock.parentBlock, identifier)

def build_expression_tree(reverse_expression_list, bracket_state = 0):
    def split(reverse_expression_list, index, Operator):
        exp = Operator()
        exp.exp1 = build_expression_tree(reverse_expression_list[index + 1:], bracket_state)
        exp.exp2 = build_expression_tree(reverse_expression_list[:index], bracket_state)
        return exp

    if len(reverse_expression_list) == 1:
        return reverse_expression_list[0]
    while True:
        for i in range(len(operator_priorities)):
            for j in range(len(operator_priorities[i])):
                try:
                    ind = reverse_expression_list.index(operator_priorities[i][j], bracket_state)
                    if reverse_expression_list[ind] == '+':
                        return split(reverse_expression_list, ind, Sum)
                except ValueError:
                    pass
        reverse_expression_list = reverse_expression_list[1:len(reverse_expression_list) -1]
        bracket_state += 1



class CurrentDataSet(object):
    def __init__(self):
        self.current_block = None
        self.current_flow_object = None
        self.current_identifier = None
        self.var_type = None
        self.current_function = None
        self.expression_list = []
        self.bracket_state = 0
        self.expression_type = None


class State(object):
    def process_opening_curly_bracket(self, data_set, position):
        raise UnexpectedIdentifierError('{')

    def process_closing_curly_bracket(self, data_set, position):
        raise UnexpectedIdentifierError('}')

    def process_opening_square_bracket(self, data_set, position):
        raise UnexpectedIdentifierError('[')

    def process_closing_square_bracket(self, data_set, position):
        raise UnexpectedIdentifierError(']')

    def process_opening_bracket(self, data_set, position):
        raise UnexpectedIdentifierError('(')

    def process_closing_bracket(self, data_set, position):
        raise UnexpectedIdentifierError(')')

    def process_comma(self, data_set, position):
        raise UnexpectedIdentifierError(',')

    def process_semicolon(self, data_set, position):
        raise UnexpectedIdentifierError(';')

    def process_if(self, data_set, position):
        raise UnexpectedIdentifierError( 'if')

    def process_while(self, data_set, position):
        raise UnexpectedIdentifierError('while')

    def process_return(self, data_set, position):
        raise UnexpectedIdentifierError('return')

    def process_identifier(self, data_set, position):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_basic_data_type(self, data_set, position):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    #def process_assignment(self, data_set, position)


################################################
###### EXPRESSION ###########################
################################################
class AfterExpressionOpenBracket(State):
    '''
    example
    ...
    a = (... <-
    ...

    '''
    #def process_opening_curly_bracket(self, data_set, position)
    #def process_closing_curly_bracket(self, data_set, position)
    #def process_opening_square_bracket(self, data_set, position)
    #def process_closing_square_bracket(self, data_set, position)

    def process_opening_bracket(self, data_set, position):
        data_set.expression.bracket_state += 1
        data_set.expression_list.append('(')
        return AfterExpressionOpenBracket(), data_set

    def process_closing_bracket(self, data_set, position):
        raise EmptyBracketsAreNotAllowedError()

    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)
    # def process_identifier(self, data_set, position)
    # def process_basic_data_type(self, data_set, position):

    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.currentBlock, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, Array):
            raise NotImplemented()
        elif isinstance(type, SimpleType):
            data_set.expression_list.append(data_set.current_identifier)
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            data_set.current_function = Function()
            data_set.expression_list.append(data_set.current_function)
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    #def process_assignment(self, data_set, position)

class AfterExpressionOperator(State):
    '''
    example
    ...
    a = (a +... <-
    ...

    '''
    #def process_opening_curly_bracket(self, data_set, position)
    #def process_closing_curly_bracket(self, data_set, position)
    #def process_opening_square_bracket(self, data_set, position)
    #def process_closing_square_bracket(self, data_set, position)

    def process_opening_bracket(self, data_set, position):
        data_set.expression.bracket_state += 1
        data_set.expression_list = '('
        return (AfterExpressionOpenBracket, data_set)

    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)
    # def process_identifier(self, data_set, position)
    # def process_basic_data_type(self, data_set, position):

    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.currentBlock, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, Array):
            raise NotImplemented()
        elif isinstance(type, SimpleType):
            data_set.expression_list.append(data_set.current_identifier)
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            data_set.current_function = Function()
            data_set.expression_list.append(data_set.current_function)
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    #def process_assignment(self, data_set, position)


class AfterExpressionOperand(State):
    # def process_opening_curly_bracket(self, data_set, position)
    # def process_closing_curly_bracket(self, data_set, position)
    # def process_opening_square_bracket(self, data_set, position)
    # def process_closing_square_bracket(self, data_set, position)
    # def process_opening_bracket(self, data_set, position)
    def process_closing_bracket(self, data_set, position):
        if data_set.bracket_state >0:
            data_set.bracket_state -= 1
            data_set.expression_list.append(')')
            return AfterExpressionOperand(), data_set
        elif data_set.bracket_state <= 0:
            return UnexpectedIdentifierError(')')

    def process_comma(self, data_set, position):
        if data_set.bracket_state == 0:
            if data_set.expression_type == 'function_param':
                return AfterFunctionCallOpenBracketState(), data_set
            else:
                raise UnexpectedIdentifierError(',')
        else:
            raise UnexpectedIdentifierError(',')

    def process_semicolon(self, data_set, position):
        if data_set.bracket_state == 0:
            if data_set.expression_type == 'return_expression':
                return InitialState(), data_set
            else:
                raise UnexpectedIdentifierError(';')
        else:
            raise UnexpectedIdentifierError(';')

    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)
    # def process_identifier(self, data_set, position)
    # def process_basic_data_type(self, data_set, position):
    #def process_assignment(self, data_set, position)

###################################################
######### FUNCTION CALL #########################
##################################################

class AfterFunctionCallOpenBracketState(State):
    #def process_opening_curly_bracket(self, data_set, position)
    #def process_closing_curly_bracket(self, data_set, position)
    #def process_opening_square_bracket(self, data_set, position)
    #def process_closing_square_bracket(self, data_set, position)

    def process_opening_bracket(self, data_set, position):
        data_set.bracket_state += 1
        data_set.expression_list.append('(')
        return AfterExpressionOpenBracket(), data_set

    def process_closing_bracket(self, data_set, position):
        # function has no parameters
        # check whether this coinside with func declaration should be later
        return AfterExpressionOperand(), data_set

    def process_identifier(self, data_set, position):
        data_set.expression_list.append(data_set.current_identifier)
        return AfterExpressionOperand(), data_set

    #def process_basic_data_type(self, data_set, position)
    #def process_assignment(self, data_set, position)


class AfterFunctionCallNameState(State):
    #def process_opening_curly_bracket(self, data_set, position)
    #def process_closing_curly_bracket(self, data_set, position)
    #def process_opening_square_bracket(self, data_set, position)
    #def process_closing_square_bracket(self, data_set, position)

    def process_opening_bracket(self, data_set, position):
        data_set.expression_type = 'function_param'
        return (AfterFunctionCallOpenBracketState(), data_set)

    # def process_closing_bracket(self, data_set, position):
    # def process_comma(self, data_set, position)
    # def process_semicolon(self, data_set, position)
    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)
    # def process_identifier(self, data_set, position):
    # def process_basic_data_type(self, data_set, position)
    #def process_assignment(self, data_set, position)


###################################################
##################  FLOW #########################
##################################################

class InitialState(State):

    def process_opening_curly_bracket(self, data_set, position):
        newBlock = Block(data_set.currentBlock)
        data_set.currentBlock.instructions.append(newBlock)
        data_set.currentBlock = newBlock
        return InitialState(), data_set

    def process_closing_curly_bracket(self, data_set, position):
        currentBlock = data_set.currentBlock.parentBlock
        if data_set.currentBlock is None:
            raise UnexpectedIdentifierError('}')
        return InitialState(), data_set

    # def process_opening_square_bracket(self, data_set, position):
    # def process_closing_square_bracket(self, data_set, position):
    # def process_opening_bracket(self, data_set, position):
    # def process_closing_bracket(self, data_set, position):
    # def process_comma(self, data_set, position):
    # def process_semicolon(self, data_set, position):

    def process_if(self, data_set, position):
        data_set.currentIf = If()
        data_set.current_block.instructions.append(data_set.currentIf)
        return AfterIfWhileState(), data_set

    def process_while(self, data_set, position):
        data_set.current_while_loop = WhileLoop()
        data_set.current_block.instructions.append(data_set.currentWhileLoop)
        return AfterIfWhileState(), data_set

    def process_return(self, data_set, position):
        data_set.expression
        return (AfterReturnWordState(), data_set)

    def process_identifier(self, data_set, position):
    # this identifier is earlier declared: it must be function or variable in the
        # current scope or higher
        obj = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if obj is None:
            raise UnknownIdentifierError(data_set.current_identifier)
        if isinstance(obj, SimpleType):
            # assignment
            return (AfterSVariableAtStartState(), data_set)
        elif isinstance(obj, Array):
            # assignment
            return (AfterArrayAtStartState(), data_set)
        elif isinstance(obj, Function):
            #function call
            current_func_call = FunctionCall()
            data_set.current_block.instructions.append(current_func_call)
            return AfterFunctionCallNameState(), data_set

    def process_basic_data_type(self, data_set, position):
         return AfterSTypeInDeclState(), data_set
    #def process_assignment(self, data_set, position)


class AfterReturnWordState(State):
    '''
    example
    ...
    return ... <-
    ...

    '''
    # def process_opening_curly_bracket(self, data_set, position)
    # def process_closing_curly_bracket(self, data_set, position)
    # def process_opening_square_bracket(self, data_set, position)
    # def process_closing_square_bracket(self, data_set, position)
    def process_opening_bracket(self, data_set, position):
        data_set.expression.expression_type = 'return_expression'
        return AfterExpressionOpenBracket(), data_set

    # def process_closing_bracket(self, data_set, position)
    # def process_comma(self, data_set, position)
    def process_semicolon(self, data_set, position):
        raise FunctionMustReturnSomethingError(';')

    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)

    def process_identifier(self, data_set, position):
        data_set.expression.expression_type = 'return_value'
        data_set.expression.expression_list.append(data_set.current_identifier)
        return (AfterExpressionOperand(), data_set)

    # def process_basic_data_type(self, data_set, position):
    #def process_assignment(self, data_set, position)

class AfterIfWhileState(State):
    #def process_opening_curly_bracket(self, data_set, position)
    #def process_closing_curly_bracket(self, data_set, position)
    #def process_opening_square_bracket(self, data_set, position)
    #def process_closing_square_bracket(self, data_set, position)

    def process_opening_bracket(self, data_set, position):
        data_set.expression_type = 'predicate'
        return AfterIfWhileOpenBracketState(), data_set

    # def process_closing_bracket(self, data_set, position):
    # def process_comma(self, data_set, position)
    # def process_semicolon(self, data_set, position)
    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)
    # def process_identifier(self, data_set, position):
    # def process_basic_data_type(self, data_set, position):
    #def process_assignment(self, data_set, position)

class AfterIfWhileOpenBracketState(State):
    #def process_opening_curly_bracket(self, data_set, position)
    #def process_closing_curly_bracket(self, data_set, position)
    #def process_opening_square_bracket(self, data_set, position)
    #def process_closing_square_bracket(self, data_set, position)

    def process_opening_bracket(self, data_set, position):
        data_set.bracket_state += 1
        data_set.expression_list.append('(')
        return AfterExpressionOpenBracket(), data_set

    def process_closing_bracket(self, data_set, position):
        # function has no parameters
        # check whether this coinside with func declaration should be later
        raise EmptyBracketsAreNotAllowedError()

    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, Array):
            raise NotImplemented()
        elif isinstance(type, SimpleType):
            data_set.expression_list.append(data_set.current_identifier)
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            data_set.current_function = Function()
            data_set.expression_list.append(data_set.current_function)
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    # def process_basic_data_type(self, data_set, position)
    #def process_assignment(self, data_set, position)


###################################################
#############  ASSIGNMENT #########################
##################################################

class AfterAssignmentSign(State):
    '''
    example
    ...
    int b = 5;
    b =...<-
    ...

    '''
    #def process_opening_curly_bracket(self, data_set, position)
    #def process_closing_curly_bracket(self, data_set, position)

    def process_opening_bracket(self, data_set, position):
        data_set.expression.expression_type = 'assignment_value'
        return AfterExpressionOpenBracket(), data_set

    # def process_closing_bracket(self, data_set, position)
    # def process_comma(self, data_set, position)
    #def process_semicolon(self, data_set, position)

    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)

    def process_identifier(self, data_set, position):
        data_set.expression.expression_type = 'assignment_value'
        data_set.expression.expression_list.append(data_set.current_identifier)
        return (AfterExpressionOperand(), data_set)

    # def process_basic_data_type(self, data_set, position):
    # def process_assignment(self, data_set, position):

class AfterSVariableAtStartState(State):
    '''
    example
    ...
    int b = 5;
    b ...<-
    ...

    '''
    #def process_opening_curly_bracket(self, data_set, position)
    #def process_closing_curly_bracket(self, data_set, position)

    def process_opening_square_bracket(self, data_set, position):
        return (AfterArrayDeclOpenSquareBracket(), data_set)

    #def process_closing_square_bracket(self, data_set, position):

    #def process_opening_bracket(self, data_set, position)
    #def process_closing_bracket(self, data_set, position)
    #def process_comma(self, data_set, position)
    #def process_semicolon(self, data_set, position):

    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)

    def process_identifier(self, data_set, position):
        # create varable #TODO
        return AfterNameInSTypeDeclState(), data_set

    # def process_basic_data_type(self, data_set, position):
    def process_assignment(self, data_set, position):
        data_set.current_assignment = AssignmentOperator()
        data_set.current_assignment.variable = data_set.current_identifier
        data_set.current_block.instructions.append(data_set.current_assignment)
        return AfterAssignmentSign(), data_set

# class AfterIfWhileState(object):
#     def process(token, current_data_set):
#
# class AfterIfWhileState(object):
#     def process(token, current_data_set):

class AfterArrayAtStartState(State):
    '''

    example:
    int[6] arr
    ...
    arr <-
    ...

    '''
    # def process_opening_curly_bracket(self, data_set, position)
    # def process_closing_curly_bracket(self, data_set, position)

    def process_opening_square_bracket(self, data_set, position):
        #TODO WHy???
        raise UnexpectedIdentifierError('[')

    # def process_closing_square_bracket(self, data_set, position)
    # def process_opening_bracket(self, data_set, position)
    # def process_closing_bracket(self, data_set, position)
    # def process_comma(self, data_set, position)
    # def process_semicolon(self, data_set, position)
    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)
    # def process_identifier(self, data_set, position)
    #def process_basic_data_type(self, data_set, position):
    # #def process_assignment(self, data_set, position)


###################################################
##################  DECLARATIONS #########################
##################################################


class AfterArrayDeclOpenSquareBracket(State):
    # def process_opening_curly_bracket(self, data_set, position)
    # def process_closing_curly_bracket(self, data_set, position)
    # def process_opening_square_bracket(self, data_set, position)
    def process_closing_square_bracket(self, data_set, position):
        raise ArrayMustHaveFixedSizeError(position, data_set.current_identifier)
    # def process_opening_bracket(self, data_set, position)
    # def process_closing_bracket(self, data_set, position)
    # def process_comma(self, data_set, position)
    # def process_semicolon(self, data_set, position)
    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)

    def process_identifier(self, data_set, position):
        #TODO implement checking whether identifier is constant
        raise NotImplemented()

    # def process_basic_data_type(self, data_set, position):
    #def process_assignment(self, data_set, position)



class AfterNameInSTypeDeclState(State):
    '''
    example
    ...
    int b = 5;
    int c ...<-
    ...

    '''
    # def process_opening_curly_bracket(self, data_set, position)
    # def process_closing_curly_bracket(self, data_set, position)
    # def process_opening_square_bracket(self, data_set, position)
    # def process_closing_square_bracket(self, data_set, position)
    # def process_opening_bracket(self, data_set, position)
    # def process_closing_bracket(self, data_set, position)
    # def process_comma(self, data_set, position)
    def process_semicolon(self, data_set, position):
        return (InitialState(), data_set)
    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)
    #def process_identifier(self, data_set, position)
    #def process_basic_data_type(self, data_set, position):
    def process_assignment(self, data_set, position):
        return AfterAssignmentSign(), data_set


class AfterSTypeInDeclState(State):
    '''
    example
    ...
    int b = 5;
    int ...<-
    ...

    '''
    # def process_opening_curly_bracket(self, data_set, position)
    # def process_closing_curly_bracket(self, data_set, position)
    def process_opening_square_bracket(self, data_set, position):
        return (AfterArrayDeclOpenSquareBracket(), data_set)
    # def process_closing_square_bracket(self, data_set, position)
    # def process_opening_bracket(self, data_set, position)
    # def process_closing_bracket(self, data_set, position)
    # def process_comma(self, data_set, position)
    # def process_semicolon(self, data_set, position)
    # def process_if(self, data_set, position)
    # def process_while(self, data_set, position)
    # def process_return(self, data_set, position)
    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if type is None:
            data_set.current_block.context.variables[data_set.current_identifier] = eval(data_set.var_type+'()')
            return AfterNameInSTypeDeclState(), data_set
        else:
            raise IdentifierAlreadyExistsError(position)
    #def process_basic_data_type(self, data_set, position)
    #def process_assignment(self, data_set, position)


class Syntan(object):
    '''
    # RESTRICTIONS
    # array size declaration - only number, not constant
    '''
    basic_data_types = ['int', 'bool', 'String', 'void']

    def __init__(self, source):
        self.source = source

    def parse(self):
        mainFunction = Function()
        lexer = Lexer(source)
        curDataSet = CurrentDataSet()
        curDataSet.current_block = mainFunction.block
        state = InitialState()

        while lexer.next_available():
            new_token, position = lexer.next_token()
            #punctuation
            if new_token == '{':
                process = state.process_opening_curly_bracket
            elif new_token == '}':
                process = state.process_closing_curly_bracket
            elif new_token == '[':
                process = state.process_opening_square_bracket
            elif new_token == ']':
                process = state.process_closing_square_bracket
            elif new_token == '(':
                process = state.process_opening_bracket
            elif new_token == ')':
                process = state.process_closing_bracket
            elif new_token == ',':
                process = state.process_comma
            elif new_token == ';':
                process = state.process_semicolon
            #reserved words
            elif new_token == 'if':
                process = state.process_if
            elif new_token == 'while':
                process = state.process_while
            elif new_token == 'return':
                process = state.process_return
            elif new_token in self.basic_data_types:
                curDataSet.var_type = new_token
                process = state.process_basic_data_type
            else:
                curDataSet.current_identifier = new_token
                process = state.process_identifier

            state, curDataSet = process(curDataSet, position)
            return mainFunction



s = Syntan(source)
# try:
print s.parse()
# except UnknownIdentifierError, e:
#     print '!!! %s' %e

# my_list = ['a', '+', Function(), '+', 'c']
# print build_expression_tree(my_list)

