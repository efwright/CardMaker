# Read through the parse results and convert everything to classes. Variable names get resolved here. Next step is to convert the classes to the actual image.

from suparse import parse
import sys
from collections import OrderedDict

# Paragraph(text, font, size(%))
class Paragraph:
	def __init__(self):
		self.text = ""
		self.font = ""
		self.size = 0.0
		self.percent = False
	def __str__(self):
		pval = '%' if self.percent else ''
		return 'Paragraph(' + self.text + ', ' + self.font + ', ' + str(int(self.size)) + pval + ')'
	def __repr__(self):
		pval = '%' if self.percent else ''
		return 'Paragraph(' + self.text + ', ' + self.font + ', ' + str(int(self.size)) + pval + ')'

# Textbox(width(%), height(%), font, size(%), list(Paragraph))
class Textbox:
	def __init__(self):
		self.width = 0.0
		self.wpercent = False
		self.height = 0.0
		self.hpercent = False
		self.font = ""
		self.size = 0.0
		self.percent = False
		self.paragraphs = list()
	def __str__(self):
		wp = '%' if self.wpercent else ''
		hp = '%' if self.hpercent else ''
		sp = '%' if self.percent else ''
		return 'Textbox(' + str(int(self.width)) + wp + ', ' + str(int(self.height)) + hp + ', ' + self.font + ', ' + str(int(self.size)) + sp + ', ' + str(self.paragraphs) + ')'
	def __repr__(self):
		wp = '%' if self.wpercent else ''
		hp = '%' if self.hpercent else ''
		sp = '%' if self.percent else ''
		return 'Textbox(' + str(int(self.width)) + wp + ', ' + str(int(self.height)) + hp + ', ' + self.font + ', ' + str(int(self.size)) + sp + ', ' + str(self.paragraphs) + ')'

# File(filename)
class File:
	def __init__(self):
		self.name = ""
	def __str__(self):
		return 'File(' + self.name + ')'
	def __repr__(self):
		return 'File(' + self.name + ')'

# Image(filename, width(%), height(%), opacity%)
class Image:
	def __init__(self):
		self.file = ""
		self.width = 0.0
		self.wpercent = False
		self.height = 0.0
		self.hpercent = False
		self.opacity = 0.0
	def __str__(self):
		wp = '%' if self.wpercent else ''
		hp = '%' if self.hpercent else ''
		return 'Image(' + self.file + ', ' + str(int(self.width)) + wp + ', ' + str(int(self.height)) + hp + ', ' + str(int(self.opacity)) + '%)'
	def __repr__(self):
		wp = '%' if self.wpercent else ''
		hp = '%' if self.hpercent else ''
		return 'Image(' + self.file + ', ' + str(int(self.width)) + wp + ', ' + str(int(self.height)) + hp + ', ' + str(int(self.opacity)) + '%)'

# Global values that will be returned from interpret fuction
variables = OrderedDict()
card_width = 0
card_height = 0

def create_paragraph(statement):
	val = Paragraph()
	val.text = statement[2]
	val.font = statement[3]
	size_len = len(statement[4])
	if size_len > 0:
		if statement[4][size_len-1] == '%':
			val.size = float(statement[4][:size_len-1])
			val.percent = True
		else:
			val.size = float(statement[4])
	return val

def interpret_paragraph(statement):
	if isinstance(statement[2], tuple):
		construct = statement[2]
		if not construct[0] == 'construct':
			print('Internal error: expected construct, saw ' + construct[0])
			sys.exit(-1)
		if not construct[1] == 'paragraph':
			print('Cannot assign paragraph')
			sys.exit(-1)
		return create_paragraph(construct)
	else:
		if not isinstance(variables[statement[2]], Paragraph):
			print('Cannot assign paragraph')
			sys.exit(-1)
		return variables[statement[2]]

def create_textbox(statement):
	val = Textbox()
	v_length = len(statement[2])
	if v_length > 0:
		if statement[2][v_length-1] == '%':
			val.width = float(statement[2][:v_length-1])
			val.wpercent = True
		else:
			val.width = float(statement[2])
	v_length = len(statement[3])
	if v_length > 0:
		if statement[3][v_length-1] == '%':
			val.height = float(statement[3][:v_length-1])
			val.hpercent = True
		else:
			val.height = float(statement[3])
	val.font = statement[4]
	v_length = len(statement[5])
	if v_length > 0:
		if statement[5][v_length-1] == '%':
			val.size = float(statement[5][:v_length-1])
			val.percent = True
		else:
			val.size = float(statement[5])
	for para in statement[6]:
		if para[0] == 'construct':
			val.paragraphs.append(create_paragraph(para))
		elif para[0] == 'read':
			val.paragraphs.append(variables[para[2]])
	return val

def interpret_textbox(statement):
	if isinstance(statement[2], tuple):
		construct = statement[2]
		if not construct[0] == 'construct':
			print('Internal error: expected construct, saw ' + construct[0])
			sys.exit(-1)
		if not construct[1] == 'textbox':
			print('Cannot assign textbox')
			sys.exit(-1)
		return create_textbox(construct)
	else:
		if not isinstance(variables[statement[2]], Textbox):
			print('Cannot assign textbox')
			sys.exit(-1)
		return variables[statement[2]]

def create_file(statement):
	val = File()
	val.name = statement
	return val

def interpret_file(statement):
	return create_file(statement[2])

def create_image(statement):
	val = Image()
	if isinstance(statement[2], tuple):
		val.file = variables[statement[2][2]].name
	else:
		val.file = statement[2]

	v_length = len(statement[3])
	if v_length > 0:
		if statement[3][v_length-1] == '%':
			val.width = float(statement[3][:v_length-1])
			val.wpercent = True
		else:
			val.width = float(statement[3])

	v_length = len(statement[4])
	if v_length > 0:
		if statement[4][v_length-1] == '%':
			val.height = float(statement[4][:v_length-1])
			val.hpercent = True
		else:
			val.height = float(statement[4])

	v_length = len(statement[5])
	if v_length > 0:
		val.opacity = float(statement[5][:v_length-1])

	return val

def interpret_image(statement):
	if isinstance(statement[2], tuple):
		construct = statement[2]
		if not construct[0] == 'construct':
			print('Internal error: expected construct, saw ' + construct[0])
			sys.exit(-1)
		if not construct[1] == 'image':
			print('Cannot assign image')
			sys.exit(-1)
		return create_image(construct)
	else:
		if not isinstance(variables[statement[2]], Image):
			print('Cannot assign image')
			sys.exit(-1)
		return variables[statement[2]]

def interpret_single(statement):
	global card_width, card_height
	if statement[0] == 'declare':
		if statement[1] == 'paragraph':
			variables[statement[2]] = Paragraph()
		elif statement[1] == 'textbox':
			variables[statement[2]] = Textbox()
		elif statement[1] == 'file':
			variables[statement[2]] = File()
		elif statement[1] == 'image':
			variables[statement[2]] = Image()
		else:
			print('Internal error: attempted to declare invalid type ' + statement[1])
			sys.exit(-1)
	elif statement[0] == 'assign':
		if isinstance(variables[statement[1]], Paragraph):
			variables[statement[1]] = interpret_paragraph(statement)
		if isinstance(variables[statement[1]], Textbox):
			variables[statement[1]] = interpret_textbox(statement)
		if isinstance(variables[statement[1]], File):
			variables[statement[1]] = interpret_file(statement)
		if isinstance(variables[statement[1]], Image):
			variables[statement[1]] = interpret_image(statement)
	elif statement[0] == 'size':
		card_width = int(statement[1])
		card_height = int(statement[2])
	else:
		print('Internal error: statement ' + statement[0])
		sys.exit(-1)

def interpret(parse_output):
	for statement in parse_output:
		interpret_single(statement)
	return (variables, card_width, card_height)

if __name__ == '__main__':
	interpret(parse(sys.argv[1]))
