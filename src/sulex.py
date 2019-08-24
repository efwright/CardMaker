# Tokenize the card file to be able to parse. Based on PLY (Python Lex-Yacc) https://www.dabeaz.com/ply/

import lex
import sys

# List of tokens
reserved = {
	'Paragraph'  : 'PARAGRAPH',
	'Image'      : 'IMAGE',
	'use'        : 'USE',
	'Textbox'    : 'TEXTBOX',
	'TEXT'       : 'TEXT',
	'FONT'       : 'FONT',
	'SIZE'       : 'SIZE',
	'WIDTH'      : 'WIDTH',
        'HEIGHT'     : 'HEIGHT',
	'PARAGRAPHS' : 'PARAGRAPHS',
	'FILE'       : 'FILE',
	'OPACITY'    : 'OPACITY',
	'File'       : 'IMAGEFILE',
	'size'       : 'CARDSIZE'
}

tokens = [
	'QUOTED_ID', 'ID', 'PERCENT', 'NUMBER'
] + list(reserved.values())

literals = "+=()[]{},;"

# Regular Expressions
# Need to allow " in quoted string
def t_QUOTED_ID(t):
	r'"[a-zA-Z_$][a-zA-Z_0-9.$]*"'
	t.type = reserved.get(t.value,'QUOTED_ID')
	if t.type == 'QUOTED_ID':
		t.value = t.value[1:len(t.value)-1]
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9.]*'
	t.type = reserved.get(t.value,'ID')
	return t

def t_PERCENT(t):
	r'([0-9]?[0-9]%|100%)'
	return t

def t_NUMBER(t):
	r'[1-9][0-9]*'
	return t

# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_COMMENT(t):
	r'\#.*'
	pass
	# No return value. Token discarded

# Error handling
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def tokenize(filename):
	try:
		f = open(filename, 'rb')
		data = f.read()
		f.close()
	except IOError:
		print("Could not find file " + filename)
		sys.exit(-2)

	lexer = lex.lex()

	lexer.input(data)
	ltokens = list()

	while True:
		tok = lexer.token()
		if not tok:
			break
		ltokens.append(tok)

	return ltokens

if __name__ == '__main__':
	print(tokenize(sys.argv[1]))

