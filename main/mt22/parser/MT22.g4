// STUDENT ID: 2011318
grammar MT22;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

//_____________________________________________________________
// 2. PROGRAM STRUCTURE
program: declare+ EOF ;
// declare_list: declare declare_list | declare ;
declare: var_declare | func_declare ;

// 5. DECLARATIONS page	5
// 5.1 Variable declaration
//_____________________________________________________________
// 5.1.1 Variables

var_declare: short_form        					// short form of variable declaration
			| init_var;   						// initialization of variable

short_form: identifier_list CL type_decl SM;     
identifier_list: ID CM identifier_list | ID;

init_var: ID pair exp SM;                       // CASE 1 id and 1 exp
pair: CM ID pair exp CM 						// case recursion
	| CL type_decl_init  EQ;                    // case end of recursion
type_decl_init: atomic_type | auto_type | array_type;        // can not declare type init with void type

// 5.1.2 Parameters
parameter_list_declare_infunc: LB parameter_list_declare RB;
parameter_list_declare: parameter_declare CM parameter_list_declare 
						| parameter_declare | ;
parameter_declare: ID CL type_parameter                         // parameter type not be void
					| INHERIT ID CL type_parameter
					| OUT ID CL type_parameter
					| INHERIT OUT ID CL type_parameter;
type_parameter: atomic_type | array_type | auto_type;
// 5.2 Function declaration
//_____________________________________________________________
func_declare: ID CL FUNCTION type_return                           // return type can be array, auto, void 
			parameter_list_declare_infunc 
			(INHERIT ID)
			block_statement
			| ID CL FUNCTION type_return 
			parameter_list_declare_infunc 
			block_statement;
//_____________________________________________________________


// 4. TYPE SYSTEM AND VALUES page 4
//_____________________________________________________________
type_return: atomic_type | array_type | void_type | auto_type;
type_decl: atomic_type | array_type | auto_type;
atomic_type: BOOLEAN | INTEGER | FLOAT | STRING;

array_type: ARRAY LSB dimension RSB OF atomic_type;
dimension: INTLIT CM dimension | INTLIT;   // change posintlit to intlit, because array can be null

void_type: VOID;
auto_type: AUTO;

// 6. EXPRESSIONS
//_____________________________________________________________
exp: exp1 DC exp1 | exp1;                       // concatenation string
exp1: exp2 (relational) exp2 | exp2;                      // logical or
	relational: DEQ | NEQ | LT | LE | GT | GE;
exp2: exp2 (logical) exp3 | exp3;                      // logical and
	logical: AND | OR;
exp3: exp3 (adding) exp4 | exp4;                      // additive and subtractive
	adding: ADD | SUB;
exp4: exp4 (multiplying) exp5 | exp5;                      // multiplicative and divide
	multiplying: MUL | DIV | MOD;
exp5: NOT exp5 | exp6;                      // logical not
exp6: SUB exp6 | exp7;                      // unary minus
exp7: index_operator| operands;

index_operator: ID LSB exp_list_array RSB;
exp_list_array: exp CM exp_list_array | exp | ;        // can be [] ??, check

operands: ID 
		| INTLIT 
		| FLOATLIT 
		| (TRUE | FALSE)
		| STRINGLIT 
		| arraylit                          
		| LB exp RB
		| function_call;

function_call: ID LB exp_list_call RB;

//_____________________________________________________________

// 7. STATEMENTS
//_____________________________________________________________
statement: assign_statement 
		| match_statement
		| unmatch_statement 
		| for_statement 
		| while_statement 
		| do_while_statement 
		| return_statement 
		| call_statement 
		| block_statement
		| continue_statement
		| break_statement;


// 7.1 Assignment Statement
// assign_statement: scalar_assign_statement 
// 				| index_operator_statement;
// scalar_assign_statement: scalar_var EQ exp SM;
// scalar_var: ID | index_operator;
// index_operator_statement: index_operator EQ exp SM;

assign_statement: lhs EQ exp SM;
lhs: ID | index_expression;
index_expression: ID LSB exp_list_array RSB;

// 7.2 If Statement
match_statement: IF LB exp RB match_statement ELSE match_statement
				| other_statement;
other_statement: assign_statement 
		| for_statement 
		| while_statement 
		| do_while_statement 
		| return_statement 
		| call_statement 
		| block_statement
		| continue_statement
		| break_statement;
unmatch_statement: IF LB exp RB statement 
				| IF LB exp RB match_statement ELSE unmatch_statement
				;


// 7.3 For Statement
for_statement: FOR LB scalar_init_expr 
			CM condition_expr 
			CM update_expr RB
			statement;
scalar_init_expr: scalar_var EQ exp;
scalar_var: ID| index_operator;
condition_expr: exp;
update_expr: exp;

// 7.4 While Statement
while_statement: WHILE LB exp RB statement;

// 7.5 Do-While Statement
do_while_statement: DO block_statement WHILE LB exp RB SM;

// 7.6 Break Statement
break_statement: BREAK SM;

// 7.7 Continue Statement
continue_statement: CONTINUE SM;

// 7.8 Return Statement
return_statement: RETURN exp SM | RETURN SM;

// 7.9 Call Statement
call_statement: ID LB exp_list_call RB SM;
exp_list_call: exp CM exp_list_call | exp |;

// 7.10 Block Statement
block_statement: LP statement_list RP;
statement_list: statement statement_list 
				| statement 
				| var_declare statement_list
				| var_declare
				| ;
//_____________________________________________________________

// 3. TOKENS
// 3.4 KEYWORDS
//_____________________________________________________________
AUTO: 'auto';
BREAK: 'break';
BOOLEAN: 'boolean';
DO: 'do';
ELSE: 'else';
FALSE: 'false';
FLOAT: 'float';
FOR: 'for';
FUNCTION: 'function';
IF: 'if';
INTEGER: 'integer';
RETURN: 'return';
STRING: 'string';
TRUE: 'true';
WHILE: 'while';
VOID: 'void';
OUT: 'out';
CONTINUE: 'continue';
OF: 'of';
INHERIT: 'inherit';
ARRAY: 'array';

// 3.5 OPERATORS
//_____________________________________________________________
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';
NOT: '!';
AND: '&&';
OR: '||';
DEQ: '==';
NEQ: '!=';
LT: '<';
LE: '<=';
GT: '>';
GE: '>=';
DC : '::';

// 3.6 SEPARATORS
//_____________________________________________________________
LB: '(';
RB: ')';
LSB: '[';
RSB: ']';
DOT: '.';
CM: ',';
SM: ';';
CL: ':';
LP: '{';
RP: '}';
EQ: '=';

// 3.3 Identifiers
//_____________________________________________________________
ID: [a-zA-Z_][a-zA-Z0-9_]*;

// 3.7 LITERALS
//_____________________________________________________________
// 1. String literal rule
INTLIT: '0' | [1-9]
		| [1-9][0-9]* (('_'? [0-9]+)* 
		{self.text = self.text.replace("_", "")});
POSINTLIT: [0-9] 
		| [1-9][0-9]* (('_'? [0-9]+)* 
		{self.text = self.text.replace("_", "")});    // write for array, but in present, it not be used
// 2. Floating number rule
FLOATLIT : (INTEGERPART DECIMALPART 
		| INTEGERPART DECIMALPART? EXPONENTPART
		| DECIMALPART EXPONENTPART	) 
		{self.text = self.text.replace("_", "")};     // action block must write here
fragment INTEGERPART : INTLIT;
fragment DECIMALPART : DOT DIGIT*;
fragment EXPONENTPART : ('e' | 'E') ('-' | '+')? DIGIT+;
fragment DIGIT: [0-9];
// 3. Boolean literal rule
BOOLEANLIT: TRUE | FALSE;

// 4. String literal rule


// 5. Array literal rule
arraylit: LP exp_list_arraylit RP;   
exp_list_arraylit: exp CM exp_list_arraylit | exp | ;           // array literal can be null

STRINGLIT: '"' STRING_CHAR* '"' {
    s = str(self.text);
    self.text = s[1:-1]
};              

fragment STRING_CHAR:  ~[\f\t\b\r\n"\\] | ESCAPE_SEQ | '\\"';
fragment ESCAPE_SEQ: '\\' [bfrnt'"\\];
fragment ESC_ILLEGAL:'\\' ~[bfrnt'"\\];

UNCLOSE_STRING: '"' (STRING_CHAR)* ([\f\t\b\n\r] | EOF | '\\') {
            if self.text[-1] in ["\n","\r","\b","\t","\f"] :
                raise UncloseString(self.text[1:-1])
            else: raise UncloseString(self.text[1:])
        };

ILLEGAL_ESCAPE: '"' STRING_CHAR* ESC_ILLEGAL {
            raise IllegalEscape(self.text[1:])
        };
// 3.2 PROGRAM COMMENTS
//_____________________________________________________________
LINE_CMT: '//' ~[\n\r]* -> skip;
BLOCK_CMT: '/*' .*? '*/' -> skip;

// 3.2 CHARACTER SET
WS: [ \t\r\n\f\b]+ -> skip; // skip spaces, tabs, newlines

ERROR_CHAR: . {raise ErrorToken(self.text)};
