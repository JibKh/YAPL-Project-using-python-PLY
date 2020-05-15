import ply.lex as lex
import ply.yacc as yacc
import sys
from lexer import tokens

# ==================================== PARSER ====================================
def MyParser():

	# Precedence and remove ambiguity
	precedence = (
		('left', 'PLUS', 'MINUS'),
		('left', 'MULTIPLY', 'DIVIDE'),
		('left', 'POWER')
	)

	# calc is the starting point
	# var_declare is for delcaring a new variable without assigning it anything, for ex int a;
	# var_assign is for declaring a new variable AND assigning it a value
	# var_access is for assigning a value to an existing variable, for ex a = 50;
	# var_increment is to increment/decrement a variable
	# print is for printing an expression
	# expression is all of the arithmetic operations and list operations and logical operations etc.
	# do_while is for the do while loop
	# list is for declaring a new llist AND assigning it values. It can be left empty as well. For ex List a = [1,2,3] or List a = []
	# list_access_change is to access a list index and change its value. For ex a[0] = 55;
	# Called calc again at the end of each statement so that a big tree can be created with multiple statements.
	def p_calc(p):
		'''
		calc	:	var_declare SEMICOLON calc
				|	var_assign SEMICOLON calc
				|	var_access SEMICOLON calc
				|	var_increment SEMICOLON calc
				|	print SEMICOLON calc
				|	expression SEMICOLON calc
				|	do_while SEMICOLON calc
				|	list SEMICOLON calc
				|	list_access_change SEMICOLON calc
				|	empty
		'''
		#print('Look here: ', p[1])
		try:
			p[0] = (p[1], p[3])
			#print('Look here: ', p[0])
		except:
			None



	# ===============================================
	#												#
	#	START VARIABLE DECLARATION ONLY FUNCTIONS	#	
	#												#

	def p_var_declare(p):
		'''
		var_declare	:	TYPE_BOOL VAR_NAME
					|	TYPE_CHAR VAR_NAME
					|	TYPE_STRING VAR_NAME
					|	TYPE_INT VAR_NAME
					|	TYPE_DOUBLE VAR_NAME
		'''
		p[0] = ('declare', p[1], p[2])

	# ==== END VARIABLE DECLARATION ONLY FUNCTIONS ====


	# =======================================================
	#														#
	#	START VARIABLE DECLARATION + ASSIGNMENT FUNCTIONS	#	
	#														#

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


	# Next 4 are int operations. Was forced to make this since I had to ensure that int was assigned to only int.
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


	# =======================================
	#										#
	#	START VARIABLE ACCESS FUNCTIONS		#	
	#										#

	def p_var_access(p):
		'''
		var_access	:	VAR_NAME EQUALS expression
		'''
		p[0] = ('access', p[1], p[3])

	# ==== END VARIABLE ACCESS FUNCTIONS ====


	# =======================================
	#										#
	#	START VARIABLE INCREMENT FUNCTIONS	#	
	#										#

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


	# ===========================
	#							#
	#	START PRINT FUNCTIONS	#	
	#							#

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


	# ===============================
	#								#
	#	START DO WHILE FUNCTIONS	#	
	#								#

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


	# ===========================
	#							#
	#	START LIST FUNCTIONS	#	
	#							#

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


	# ===========================================
	#											#
	#	START LIST ACCESS + CHANGE FUNCTIONS	#	
	#											#

	def p_list_access_change(p):
		'''
		list_access_change	:	VAR_NAME LBRACK expression RBRACK EQUALS expression
		'''
		p[0] = ('list_access_change', p[1], p[3], p[6])

	# ==== END LIST ACCESS + CHANGE FUNCTIONS ====


	# ===================================
	#									#
	#	START EXPRESSIONS FUNCTIONS		#	
	#									#

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

	return yacc.yacc()