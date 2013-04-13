<Number>:= 0|1|2|3|4|5|6|7|8|9
<letter>:= a-Z
<Constant>:= [–]<number>[{<number>}]
<StringConstant>::="{<letter>|<Number>}"
<Ident>:= <letter>[{<letter >|<Number>}]
<Type>:=<SimpleType>|<Array>
<SimpleType>:= int|bool|string
<Array>:=[]<SimpleType>
<Operation_а>:= +|–|*|/|%
<Operation_l>:=!|&&| || 
<Operation_cmp>:=<|>|>=|<=| == | !=
<If>:=if (<Condition>) <Block>
<Instruction>:=[{<Cycle>|<If>}]
<Cycle>:= for (<Initialization>; <Condition>, Increment) <Block>
<Block>:={ [{<Statement>}] }
<Statement>:= [<Assignment>|<If>|<Cycle>|<Input>|<Output>]
<Condition>:=<Compare>[{<Operation_l><Compare>}]
<Compare>:=<Ident|Constant> <Operation_cmp> <Ident|Constant>
<Initialization>:= <Type> <Assignment>
<Assignment>:=<Ident> = <Expression>
<Expression>:=
<Increment>:=<Assignment>