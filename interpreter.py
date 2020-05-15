import ply.lex as lex
import ply.yacc as yacc
import sys
from parserT import MyParser

# ==================================== INTERPRETER ===================================

env = {} # Handles all the variables
printString = '' # Handles print statements

def run(p):
	global env
	global printString
	if type(p) == tuple: # If its a tuple it means there is a tree. If not, its a single item like a number or string.

		# Adds values
		if p[0] == '+':
			try:
				return run(p[1]) + run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Subtracts values
		elif p[0] == '-':
			try:
				return run(p[1]) - run(p[2])
			except Exception as e:
				print('TypeErorr:', e)
		
		# Multiplies values
		elif p[0] == '*':
			try:
				return run(p[1]) * run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Divides values
		elif p[0] == '/':
			try:
				return run(p[1]) / run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Modulo of values
		elif p[0] == '%':
			try:
				return run(p[1]) % run(p[2])
			except Exception as e:
				print('TypeErorr:', e)
		
		# Raises to the power
		elif p[0] == '^':
			try:
				return run(p[1]) ** run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Smaller than
		elif p[0] == '<':
			try:
				return run(p[1]) < run(p[2])
			except Exception as e:
				print('TypeErorr:', e)
		
		# Smaller than equals to
		elif p[0] == '<=':
			try:
				return run(p[1]) <= run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Greater than
		elif p[0] == '>':
			try:
				return run(p[1]) > run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Greater than equals to
		elif p[0] == '>=':
			try:
				return run(p[1]) >= run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Not equals to
		elif p[0] == '!=':
			try:
				return run(p[1]) != run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Equals Equals
		elif p[0] == '==':
			try:
				return run(p[1]) == run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# NOT
		elif p[0] == 'NOT':
			try:
				return not run(p[1])
			except Exception as e:
				print('TypeErorr:', e)
		
		# AND
		elif p[0] == 'AND':
			try:
				return run(p[1]) and run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# OR
		elif p[0] == 'OR':
			try:
				return run(p[1]) or run(p[2])
			except Exception as e:
				print('TypeErorr:', e)

		# Increments or decrements a variable
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
					except Exception as e:
						print('Invalid operation:', e)
				
			elif p[1] == '--':
				if p[2] not in env:
					return 'Undeclared variable found or something else'
				else:
					try:
						var_type = env[p[2]][0]
						val = env[p[2]][1] - 1
						final = (var_type, val)
						env[p[2]] = final
					except Exception as e:
						print('Invalid operation:', e)
			else:
				return 'Error in var'

		# Declare a new variable without assigning it a value. Does not include lists here.
		elif p[0] == 'declare':
			if p[2] not in env:
				env[p[2]] = (p[1], None)

		# Declare and assign a value to a new variable. Does not include lists here.
		elif p[0] == 'assign':
			if p[2][1] not in env:
				if p[2][0] == 'string':
					val = run(p[3])
					if type(val) is str:
						env[p[2][1]] = (p[2][0], val)
						return ('scope', p[2][1])
					else:
						print('Cannot assign value to type string')
				elif p[2][0] == 'int':
					try:
						val = int(run(p[3]))
						env[p[2][1]] = (p[2][0], val)
						return ('scope', p[2][1])
					except Exception as e:
						print('Cannot assign value to type int:', e)
					# if type(run(p[3])) is int:
					# 	env[p[2][1]] = run(p[3])
					# else:
					# 	print('Cannot assign value to type int')
				elif p[2][0] == 'double':
					val = run(p[3])
					if (type(val) is float) | (type(val) is int):
						env[p[2][1]] = (p[2][0], val)
						return ('scope', p[2][1])
					else:
						print('Cannot assign value to type double')
				elif p[2][0] == 'char':
					val = run(p[3])
					if (type(val) is str) & (len(val) <= 1 ):
						env[p[2][1]] = (p[2][0], val)
						return ('scope', p[2][1])
					else:
						print('Cannot assign value to type char')
				elif p[2][0] == 'bool':
					val = run(p[3])
					if type(val) is bool:
						env[p[2][1]] = (p[2][0], val)
						return ('scope', p[2][1])
					else:
						print('Cannot assign value to type bool')
				else:
					return 'Invalid type'
			else:
				print('RedeclarationError')

		# You can access a variable and change the value here. a = 5; or b = 5.0;
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

		# Returns the value of a variable
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

		# Print statement
		elif p[0] == 'print':
			printString = printString + str(run(p[1]) if run(p[1]) != None else '') + ' '
			try:
				run(p[2])
			except:
				print(printString)
				printString = ''
			
		# Executes a do loop
		elif p[0] == 'DO':
			while True: # Start of do loop. This allows it to happens the first time in the DO. It breaks when while loop is false.
				temp = p[1]
				scope_var = [] # Used to keep track of all scope variables. The variables are added to env and using this scope_var we delete it from env.
				while True: # Goes through all the statements in the DO loop
					val = run(temp[0])
					try:
						if val[0] == 'scope':
							scope_var.append(val[1])
					except:
						None
					if temp[1] != None:
						temp = temp[1]
					else:
						break
				for var in scope_var: # Delete the scope variables from env at the end of each loop
					del env[var] 
				if not run(p[2]): # WHILE STATEMENT
					break
				
		# Creates a new list and recursively adds it to the variables
		elif p[0] == 'list_assign':
			if p[1] not in env:
				env[p[1]] = ('list', run(p[2])) # run(p[2]) will return a list which contains all the values. It will be added recursively using the elif p[0] == 'list'
				if env[p[1]][1][0] == None: # Checks if its and empty list
					env[p[1]] = ('list', [])
				
			else:
				print('Redeclaration error')

		# Returns the value of a list index
		elif p[0] == 'list_access':
			try:
				return env[p[1]][1][p[2]]
			except Exception as e:
				errorVal = str(e)
				if errorVal[1:-1] == p[1]:
					print('Variable does not exist')
				else:
					print(e)

		# Slices a list
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
					print(e)

		# Pops a list
		elif p[0] == 'list_pop':
			try:
				return env[p[1]][1].pop(p[2])
			except Exception as e:
				errorVal = str(e)
				if errorVal[1:-1] == p[1]:
					print('Variable does not exist')
				else:
					print(e)

		# Pushes into a list
		elif p[0] == 'list_push':
			try:
				return env[p[1]][1].append(p[2])
			except Exception as e:
				errorVal = str(e)
				if errorVal[1:-1] == p[1]:
					print('Variable does not exist')
				else:
					print(e)

		# Adds values to the new list when you create the list for the first time
		elif p[0] == 'list':
			if len(p) < 3: # Base case
				return [run(p[1])]

			test = [run(p[1])] + run(p[2])
			return test

		# Access and change a value in the list. a[0] = 20;
		elif p[0] == 'list_access_change':
			try:
				env[p[1]][1][run(p[2])] = run(p[3])
			except Exception as e:
				print('Error: ', e)

		else:
			return False

	else:
		return p # Return the string or int or any single item that is not a tuple

# HANDLE INPUTS

if len(sys.argv) < 2:
	print('Please input a text file')
else:
	
	file = open('test_cases/'+sys.argv[1])
	text = file.read()
	text = text.replace('\n', '').replace('\t', '')
	result = MyParser().parse(text)
	while True: # Keeps going until the end of the result
		run(result[0]) # First tree
		if result[1] != None:
			result = result[1] # Next tree
		else:
			break