from interpret_card import interpret, Paragraph, Textbox, File, Image
import sys
from suparse import parse

def build_textbox(var, width, height):
	None

def build_image(var, width, height):
	None

def build(variables, width, height):
	for var in variables:
		if isinstance(var, Textbox):
			build_textbox(var, width, height)
		elif isinstance(var, Image):
			build_image(var, width, height)

if __name__ == '__main__':
	parse_tree = parse(sys.argv[1])
	card_variables, card_width, card_height = interpret(parse_tree)
	print(card_variables)
	print(card_width)
	print(card_height)
	build(card_variables, card_width, card_height)
