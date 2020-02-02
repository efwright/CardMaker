import lex
import sys

# List of tokens
reserved = {
    'use'  : 'USE',
    'card_size' : 'CARDSIZE',
    'card_name' : 'CARDNAME',
    'card_fill' : 'CARDFILL',
    'Image' : 'IMAGE',
    'Imagebox' : 'IMAGEBOX',
    'Text' : 'TEXT',
    'Textbox' : 'TEXTBOX',
    'read_image' : 'READIMAGE',
    'crop_image' : 'CROPIMAGE',
    'scale_image' : 'SCALEIMAGE',
    'image' : 'IMAGEMEMBER',
    'box' : 'BOXMEMBER',
    'opacity' : 'OPACITYMEMBER',
    'text' : 'TEXTMEMBER',
    'font' : 'FONTMEMBER',
    'fontsize' : 'FONTSIZEMEMBER'
}

tokens = [
    'STRING', 'ID', 'PERCENT', 'NUMBER'
] + list(reserved.values())

literals = '+=()[],;.'

def t_STRING(t):
    r'"[a-zA-Z/.][a-zA-Z_0-9./\-$() ]*"'
    t.type = reserved.get(t.value, 'STRING')
    if t.type == 'STRING':
        t.value = t.value[1:len(t.value)-1]
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_PERCENT(t):
	r'([0-9]?[0-9]%|100%)'
	return t

def t_NUMBER(t):
	r'[1-9][0-9]*|0'
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_COMMENT(t):
	r'\#.*'
	pass

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def tokenize(text):
	lexer = lex.lex()

	lexer.input(text)
	ltokens = list()

	while True:
		tok = lexer.token()
		if not tok:
			break
		ltokens.append(tok)

	return ltokens

