lexer grammar Python3Lexer;

tokens {
    INDENT,
    DEDENT
}

STRING: '"' ( ESC_SEQ | ~['"\\] )* '"'
       | '\'' ( ESC_SEQ | ~['\'\\] )* '\''
       ;

NUMBER: '-'? DIGITS ('.' DIGITS)?;

NAME: [a-zA-Z_][a-zA-Z0-9_]*;

AND        : 'and';
AS         : 'as';
BREAK      : 'break';
CASE       : 'case';
CLASS      : 'class';
CONTINUE   : 'continue';
DEF        : 'def';
DEL        : 'del';
ELIF       : 'elif';
ELSE       : 'else';
EXCEPT     : 'except';
FALSE      : 'False';
FINALLY    : 'finally';
FOR        : 'for';
FROM       : 'from';
IF         : 'if';
IMPORT     : 'import';
IN         : 'in';
IS         : 'is';
LAMBDA     : 'lambda';
MATCH      : 'match';
NONE       : 'None';
NONLOCAL   : 'nonlocal';
NOT        : 'not';
OR         : 'or';
PASS       : 'pass';
RAISE      : 'raise';
RETURN     : 'return';
TRUE       : 'True';
TRY        : 'try';
UNDERSCORE : '_';
WHILE      : 'while';
WITH       : 'with';

DOT                : '.';
ELLIPSIS           : '...';
STAR               : '*';
OPEN_PAREN         : '(';
CLOSE_PAREN        : ')';
COMMA              : ',';
COLON              : ':';
SEMI_COLON         : ';';
POWER              : '**';
ASSIGN             : '=';
OPEN_BRACK         : '[';
CLOSE_BRACK        : ']';
OR_OP              : '|';
XOR                : '^';
AND_OP             : '&';
LEFT_SHIFT         : '<<';
RIGHT_SHIFT        : '>>';
ADD                : '+';
MINUS              : '-';
DIV                : '/';
MOD                : '%';
IDIV               : '//';
NOT_OP             : '~';
OPEN_BRACE         : '{';
CLOSE_BRACE        : '}';
LESS_THAN          : '<';
GREATER_THAN       : '>';
EQUALS             : '==';
GT_EQ              : '>=';
LT_EQ              : '<=';
NOT_EQ_1           : '<>';
NOT_EQ_2           : '!=';
AT                 : '@';
ARROW              : '->';
ADD_ASSIGN         : '+=';
SUB_ASSIGN         : '-=';
MULT_ASSIGN        : '*=';
AT_ASSIGN          : '@=';
DIV_ASSIGN         : '/=';
MOD_ASSIGN         : '%=';
AND_ASSIGN         : '&=';
OR_ASSIGN          : '|=';
XOR_ASSIGN         : '^=';
LEFT_SHIFT_ASSIGN  : '<<=';
RIGHT_SHIFT_ASSIGN : '>>=';
POWER_ASSIGN       : '**=';
IDIV_ASSIGN        : '//=';

SPACES: [ \t]+;

COMMENT: '#' ~[\r\n\f]*;

NEWLINE: '\r'? '\n';

SKIP_: ( SPACES | COMMENT ) -> skip;

fragment DIGITS : '0' | [1-9] [0-9]*;

fragment ESC_SEQ : '\\' . ;