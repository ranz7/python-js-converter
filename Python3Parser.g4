parser grammar Python3Parser;

options {
    superClass = Python3ParserBase;
    tokenVocab = Python3Lexer;
}

file_input
    : (stmt | NEWLINE)* EOF
    ;

funcdef
    : 'def' name parameters ('->' test)? ':' block
    ;

parameters
    : '(' argslist? ')'
    ;

argslist
    : (arg (',' arg)* (',' kwarg (',' kwarg)* )?
       | kwarg (',' kwarg)*? )
    ;

arg
    : name
    ;

kwarg
    : name '=' test
    ;

stmt
    : simple_stmts
    | compound_stmt
    ;

simple_stmts
    : simple_stmt* NEWLINE
    ;

simple_stmt
    : (
        expr_stmt
        | del_stmt
        | pass_stmt
        | flow_stmt
        | import_stmt
    )
    ;

expr_stmt
    : annassign
    | augassign testlist
    ;

annassign
    : ':' test ('=' test)?
    ;

augassign
    : (
        '+='
        | '-='
        | '*='
        | '@='
        | '/='
        | '%='
        | '&='
        | '|='
        | '^='
        | '<<='
        | '>>='
        | '**='
        | '//='
    )
    ;

del_stmt
    : 'del' exprlist
    ;

pass_stmt
    : 'pass'
    ;

flow_stmt
    : break_stmt
    | continue_stmt
    | return_stmt
    | raise_stmt
    ;

break_stmt
    : 'break'
    ;

continue_stmt
    : 'continue'
    ;

return_stmt
    : 'return' testlist?
    ;

raise_stmt
    : 'raise' (test ('from' test)?)?
    ;

import_stmt
    : import_name
    | import_from
    ;

import_name
    : 'import' dotted_as_names
    ;

import_from
    : (
        'from' (('.' | '...')* dotted_name | ('.' | '...')+) 'import' (
            '*'
            | '(' import_as_names ')'
            | import_as_names
        )
    )
    ;

import_as_name
    : name ('as' name)?
    ;

dotted_as_name
    : dotted_name ('as' name)?
    ;

import_as_names
    : import_as_name (',' import_as_name)* ','?
    ;

dotted_as_names
    : dotted_as_name (',' dotted_as_name)*
    ;

dotted_name
    : name ('.' name)*
    ;

compound_stmt
    : if_stmt
    | while_stmt
    | for_stmt
    | try_stmt
    | funcdef
    ;

if_stmt
    : 'if' test ':' block ('elif' test ':' block)* ('else' ':' block)?
    ;

while_stmt
    : 'while' test ':' block ('else' ':' block)?
    ;

for_stmt
    : 'for' exprlist 'in' testlist ':' block ('else' ':' block)?
    ;

try_stmt
    : (
        'try' ':' block (
            (except_clause ':' block)+ ('else' ':' block)? ('finally' ':' block)?
            | 'finally' ':' block
        )
    )
    ;

except_clause
    : 'except' (test ('as' name)?)?
    ;

block
    : simple_stmts
    | NEWLINE INDENT stmt+ DEDENT
    ;

pattern
    : as_pattern
    | or_pattern
    ;

as_pattern
    : or_pattern 'as' name
    ;

or_pattern
    : closed_pattern ('|' closed_pattern)*
    ;

closed_pattern
    : literal_pattern
    | wildcard_pattern
    | value_pattern
    | group_pattern
    | sequence_pattern
    ;

literal_pattern
    : signed_number
    | strings
    | 'None'
    | 'True'
    | 'False'
    ;

literal_expr
    : signed_number
    | strings
    | 'None'
    | 'True'
    | 'False'
    ;


signed_number
    : NUMBER
    | '-' NUMBER
    ;

signed_real_number
    : real_number
    | '-' real_number
    ;

real_number
    : NUMBER
    ;

wildcard_pattern
    : '_'
    ;

value_pattern
    : attr
    ;

attr
    : name ('.' name)+
    ;

name_or_attr
    : attr
    | name
    ;

group_pattern
    : '(' pattern ')'
    ;

sequence_pattern
    : '[' maybe_sequence_pattern? ']'
    | '(' open_sequence_pattern? ')'
    ;

open_sequence_pattern
    : maybe_star_pattern ',' maybe_sequence_pattern?
    ;

maybe_sequence_pattern
    : maybe_star_pattern (',' maybe_star_pattern)* ','?
    ;

maybe_star_pattern
    : star_pattern
    | pattern
    ;

star_pattern
    : '*' wildcard_pattern
    ;

items_pattern
    : key_value_pattern (',' key_value_pattern)*
    ;

key_value_pattern
    : (literal_expr | attr) ':' pattern
    ;

double_star_pattern
    : '**' pattern_capture_target
    ;

pattern_capture_target
    : name
    ;

positional_patterns
    : pattern (',' pattern)*
    ;

keyword_patterns
    : keyword_pattern (',' keyword_pattern)*
    ;

keyword_pattern
    : name '=' pattern
    ;

test
    : or_test ('if' or_test 'else' test)?
    ;

test_nocond
    : or_test
    ;

or_test
    : and_test ('or' and_test)*
    ;

and_test
    : not_test ('and' not_test)*
    ;

not_test
    : 'not' not_test
    | comparison
    ;

comparison
    : expr (comp_op expr)*
    ;

comp_op
    : '<'
    | '>'
    | '=='
    | '>='
    | '<='
    | '<>'
    | '!='
    | 'in'
    | 'not' 'in'
    | 'is'
    | 'is' 'not'
    ;

star_expr
    : '*' expr
    ;

expr
    : atom_expr
    | expr '**' expr
    | ('+' | '-' | '~')+ expr
    | expr ('*' | '@' | '/' | '%' | '//') expr
    | expr ('+' | '-') expr
    | expr ('<<' | '>>') expr
    | expr '&' expr
    | expr '^' expr
    | expr '|' expr
    ;

atom_expr
    : atom
    ;

atom
    : '[' testlist_comp? ']'
    | name
    | NUMBER
    | STRING+
    | '...'
    | 'None'
    | 'True'
    | 'False'
    ;

name
    : NAME
    | '_'
    | 'match'
    ;

testlist_comp
    : (test | star_expr) (comp_for | (',' (test | star_expr))* ','?)
    ;

exprlist
    : (expr | star_expr) (',' (expr | star_expr))* ','?
    ;

testlist
    : test (',' test)* ','?
    ;

arglist
    : argument (',' argument)* ','?
    ;

argument
    : (test comp_for? | test '=' test | '**' test | '*' test)
    ;

comp_iter
    : comp_for
    | comp_if
    ;

comp_for
    : 'for' exprlist 'in' or_test comp_iter?
    ;

comp_if
    : 'if' test_nocond comp_iter?
    ;

strings
    : STRING+
    ;