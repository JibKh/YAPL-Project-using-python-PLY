import ply.lex as lex
import ply.yacc as yacc
import sys

# =========================== LEXER =================================

# Declare tokens
tokens = [
	'SEMICOLON',
	'VAR_NAME',
	'PRINT',
	'COMMA',
	'LPARA',
	'RPARA',
	'EQUALS',
	# VAR TYPES
	'TYPE_BOOL',
	'TYPE_CHAR',
	'TYPE_STRING',
	'TYPE_INT',
	'TYPE_DOUBLE',
	# VARIABLES
	'INT',
	'BOOL',
	'DOUBLE',
	'CHAR',
	'STRING',
	# NUMERICALS
	'PLUS',
	'MINUS',
	'DIVIDE',
	'MULTIPLY',
	'MODULO',
	'INCREMENT',
	'DECREMENT',
	'POWER',
	#LOGIAL OPERATORS
	'LESSER',
	'GREATER',
	'GREATER_EQUAL',
	'LESSER_EQUAL',
	'NOT_EQUAL',
	'DOUBLE_EQUAL',
	'NOT',
	'AND',
	'OR',
	# DO WHILE
	'DO',
	'WHILE',
	'LBRACE',
	'RBRACE',
	# LIST
	'LIST',
	'LBRACK',
	'RBRACK',
	'DOT',
	'INDEX',
	'SLICE',
	'POP',
	'PUSH',
]


t_LBRACK = r'\['
t_RBRACK = r'\]'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\--'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_EQUALS = r'\='
t_PLUS = r'\+'
t_MODULO = r'\%'
t_SEMICOLON = r'\;'
t_LPARA = r'\('
t_RPARA = r'\)'
t_POWER = r'\^'
t_COMMA = r'\,'
t_GREATER = r'\>'
t_LESSER = r'\<'
t_GREATER_EQUAL = r'\>\='
t_LESSER_EQUAL = r'\<\='
t_NOT_EQUAL = r'\!\='
t_DOUBLE_EQUAL = r'\=\='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'

t_ignore = ' \n\t'

def t_PUSH(t):
	r'push'
	t.type = 'PUSH'
	return t
	
def t_POP(t):
	r'pop'
	t.type = 'POP'
	return t

def t_INDEX(t):
	r'index'
	t.type = 'INDEX'
	return t

def t_SLICE(t):
	r'slice'
	t.type = 'SLICE'
	return t

def t_LIST(t):
	r'list'
	t.type = 'LIST'
	return t

def t_DO(t):
	r'DO'
	t.type = 'DO'
	return t

def t_WHILE(t):
	r'WHILE'
	t.type = 'WHILE'
	return t

def t_AND(t):
	r'AND'
	t.type = 'AND'
	return t

def t_OR(t):
	r'OR'
	t.type = 'OR'
	return t

def t_NOT(t):
	r'NOT'
	t.type = 'NOT'
	return t

def t_TYPE_PRINT(t):
	r'print'
	t.type = 'PRINT'
	return t

def t_TYPE_INT(t):
	r'int'
	t.type = 'TYPE_INT'
	return t

def t_TYPE_DOUBLE(t):
	r'double'
	t.type = 'TYPE_DOUBLE'
	return t

def t_TYPE_BOOL(t):
	r'bool'
	t.type = 'TYPE_BOOL'
	return t

def t_TYPE_CHAR(t):
	r'char'
	t.type = 'TYPE_CHAR'
	return t

def t_TYPE_STRING(t):
	r'string'
	t.type = 'TYPE_STRING'
	return t
	
def t_BOOL(t):
	r'False|True'
	
	if t.value == 'False':
		t.value = False
	else:
		t.value = True
		
	#t.value = bool(t.value)
	t.type = 'BOOL'
	return t

def t_VAR_NAME(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = 'VAR_NAME'
	return t

def t_DOUBLE(t):
	r'[\-]?\d+\.\d+'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'[\-]?\d+'
	t.value = int(t.value)
	return t

def t_CHAR(t):
	r'"[^"]?"'
	t.value = t.value[1:-1]
	t.type = 'CHAR'
	return t

def t_STRING(t):
	r'"[^"]*"'
	t.value = t.value[1:-1]
	t.type = 'STRING'
	return t

t_MINUS = r'\-'

def t_error(t):
	print(t)
	print('Illegal Characters')
	t.lexer.skip(1)


lexer = lex.lex()