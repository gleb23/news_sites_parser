from bricks import Int, String, Bool, If, WhileLoop, ReturnExpression, Array, SimpleType, AssignmentOperator, Function, FunctionCall, Block, Expression, BinaryOperator, Sum
from errs import UnexpectedIdentifierError, ErrorInExpression, UnknownIdentifierError, VariableNotInitializedError, IndexOutOfBoundsError, FunctionMustReturnSomethingError, EmptyBracketsAreNotAllowedError, ArrayMustHaveFixedSizeError, IdentifierAlreadyExistsError
from lexer import Lexer
import bricks

__author__ = 'gleb23'

# = 3
# if (a) {
#     int myprint(int a) {
# return a * a;
# }
# myprint(a);
# }


operator_priorities = [
    ['<', '=='],
    ['+', '-'],
    ['*', '/', '%']
]

def searchIdentifier(currentBlock, identifier):
    '''
    searches for identifier <code>identifier</code> in current scope or outer
    '''
    if currentBlock is None:
        return None
    if currentBlock.context.functions.has_key(identifier):
        return currentBlock.context.functions[identifier]
    if currentBlock.context.variables.has_key(identifier):
        return currentBlock.context.variables[identifier]
    return searchIdentifier(currentBlock.parentBlock, identifier)

def split(reverse_expression_list, index, operator, bracket_state):
    operator.exp1 = build_expression_tree(reverse_expression_list[index + 1:], bracket_state)
    operator.exp2 = build_expression_tree(reverse_expression_list[:index], bracket_state)
    return operator

def build_expression_tree(reverse_expression_list, bracket_state = 0):
    if len(reverse_expression_list) == 1:
        val = reverse_expression_list[0][0]
        if isinstance(val, basestring) and val.isdigit():
            try:
                return Int(int(float(val)))
            except ValueError:
                assert False
        else:
            return val


    while True:
        for i in range(len(operator_priorities)):
            for j in range(len(operator_priorities[i])):
                try:
                    ind = reverse_expression_list.index((operator_priorities[i][j], bracket_state))
                    if reverse_expression_list[ind] == ('+', bracket_state):
                        op = Sum()
                    elif reverse_expression_list[ind] == ('-', bracket_state):
                        op = bricks.Minus()
                    return split(reverse_expression_list, ind, op, bracket_state)
                except ValueError:
                    pass
        reverse_expression_list = reverse_expression_list[1:len(reverse_expression_list) -1]
        bracket_state += 1


class Subexpression:
    def __init__(self):
        self.expression_list = []
        self.bracket_state = 0
        self.expression_type = None

class CurrentDataSet(object):
    def __init__(self):
        self.current_block = None
        self.current_flow_object = None
        self.current_return_expression = None
        self.current_assignment = None
        self.current_identifier = None
        self.current_arithm_op = None
        self.current_variable = None
        self.var_type = None
        self.current_number = ""
        self.current_string_literal = ""
        self.current_function = None
        self.subexpressions = []
        self.current_expression = None


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

    def process_assignment(self, data_set, position):
        raise UnexpectedIdentifierError('=')

    def process_number(self, data_set, position):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_string_literal(self, data_set, position):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_print(self, data_set, position):
        raise UnexpectedIdentifierError(data_set.current_identifier)

    def process_arithmetic_operations(self, data_set, position):
        raise UnexpectedIdentifierError(data_set.current_identifier)


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

    def process_opening_bracket(self, data_set, position):
        data_set.current_expression.expression_list.insert(0,('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_closing_bracket(self, data_set, position):
        raise EmptyBracketsAreNotAllowedError()

    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, Array):
            raise NotImplemented()
        elif isinstance(type, SimpleType):
            data_set.current_expression.expression_list.insert(0, (type, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            function_call = FunctionCall()
            function_call.function = type
            data_set.current_expression.expression_list.insert(0, (function_call, data_set.current_expression.bracket_state))
            data_set.current_expression = Subexpression()
            data_set.subexpressions.append(data_set.current_expression)
            data_set.current_expression.expression_type = "function_param"
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set, position):
        data_set.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set


class AfterExpressionOperator(State):
    '''
    example
    ...
    a = (a +... <-
    ...

    '''

    def process_opening_bracket(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, Array):
            raise NotImplemented()
        elif isinstance(type, SimpleType):
            data_set.current_expression.expression_list.insert(0, (type, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            function_call = FunctionCall()
            function_call.function = type
            data_set.current_expression.expression_list.insert(0, (function_call, data_set.current_expression.bracket_state))
            data_set.current_expression = Subexpression()
            data_set.subexpressions.append(data_set.current_expression)
            data_set.current_expression.expression_type = "function_param"
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number,data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set


class AfterExpressionOperand(State):
    '''
    example
    ...
    a = (4... <-
    ...

    '''
    def process_closing_bracket(self, data_set, position):
        if data_set.current_expression.bracket_state >0:
            data_set.current_expression.bracket_state -= 1
            data_set.current_expression.expression_list.insert(0, (')', data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif data_set.current_expression.bracket_state == 0:
            if data_set.current_expression.expression_type == 'function_param':
                func_arg = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.subexpressions[-1].args.append(func_arg)
                return AfterExpressionOperand(), data_set
            elif data_set.current_expression.expression_type == 'predicate':
                predicate = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.current_block.instructions[-1].condition = predicate
                return AfterIfWhileCondition(), data_set
            else:
                return UnexpectedIdentifierError(')')
        else:
            return UnexpectedIdentifierError(')')

    def process_comma(self, data_set, position):
        # end of argument expression
        if data_set.bracket_state == 0:
            if data_set.current_expression.expression_type == 'function_param':
                func_arg = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.subexpressions[-1].args.append(func_arg)
                data_set.current_expression = Subexpression()
                data_set.subexpressions.append(data_set.current_expression)
                data_set.current_expression.expression_type = 'function_param'
                return AfterFunctionCallOpenBracketState(), data_set
            else:
                raise UnexpectedIdentifierError(',')
        else:
            raise UnexpectedIdentifierError(',')

    def process_semicolon(self, data_set, position):
        if data_set.current_expression.bracket_state == 0:
            if data_set.current_expression.expression_type == 'return_expression':
                return_expression = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.current_block.instructions[-1] = return_expression   # last instruction is return expression
                return InitialState(), data_set
            elif data_set.current_expression.expression_type == 'assignment_value':
                assignment_value = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                del(data_set.current_expression)
                data_set.current_block.instructions[-1].exp = assignment_value  # last inst is assignment op
                return InitialState(), data_set
            elif data_set.current_expression.expression_type == 'print_expression':
                assignment_value = build_expression_tree(data_set.current_expression.expression_list)
                data_set.subexpressions.pop()
                data_set.current_block.instructions[-1].value = assignment_value
                return InitialState(), data_set
            else:
                raise UnexpectedIdentifierError(';')
        else:
            raise UnexpectedIdentifierError(';')

    def process_arithmetic_operations(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, (data_set.current_arithm_op, data_set.current_expression.bracket_state))
        return AfterExpressionOperator(), data_set



    ###################################################
######### FUNCTION CALL #########################
##################################################
class AfterFunctionCallOpenBracketState(State):
    '''
    example
    ...
    a = (a + myfunc(... <-
    ...

    '''
    def process_opening_bracket(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_closing_bracket(self, data_set, position):
        # function has no parameters
        # check whether this coinside with func declaration should be later
        data_set.subexpressions.pop()
        return AfterExpressionOperand(), data_set

    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.currentBlock, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, Array):
            raise NotImplemented()
        elif isinstance(type, SimpleType):
            data_set.expression_list.insert(0, (type, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            function_call = FunctionCall()
            function_call.function = type
            data_set.current_expression.expression_list.insert(0, (function_call, data_set.current_expression.bracket_state))
            data_set.current_expression = Subexpression()
            data_set.subexpressions.append(data_set.current_expression)
            data_set.current_expression.expression_type = "function_param"
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set, position):
        data_set.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set, position):
        data_set.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set


class AfterFunctionCallNameState(State):
    def process_opening_bracket(self, data_set, position):
        return (AfterFunctionCallOpenBracketState(), data_set)


###################################################
##################  FLOW #########################
##################################################

class InitialState(State):
    '''
    example
    ...
    int a = 3;
    <-
    ...

    '''
    def process_opening_curly_bracket(self, data_set, position):
        newBlock = Block(data_set.current_block)
        data_set.current_block.instructions.append(newBlock)
        data_set.current_block = newBlock
        return InitialState(), data_set

    def process_closing_curly_bracket(self, data_set, position):
        currentBlock = data_set.current_block.parentBlock
        if data_set.current_block is None:
            raise UnexpectedIdentifierError('}')
        return InitialState(), data_set

    def process_if(self, data_set, position):
        currentIf = If()
        data_set.current_block.instructions.append(currentIf)
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'predicate'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterIfWhileState(), data_set

    def process_while(self, data_set, position):
        current_while_loop = WhileLoop()
        data_set.current_block.instructions.append(current_while_loop)
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'predicate'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterIfWhileState(), data_set

    def process_return(self, data_set, position):
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'return_expression'
        data_set.subexpressions(data_set.current_expression)
        return AfterReturnWordState(), data_set

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
            function_call = FunctionCall()
            function_call.function = type
            data_set.current_expression.expression_list.insert(0, (function_call, data_set.current_expression.bracket_state))
            data_set.current_expression = Subexpression()
            data_set.subexpressions.append(data_set.current_expression)
            data_set.current_expression.expression_type = "function_param"
            return AfterFunctionCallNameState(), data_set

    def process_basic_data_type(self, data_set, position):
         return AfterSTypeInDeclState(), data_set

    def process_print(self, data_set, position):
        printOperator = bricks.PrintOperator()
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'print_expression'
        data_set.subexpressions.append(data_set.current_expression)
        data_set.current_block.instructions.append(printOperator)
        return AfterReturnWordState(), data_set     #TODO change this confusing state. all right here


class AfterReturnWordState(State):
    '''
    example
    ...
    return ... <-
    ...

    '''
    def process_opening_bracket(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set

    def process_semicolon(self, data_set, position):
        raise FunctionMustReturnSomethingError(';')

    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, Array):
            raise NotImplemented()
        elif isinstance(type, SimpleType):
            data_set.current_expression.expression_list.insert(0, (type, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            function_call = FunctionCall()
            function_call.function = type
            data_set.current_expression.expression_list.insert(0, (function_call, data_set.current_expression.bracket_state))
            data_set.current_expression = Subexpression()
            data_set.subexpressions.append(data_set.current_expression)
            data_set.current_expression.expression_type = "function_param"
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set


class AfterIfWhileState(State):
    def process_opening_bracket(self, data_set, position):
        return AfterIfWhileOpenBracketState(), data_set


class AfterIfWhileOpenBracketState(State):
    '''
    example
    ...
    a = 3;
    if (... <-
    ...

    '''
    def process_opening_bracket(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, ('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
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
            data_set.current_expression.expression_list.insert(0, (type, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            function_call = FunctionCall()
            function_call.function = type
            data_set.current_expression.expression_list.insert(0, (function_call, data_set.current_expression.bracket_state))
            data_set.current_expression = Subexpression()
            data_set.subexpressions.append(data_set.current_expression)
            data_set.current_expression.expression_type = "function_param"
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set, position):
        data_set.current_expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set, position):
        data_set.current_expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set


class AfterIfWhileCondition:
    '''
    example
    ...
    int = 3;
    if (a)...<-
    ...
    '''
    def process_opening_curly_bracket(self, data_set, position):
        newBlock = Block(data_set.current_block)
        data_set.current_block.instructions[-1].body = newBlock
        data_set.current_block = newBlock
        return InitialState(), data_set


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

    def process_opening_bracket(self, data_set, position):
        data_set.current_expression.expression_list.insert(0,('(', data_set.current_expression.bracket_state))
        data_set.current_expression.bracket_state += 1
        return AfterExpressionOpenBracket(), data_set


    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if type is None:
            raise UnknownIdentifierError()
        if isinstance(type, Array):
            raise NotImplemented()
        elif isinstance(type, SimpleType):
            data_set.current_expression.expression_list.insert(0, (type, data_set.current_expression.bracket_state))
            return AfterExpressionOperand(), data_set
        elif isinstance(type, Function):
            function_call = FunctionCall()
            function_call.function = type
            data_set.current_expression.expression_list.insert(0, (function_call, data_set.current_expression.bracket_state))
            data_set.current_expression = Subexpression()
            data_set.subexpressions.append(data_set.current_expression)
            data_set.current_expression.expression_type = "function_param"
            return AfterFunctionCallNameState(), data_set
        else:
            assert False

    def process_number(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, (data_set.current_number, data_set.current_expression.bracket_state))
        return AfterExpressionOperand(), data_set

    def process_string_literal(self, data_set, position):
        data_set.current_expression.expression_list.insert(0, data_set.current_number, data_set.current_expression.bracket_state)
        return AfterExpressionOperand(), data_set

class AfterSVariableAtStartState(State):
    '''
    example
    ...
    int b = 5;
    b ...<-
    ...

    '''

    def process_opening_square_bracket(self, data_set, position):
        return AfterArrayDeclOpenSquareBracket(), data_set
    def process_assignment(self, data_set, position):
        data_set.current_assignment = AssignmentOperator()
        data_set.current_assignment.variable = data_set.current_variable
        data_set.current_block.instructions.append(data_set.current_assignment)
        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'assignment_value'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterAssignmentSign(), data_set


class AfterArrayAtStartState(State):
    '''

    example:
    int[6] arr;
    ...
    arr <-
    ...

    '''
    def process_opening_square_bracket(self, data_set, position):
        raise NotImplemented()


###################################################
##################  DECLARATIONS #########################
##################################################


class AfterArrayDeclOpenSquareBracket(State):
    '''
    example
    ...
    int a = 3
    int[...<-
    ...
    '''
    def process_closing_square_bracket(self, data_set, position):
        raise ArrayMustHaveFixedSizeError(position, data_set.current_identifier)

    def process_identifier(self, data_set, position):
        #TODO implement checking whether identifier is constant
        raise NotImplemented()

    def process_number(self, data_set, position):
        raise NotImplemented()

    def process_string_literal(self, data_set, position):
        raise ArrayMustHaveFixedSizeError(position, data_set.current_identifier)


class AfterNameInSTypeDeclState(State):
    '''
    example
    ...
    int b = 5;
    int c ...<-
    ...

    '''

    def process_opening_bracket(self, data_set, position):
        # function declaration
        raise NotImplemented

    def process_semicolon(self, data_set, position):
        return (InitialState(), data_set)

    def process_assignment(self, data_set, position):
        data_set.current_assignment = AssignmentOperator()
        data_set.current_assignment.variable = data_set.current_variable
        data_set.current_block.instructions.append(data_set.current_assignment)

        data_set.current_expression = Subexpression()
        data_set.current_expression.expression_type = 'assignment_value'
        data_set.subexpressions.append(data_set.current_expression)
        return AfterAssignmentSign(), data_set


class AfterSTypeInDeclState(State):
    '''
    example
    ...
    int b = 5;
    int ...<-
    ...

    '''
    def process_opening_square_bracket(self, data_set, position):
        return (AfterArrayDeclOpenSquareBracket(), data_set)

    def process_identifier(self, data_set, position):
        type = searchIdentifier(data_set.current_block, data_set.current_identifier)
        if type is None:
            data_set.current_variable = eval("bricks." + data_set.var_type.capitalize()+'()')
            data_set.current_block.context.variables[data_set.current_identifier] = data_set.current_variable
            return AfterNameInSTypeDeclState(), data_set
        else:
            raise IdentifierAlreadyExistsError(position)


class Syntan(object):
    '''
    # RESTRICTIONS
    # array size declaration - only number, not constant
    # unique identifier in ALL scopes
    # type_checking !!! when 'compiling'
    # do not embrace one operand with brackets
    '''
    basic_data_types = ['int', 'bool', 'String', 'void']

    def __init__(self, source):
        self.source = source

    def parse(self):
        mainFunction = Function()
        lexer = Lexer(self.source)
        curDataSet = CurrentDataSet()
        curDataSet.current_block = mainFunction.block
        state = InitialState()

        while lexer.next_available():
            new_token, position = lexer.next_token()
            #print new_token

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
            elif new_token == 'print':
                process = state.process_print
            # arithmetic operations
            elif new_token == '+' or new_token == '-':
                process = state.process_arithmetic_operations
                curDataSet.current_arithm_op = new_token
            elif new_token in self.basic_data_types:
                curDataSet.var_type = new_token
                process = state.process_basic_data_type
            elif new_token == '=':
                process = state.process_assignment
            elif new_token.startswith("//"):
                continue
            elif new_token.startswith('"') and new_token.endswith('"'):
                curDataSet.current_string_literal = new_token
                process = state.process_string_literal
            elif new_token.isdigit():
                curDataSet.current_number = new_token
                process = state.process_number
            else:
                curDataSet.current_identifier = new_token
                process = state.process_identifier

            try:
                state, curDataSet = process(curDataSet, position)
            except UnexpectedIdentifierError, ex:
                ex.wrongSymbol = new_token
                ex.position = position
                raise ex
            except UnknownIdentifierError, ex:
                ex.value = new_token
                ex.position = position
                raise ex


        return mainFunction



#s = Syntan(source)
# try:
# print s.parse()
# except UnknownIdentifierError, e:
#     print '!!! %s' %e

# my_list = ['a', '+', Function(), '+', 'c']
# print build_expression_tree(my_list)

