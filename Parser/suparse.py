import sulex
from sulex import tokens
import sys
import os
import yacc

# Parsing Rules

#######################################################################
# M A I N 
#######################################################################

def p_main(p):
	'''main : main statement '''
	p[0] = p[1] + p[2]

def p_main_empty(p):
	'''main : empty '''
	p[0] = list()

#######################################################################
# S T A T E M E N T 
#######################################################################

def p_statement_decl(p):
	'''statement : decl ';' '''
	p[0] = [("declare",) + p[1]]

def p_statement_assign(p):
	'''statement : ID '=' construct ';' '''
	p[0] = [("assign", p[1], p[3])]

def p_statement_decl_and_assign(p):
	'''statement : decl '=' construct ';' '''
	p[0] = [("declare",) + p[1], ("assign", p[1][1], p[3])]

#######################################################################
# D E C L 
#######################################################################

def p_decl(p):
	'''decl : type ID '''
	p[0] = (p[1], p[2])

#######################################################################
# T Y P E
#######################################################################

def p_type_paragraph(p):
	'''type : PARAGRAPH '''
	p[0] = "paragraph"

def p_type_image(p):
	'''type : IMAGE '''
	p[0] = "image"

def p_type_textbox(p):
	'''type : TEXTBOX '''
	p[0] = "textbox"

def p_type_file(p):
	'''type : IMAGEFILE '''
	p[0] = "file"

#######################################################################
# C O N S T R U C T 
#######################################################################

def p_construct_file(p):
	'''construct : QUOTED_ID '''
	p[0] = p[1]

def p_construct_paragraph(p):
	'''construct : PARAGRAPH '(' pbody ')' '''
	p[0] = ("construct", "paragraph", p[3][0], p[3][1], p[3][2])

def p_construct_image(p):
	'''construct : IMAGE '(' ibody ')' '''
	p[0] = ("construct", "image", p[3][0], p[3][1], p[3][2], p[3][3])

def p_construct_textbox(p):
	'''construct : TEXTBOX '(' tbody ')' '''
	p[0] = ("construct", "textbox", p[3][0], p[3][1], p[3][2], p[3][3], p[3][4])

#######################################################################
# P A R A G R A P H   C O N S T R U C T O R   B O D Y 
#######################################################################

def p_pbody_empty(p):
	'''pbody : empty '''
	p[0] = ["","",""]

def p_pbody_single(p):
	'''pbody : pbody_exp '''
	p[0] = p[1]

def p_pbody_getmany(p):
	'''pbody : pbody_many '''
	p[0] = p[1]

def p_pbody_many(p):
	'''pbody_many : pbody_many ',' pbody_exp '''
	p[0] = ["","",""]
	if len(p[1][0]) > 0:
		p[0][0] = p[1][0]
	if len(p[1][1]) > 0:
		p[0][1] = p[1][1]
	if len(p[1][2]) > 0:
		p[0][2] = p[1][2]
	if len(p[3][0]) > 0:
		p[0][0] = p[3][0]
	if len(p[3][1]) > 0:
		p[0][1] = p[3][1]
	if len(p[3][2]) > 0:
		p[0][2] = p[3][2]

def p_pbody_many_default(p):
	'''pbody_many : pbody_exp '''
	p[0] = p[1]

def p_pbody_exp_text(p):
	'''pbody_exp : TEXT '=' QUOTED_ID '''
	p[0] = [p[3], "", ""]

def p_pbody_exp_font(p):
	'''pbody_exp : FONT '=' QUOTED_ID '''
	p[0] = ["", p[3], ""]

def p_pbody_exp_size(p):
	'''pbody_exp : SIZE '=' NUMBER 
               | SIZE '=' PERCENT'''
	p[0] = ["", "", p[3]]

#######################################################################
# I M A G E   C O N S T R U C T O R   B O D Y 
#######################################################################

def p_ibody_empty(p):
	''' ibody : empty '''
	p[0] = ["","","",""]

def p_ibody_single(p):
	'''ibody : ibody_exp '''
	p[0] = p[1]

def p_ibody_getmany(p):
	'''ibody : ibody_many '''
	p[0] = p[1]

def p_ibody_many(p):
	'''ibody_many : ibody_many ',' ibody_exp '''
	p[0] = ["","","",""]
	if len(p[1][0]) > 0:
		p[0][0] = p[1][0]
	if len(p[1][1]) > 0:
		p[0][1] = p[1][1]
	if len(p[1][2]) > 0:
		p[0][2] = p[1][2]
	if len(p[1][3]) > 0:
		p[0][3] = p[1][3]
	if len(p[3][0]) > 0:
		p[0][0] = p[3][0]
	if len(p[3][1]) > 0:
		p[0][1] = p[3][1]
	if len(p[3][2]) > 0:
		p[0][2] = p[3][2]
	if len(p[3][3]) > 0:
		p[0][3] = p[3][3]

def p_ibody_many_default(p):
	'''ibody_many : ibody_exp '''
	p[0] = p[1]

def p_ibody_exp_file(p):
	'''ibody_exp : FILE '=' QUOTED_ID '''
	p[0] = [p[3], "", "", ""]

def p_ibody_exp_file_var(p):
	'''ibody_exp : FILE '=' ID '''
	p[0] = [("read", "file", p[3]), "", "", ""]

def p_ibody_exp_width(p):
	'''ibody_exp : WIDTH '=' NUMBER 
               | WIDTH '=' PERCENT '''
	p[0] = ["", p[3], "", ""]

def p_ibody_exp_height(p):
	'''ibody_exp : HEIGHT '=' NUMBER 
               | HEIGHT '=' PERCENT '''
	p[0] = ["", "", p[3], ""]

def p_ibody_exp_opacity(p):
	'''ibody_exp : OPACITY '=' PERCENT ''' 
	p[0] = ["", "", "", p[3]]

#######################################################################
# T E X T B O X   C O N S T R U C T O R   B O D Y 
#######################################################################

def p_tbody_empty(p):
	'''tbody : empty '''
	p[0] = ["","","","",list()]

def p_tbody_single(p):
	'''tbody : tbody_exp '''
	p[0] = p[1]

def p_tbody_getmany(p):
	'''tbody : tbody_many '''
	p[0] = p[1]

def p_tbody_many_default(p):
	'''tbody_many : tbody_exp '''
	p[0] = p[1]

def p_tbody_many(p):
	'''tbody_many : tbody_many ',' tbody_exp '''
	p[0] = ["","","","",p[1][4] + p[3][4]]
	if len(p[1][0]) > 0:
		p[0][0] = p[1][0]
	if len(p[3][0]) > 0:
		p[0][0] = p[1][0]

	if len(p[1][1]) > 0:
		p[0][1] = p[1][1]
	if len(p[3][1]) > 0:
		p[0][1] = p[3][1]

	if len(p[1][2]) > 0:
		p[0][2] = p[1][2]
	if len(p[3][2]) > 0:
		p[0][2] = p[3][2]

	if len(p[1][3]) > 0:
		p[0][3] = p[1][3]
	if len(p[3][3]) > 0:
		p[0][3] = p[3][3]

def p_tbody_exp_width(p):
	'''tbody_exp : WIDTH '=' NUMBER 
               | WIDTH '=' PERCENT '''
	p[0] = [p[3], "", "", "", list()]

def p_tbody_exp_height(p):
	'''tbody_exp : HEIGHT '=' NUMBER 
               | HEIGHT '=' PERCENT '''
	p[0] = ["", p[3], "", "", list()]

def p_tbody_exp_font(p):
	'''tbody_exp : FONT '=' QUOTED_ID '''
	p[0] = ["", "", p[3], "", list()]

def p_tbody_exp_size(p):
	'''tbody_exp : SIZE '=' NUMBER 
               | SIZE '=' PERCENT '''
	p[0] = ["", "", "", p[3], list()]

def p_tbody_exp_para(p):
	'''tbody_exp : PARAGRAPHS '=' '[' para_list ']' '''
	p[0] = ["", "", "", "", p[4]]

def p_para_list_empty(p):
	'''para_list : empty '''
	p[0] = list()

def p_para_list_single(p):
	'''para_list : para_exp '''
	p[0] = p[1]

def p_para_list_getmany(p):
	'''para_list : para_many '''
	p[0] = p[1]

def p_para_many_default(p):
	'''para_many : para_exp '''
	p[0] = p[1]

def p_para_many(p):
	'''para_many : para_many ',' para_exp '''
	p[0] = p[1] + p[3]

def p_para_exp(p):
	'''para_exp : construct '''
	p[0] = [p[1]]

def p_para_exp_id(p):
	'''para_exp : ID '''
	p[0] = [("read", "paragraph", p[1])]

def p_empty(p):
	'empty :'
	p[0] = list()

def p_error(p):
	print(p)

#######################################################################
# E N D   P A R S E R   R U L E S 
#######################################################################

# Handle use imports
def expand_use(tokens, path):
	index = 0
	while index < len(tokens):
		if tokens[index].type == 'USE':
			end = verify_syntax_use(tokens, index)
			use_filename = os.path.join(path, tokens[index+1].value)
			tokens = tokens[:index] + sulex.tokenize(use_filename) + sublist(tokens, end)
		else:
			index += 1
	return tokens

def verify_syntax_use(tokens, index):
	if len(tokens) <= index+1:
		print("Expected filename after 'use', but saw end-of-file instead. ")
		sys.exit(-1)
	if tokens[index+1].type != 'QUOTED_ID':
		print("Expected filename after 'use', but saw " + tokens[index+1].value + " instead. ")
		sys.exit(-1)
	if len(tokens) <= index+2:
		print("Expected ; after filename, but saw end-of-file instead. ")
		sys.exit(-1)
	if tokens[index+2].type != ';':
		print("Expected ; after filename.")
		sys.exit(-1)
	return index+3

def sublist(tokens, index):
	if len(tokens) > index:
		return tokens[index:]
	else:
		return list()

# Custom lexer for yacc

def create_lex():
	return SULex()

class SULex:
	def __init__(self):
		self.t = list()
		self.i = 0
	def tokenize(self, filename):
		self.t = sulex.tokenize(filename)
		self.t = expand_use(self.t, os.path.dirname(os.path.abspath(filename)))
		self.i = 0
	def token(self):
		if self.i < len(self.t):
			self.i += 1
			return self.t[self.i-1]
		else:
			return None

# Parse
def parse(filename):
	lexer = create_lex()
	lexer.tokenize(filename)
	parser = yacc.yacc(debug=False, write_tables=False, errorlog=yacc.NullLogger())
	return parser.parse(lexer=lexer)

### Main
if __name__ == '__main__':
	print(parse(sys.argv[1]))

