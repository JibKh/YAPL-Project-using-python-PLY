import ply.lex as lex
import ply.yacc as yacc
import sys

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

# =========================== LEXER =================================

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

t_ignore = r'\n '

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
	r'List'
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
lexer.input("abc = 135435.63553")



# ==================================== PARSER ====================================

# Precedence and remove ambiguity
precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'MULTIPLY', 'DIVIDE'),
	('left', 'POWER')
)

# Expressions are any expressions like 1 + 1 or "Hello World"
# Var assign is for assigning new variables
def p_calc(p):
	'''
	calc	:	var_declare SEMICOLON
			|	var_assign SEMICOLON
			|	var_access SEMICOLON
			|	var_increment SEMICOLON
			|	print SEMICOLON
			|	expression SEMICOLON
			|	do_while SEMICOLON
			|	list SEMICOLON
			|	list_access_change SEMICOLON
			|	empty
	'''
	#print('Look here: ', p[1])
	run(p[1])


# ==== START LIST ACCESS CHANGE FUNCTIONS ====

def p_list_access_change(p):
	'''
	list_access_change	:	VAR_NAME LBRACK expression RBRACK EQUALS expression
	'''
	p[0] = ('list_access_change', p[1], p[3], p[6])

# ==== END LIST ACCESS CHANGE FUNCTIONS ====


# ==== START DO WHILE FUNCTIONS ====

def p_do_while(p):
	'''
	do_while	:	DO LBRACE do_expression WHILE LPARA expression RPARA
	'''
	p[0] = (p[1], p[3], p[6])

def p_do_expression(p):
	'''
	do_expression	:	multiple_expressions do_expression
					|	RBRACE
	'''
	try:
		p[0] = (p[1], p[2])
	except:
		return

def p_do_multiple_expressions(p):
	'''
	multiple_expressions	:	var_declare SEMICOLON
							|	var_assign SEMICOLON
							|	var_access SEMICOLON
							|	var_increment SEMICOLON
							|	print SEMICOLON
							|	expression SEMICOLON
							|	do_while SEMICOLON
							|	list SEMICOLON
							|	empty
	'''
	p[0] = p[1]

# ==== END DO WHILE FUNCTIONS ====



# ==== START LIST FUNCTIONS ====

def p_list(p):
	'''
	list	:	LIST VAR_NAME EQUALS LBRACK list_expression
	'''
	p[0] = ('list_assign', p[2], p[5])

def p_list_expression(p):
	'''
	list_expression	:	list_multiple_expressions COMMA list_expression
					|	list_multiple_expressions RBRACK
	'''
	try:
		p[0] = ('list', p[1], p[3])
	except:
		p[0] = ('list', p[1])

def p_list_multiple_expressions(p):
	'''
	list_multiple_expressions	:	var_declare
								|	var_assign
								|	var_access
								|	var_increment
								|	print
								|	expression
								|	do_while
								|	list
								|	empty
	'''
	p[0] = p[1]

# ==== END LIST FUNCTIONS ====



# ==== START PRINT FUNCTIONS ====

def p_print(p):
	'''
	print	:	PRINT LPARA print_expression RPARA 
	'''
	p[0] = p[3]

def p_print_expression(p):
	'''
	print_expression	:	expression COMMA print_expression
						|	expression
	'''
	try:
		p[0] = ('print', p[1], p[3])
	except:
		p[0] = ('print', p[1])

# ==== END PRINT FUNCTIONS ====



# ==== START VARIABLE ACCESS FUNCTIONS ====

def p_var_access(p):
	'''
	var_access	:	VAR_NAME EQUALS expression
	'''
	p[0] = ('access', p[1], p[3])

# ==== END VARIABLE ACCESS FUNCTIONS ====



# ==== START VARIABLE DECLARATION FUNCTIONS ====

def p_var_declare(p):
	'''
	var_declare	:	TYPE_BOOL VAR_NAME
				|	TYPE_CHAR VAR_NAME
				|	TYPE_STRING VAR_NAME
				|	TYPE_INT VAR_NAME
				|	TYPE_DOUBLE VAR_NAME
	'''
	p[0] = ('declare', p[1], p[2])

# ==== END VARIABLE DECLARATION FUNCTIONS ====



# ==== START VARIABLE DECLARATION + ASSIGNMENT FUNCTIONS ====

def p_var_assign(p):
	'''
	var_assign	:	type
	'''
	p[0] = ('assign', '=', (p[1][0], p[1][1]), p[1][2])

def p_type(p):
	'''
	type	:	TYPE_BOOL VAR_NAME EQUALS expression
			|	TYPE_CHAR VAR_NAME EQUALS CHAR
			|	TYPE_STRING VAR_NAME EQUALS expression
			|	TYPE_INT VAR_NAME EQUALS int_expression
			|	TYPE_DOUBLE VAR_NAME EQUALS expression
	'''
	p[0] = (p[1], p[2], p[4])


# Next 4 are int operations
def p_int_expression(p):
	'''
	int_expression	:	int_expression MULTIPLY int_expression
					|	int_expression DIVIDE int_expression
					|	int_expression PLUS int_expression
					|	int_expression MINUS int_expression
					|	int_expression MODULO int_expression
					|	int_expression POWER int_expression
	'''
	p[0] = (p[2], p[1], p[3])

def p_int_value(p):
	'''
	int_expression	:	INT
	'''
	p[0] = p[1]

def p_int_parentheses(p):
	'''
	int_expression	:	LPARA int_expression RPARA
	'''
	p[0] = (p[2])

def p_int_variable(p):
	'''
	int_expression	:	VAR_NAME
	'''
	p[0] = ('var', p[1])

# ==== END VARIABLE DECLARATION + ASSIGNMENT FUNCTIONS ====



# ==== START VARIABLE INCREMENT FUNCTIONS ====

def p_var_increment(p):
	'''
	var_increment	:	VAR_NAME var_func
	'''
	
	p[0] = ('var_increment', p[2], p[1])

def p_var_increment_func(p):
	'''
	var_func	:	INCREMENT
				|	DECREMENT
	'''
	p[0] = p[1]

# ==== END VARIABLE INCREMENT FUNCTIONS ====



# ==== START EXPRESSIONS FUNCTIONS ====

def p_expression(p):
	'''
	expression	:	expression MULTIPLY expression
				|	expression DIVIDE expression
				|	expression PLUS expression
				|	expression MINUS expression
				|	expression MODULO expression
				|	expression POWER expression
				|	expression LESSER expression
				|	expression GREATER expression
				|	expression GREATER_EQUAL expression
				|	expression LESSER_EQUAL expression
				|	expression NOT_EQUAL expression
				|	expression DOUBLE_EQUAL expression
				|	NOT expression
				|	expression AND expression
				|	expression OR expression
				|	VAR_NAME DOT INDEX LPARA expression RPARA
				|	VAR_NAME DOT SLICE LPARA expression COMMA expression RPARA
				|	VAR_NAME DOT POP LPARA expression RPARA
				|	VAR_NAME DOT PUSH LPARA expression RPARA
				|	VAR_NAME LBRACK expression RBRACK
	'''
	if p[1] == 'NOT':
		p[0] = (p[1], p[2])
	elif p[2] == '[':
		p[0] = ('list_access', p[1], p[3])
	elif p[3] == 'index':
		p[0] = ('list_access', p[1], p[5])
	elif p[3] == 'slice':
		p[0] = ('list_slice', p[1], (p[5], p[7]))
	elif p[3] == 'pop':
		p[0] = ('list_pop', p[1], p[5])
	elif p[3] == 'push':
		p[0] = ('list_push', p[1], p[5])
	else:
		p[0] = (p[2], p[1], p[3])

def p_expression_parentheses(p):
	'''
	expression	:	LPARA expression RPARA
	'''
	p[0] = (p[2])

def p_expression_val(p):
	'''
	expression	:	INT
				|	DOUBLE
				|	BOOL
				|	STRING
				|	CHAR
	'''
	p[0] = p[1]

def p_expression_var(p):
	'''
	expression	:	VAR_NAME
				|	MINUS VAR_NAME
	'''
	if p[1] == '-':
		p[0] = ('var', p[1]+p[2])
	else:
		p[0] = ('var', p[1])

# ==== END EXPRESSIONS FUNCTIONS ====


# == ERROR HANDLING ==

def p_error(p):
	print('TypeError p')

def p_empty(p):
	'''
	empty	:
	'''

	p[0] = None

parser = yacc.yacc()

env = {}
printString = ''

# ==================================== INTERPRETER ===================================

def run(p):
	global env
	global printString
	if type(p) == tuple:
		if p[0] == '+':
			try:
				return run(p[1]) + run(p[2])
			except Exception as e:
				print('TypeErorr + ', e)
			# val1 = run(p[1])
			# val2 = run(p[2])
			# if type(val1) == type(val2):
			# 	return run(p[1]) + run(p[2])
			# # if (type(val1) == type(val2)) | (type(val1) == 'double' & type(val2) == 'int') | (type(val2) == 'double' & type(val1) == 'int'):
			# # 	return int(run(p[1]) + run(p[2]))
			# else:
			# 	print('TypeError line 382')

		elif p[0] == '-':
			try:
				return run(p[1]) - run(p[2])
			except:
				print('TypeErorr -')

		elif p[0] == '*':
			try:
				return run(p[1]) * run(p[2])
			except:
				print('TypeErorr *')

		elif p[0] == '/':
			try:
				return run(p[1]) / run(p[2])
			except:
				print('TypeErorr /')

		elif p[0] == '%':
			try:
				return run(p[1]) % run(p[2])
			except:
				print('TypeErorr %')

		elif p[0] == '^':
			try:
				return run(p[1]) ** run(p[2])
			except:
				print('TypeErorr ^')

		elif p[0] == '<':
			try:
				return run(p[1]) < run(p[2])
			except:
				print('TypeErorr <')

		elif p[0] == '<=':
			try:
				return run(p[1]) <= run(p[2])
			except:
				print('TypeErorr <=')

		elif p[0] == '>':
			try:
				return run(p[1]) > run(p[2])
			except:
				print('TypeErorr >')

		elif p[0] == '>=':
			try:
				return run(p[1]) >= run(p[2])
			except:
				print('TypeErorr >=')

		elif p[0] == '!=':
			try:
				return run(p[1]) != run(p[2])
			except:
				print('TypeErorr !=')

		elif p[0] == '==':
			try:
				return run(p[1]) == run(p[2])
			except:
				print('TypeErorr ==')

		elif p[0] == 'NOT':
			try:
				return not run(p[1])
			except:
				print('TypeErorr NOT')

		elif p[0] == 'AND':
			try:
				return run(p[1]) and run(p[2])
			except:
				print('TypeErorr AND')

		elif p[0] == 'OR':
			try:
				return run(p[1]) or run(p[2])
			except:
				print('TypeErorr OR')

		elif p[0] == 'var_increment':
			if p[1] == '++':
				if p[2] not in env:
					return 'Undeclared variable found or something else'
				else:
					try:
						var_type = env[p[2]][0]
						val = env[p[2]][1] + 1
						final = (var_type, val)
						env[p[2]] = final
					except:
						print('Invalid operation')
				
			elif p[1] == '--':
				if p[2] not in env:
					return 'Undeclared variable found or something else'
				else:
					try:
						var_type = env[p[2]][0]
						val = env[p[2]][1] - 1
						final = (var_type, val)
						env[p[2]] = final
					except:
						print('Invalid operation')
			
			# elif p[1][0] == '=':
			# 	if p[2] not in env:
			# 		return 'Undeclared variable found or something else'
			# 	else:
			# 		return env[p[2]] = run(p[1][1])

			else:
				return 'Error in var'

		elif p[0] == 'declare':
			if p[2] not in env:
				env[p[2]] = (p[1], None)

		elif p[0] == 'assign':
			if p[2][1] not in env:
				if p[2][0] == 'string':
					val = run(p[3])
					if type(val) is str:
						env[p[2][1]] = (p[2][0], val)
					else:
						print('Cannot assign value to type string')
				elif p[2][0] == 'int':
					try:
						val = int(run(p[3]))
						env[p[2][1]] = (p[2][0], val)
					except:
						print('Cannot assign value to type int')
					# if type(run(p[3])) is int:
					# 	env[p[2][1]] = run(p[3])
					# else:
					# 	print('Cannot assign value to type int')
				elif p[2][0] == 'double':
					val = run(p[3])
					if (type(val) is float) | (type(val) is int):
						env[p[2][1]] = (p[2][0], val)
					else:
						print('Cannot assign value to type double')
				elif p[2][0] == 'char':
					val = run(p[3])
					if (type(val) is str) & (len(val) <= 1 ):
						env[p[2][1]] = (p[2][0], val)
					else:
						print('Cannot assign value to type char')
				elif p[2][0] == 'bool':
					val = run(p[3])
					if type(val) is bool:
						env[p[2][1]] = (p[2][0], val)
					else:
						print('Cannot assign value to type bool')
				else:
					return 'Invalid type'
			else:
				print('RedeclarationError')

		elif p[0] == 'access':
			if p[1] in env:
				val = run(p[2])
				if (type(val).__name__ == env[p[1]][0]) | ((type(val) is float) & (env[p[1]][0] == 'double')) | ((type(val) is int) & (env[p[1]][0] == 'double')):
					var_type = env[p[1]][0]
					final = (var_type, val)
					env[p[1]] = final
				else:
					print('TypeError access')
			else:
				print('Variable does not exist')

		elif p[0] == 'var':
			if p[1][0] == '-':
				if p[1][1:] not in env:
					print('Undeclared variable found')
					return
				else:
					if (env[p[1][1:]][0] == "int") | (env[p[1][1:]][0] == "double"):
						return -env[p[1][1:]][1]
			else:
				if p[1] not in env:
					print('Undeclared variable found')
					return
				else:
					return env[p[1]][1]
			# if p[1] not in env:
			# 	print('Undeclared variable found')
			# 	return
			# else:
			# 	return env[p[1]][1]

		elif p[0] == 'print':
			printString = printString + str(run(p[1]) if run(p[1]) != None else '') + ' '
			try:
				run(p[2])
			except:
				print(printString)
				printString = ''
			
		elif p[0] == 'DO':
			temp = p[1]
			while True:
				#scope_var = {}
				while True:
					run(temp[0])
					if temp[1] != None:
						temp = temp[1]
					else:
						break
				if not run(p[2]):
					break
		
		elif p[0] == 'list_assign':
			if p[1] not in env:
				env[p[1]] = ('list', run(p[2]))
				if env[p[1]][1][0] == None:
					env[p[1]] = ('list', [])
				
			else:
				print('Redeclaration error')

		elif p[0] == 'list_access':
			try:
				return env[p[1]][1][p[2]]
			except Exception as e:
				errorVal = str(e)
				if errorVal[1:-1] == p[1]:
					print('Variable does not exist')
				else:
					print(e)

		elif p[0] == 'list_slice':
			try:
				if (p[2][1] > len(env[p[1]][1])) | (p[2][0] > len(env[p[1]][1])):
					print('IndexOutOfBoundsError')
				else:
					return env[p[1]][1][p[2][0]:p[2][1]]
			except Exception as e:
				errorVal = str(e)
				if errorVal[1:-1] == p[1]:
					print('Variable does not exist')
				else:
					print('boop', e)

		elif p[0] == 'list_pop':
			try:
				return env[p[1]][1].pop(p[2])
			except Exception as e:
				errorVal = str(e)
				if errorVal[1:-1] == p[1]:
					print('Variable does not exist')
				else:
					print(e)

		elif p[0] == 'list_push':
			try:
				return env[p[1]][1].append(p[2])
			except Exception as e:
				errorVal = str(e)
				if errorVal[1:-1] == p[1]:
					print('Variable does not exist')
				else:
					print(e)

		elif p[0] == 'list':
			if len(p) < 3:
				return [run(p[1])]

			test = [run(p[1])] + run(p[2])
			return test

		elif p[0] == 'list_access_change':
			try:
				env[p[1]][1][run(p[2])] = run(p[3])
			except Exception as e:
				print('Error: ', e)

		else:
			return False

	else:
		return p

while True:
	try:
		s = input('>> ')
	except EOFError:
		break

	parser.parse(s)