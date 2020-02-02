import cmlex
from cmlex import tokens
import sys
import os
import yacc
import cmfilehandler

import PIL
from PIL import Image
from collections import OrderedDict

# AST
class Imagebox:
    def __init__(self):
        self.image = ''
        self.box = (0, 0, 0, 0)
        self.opacity = 1.0
    def set_image(self, image):
        self.image = image
    def set_box(self, box):
        self.box = box
    def set_opacity(self, opacity):
        self.opacity = opacity
    def __repr__(self):
        s  = 'Imagebox('
        s += self.image + ', '
        s += str(self.box) + ', '
        s += str(self.opacity) + ')'
        return s

class Textbox:
    def __init__(self):
        self.text = list()
        self.box = (0, 0, 0, 0)
        self.font = ''
        self.fontsize = 0
    def set_text(self, text):
        self.text = text
    def set_box(self, box):
        self.box = box
    def set_font(self, font):
        self.font = font
    def set_fontsize(self, fontsize):
        self.fontsize = fontsize
    def __repr__(self):
        s  = 'Textbox('
        s += str(self.text) + ', '
        s += str(self.box) + ', '
        s += self.font + ', '
        s += str(self.fontsize) + ')'
        return s

def read_image(filename):
    try:  
        img  = Image.open(cmfilehandler.path + filename)
        return img
    except IOError: 
        print('Could not load ' + filename)
        sys.exit(-1)

def crop_image(filename, x, y, w, h):
    img = read_image(filename)
    return img.crop((x, y, x+w, y+h))

def scale_image(filename, w, h):
    img = read_image(filename)
    return img.resize((w, h), resample=PIL.Image.LANCZOS)

class AST:
    def __init__(self):
        self.card_name = ''
        self.card_size = (0, 0)
        self.card_file = (-1, -1, -1)
        self.symtable = OrderedDict()
    def set_name(self, name):
        self.card_name = name
    def set_size(self, w, h):
        self.card_size = (w, h)
    def set_fill(self, r, g, b):
        self.card_fill = (r, g, b)
    def declare(self, ID, obj):
        self.symtable[ID] = obj
    def assign(self, ID, obj):
        self.symtable[ID] = obj
    def assign_textbox_text(self, ID, l):
        self.symtable[ID].text = l
    def assign_textbox_imagebox_box(self, ID, x, y, w, h):
        self.symtable[ID].box = (x, y, w, h)
    def assign_textbox_font(self, ID, font):
        self.symtable[ID].font = font
    def assign_textbox_fontsize(self, ID, fontsize):
        self.symtable[ID].fontsize = fontsize
    def assign_imagebox_image(self, ID, img):
        self.symtable[ID].image = img
    def assign_imagebox_opacity(self, ID, opacity):
        self.symtable[ID].opacity = opacity
    def __repr__(self):
        s  = 'AST(\n'
        s += '  Name: ' + self.card_name + '\n'
        s += '  Size: (' + str(self.card_size[0]) + ', ' + str(self.card_size[1]) + ')\n'
        s += '  Fill: ' + str(self.card_fill) + '\n'
        s += '  ' + str(self.symtable) + '\n'
        s += ')'
        return s

ast = None

#############################################################################
# Parse Rules
#############################################################################

def p_main(p):
    '''main : main statement '''

def p_main_empty(p):
    '''main : empty '''

def p_card_name(p):
    '''statement : CARDNAME '(' STRING ')' ';' '''
    ast.set_name(p[3])

def p_card_size(p):
    '''statement : CARDSIZE '(' NUMBER ',' NUMBER ')' ';' '''
    ast.set_size(int(p[3]), int(p[5]))

def p_card_fill(p):
    '''statement : CARDFILL '(' NUMBER ',' NUMBER ',' NUMBER ')' ';' '''
    ast.set_fill(int(p[3]), int(p[5]), int(p[7]))

def p_text_decl(p):
    '''statement : TEXT ID ';' '''
    ast.declare(p[2], '')

def p_text_assign(p):
    '''statement : ID '=' STRING ';' '''
    ast.assign(p[1], p[3])

def p_image_decl(p):
    '''statement : IMAGE ID ';' '''
    ast.declare(p[2], Image.new('RGBA', (0, 0)))

def p_image_assign_read_image(p):
    '''statement : ID '=' READIMAGE '(' STRING ')' ';' '''
    ast.assign(p[1], read_image(p[5]))

def p_image_assign_crop_image(p):
    '''statement : ID '=' CROPIMAGE '(' STRING ',' NUMBER ',' NUMBER ',' NUMBER ',' NUMBER ')' ';' '''
    ast.assign(p[1], crop_image(p[5], int(p[7]), int(p[9]), int(p[11]), int(p[13])))

def p_image_assign_scale_image(p):
    '''statement : ID '=' SCALEIMAGE '(' STRING ',' NUMBER ',' NUMBER ')' ';' '''
    ast.assign(p[1], scale_image(p[5], int(p[7]), int(p[9])))

def p_textbox_decl(p):
    '''statement : TEXTBOX ID ';' '''
    ast.declare(p[2], Textbox())

def p_textbox_assign_text(p):
    '''statement : ID '.' TEXTMEMBER '=' '[' idlist ']' ';' '''
    ast.assign_textbox_text(p[1], p[6])

def p_textbox_imagebox_assign_box(p):
    '''statement : ID '.' BOXMEMBER '=' '(' NUMBER ',' NUMBER ',' NUMBER ',' NUMBER ')' ';' '''
    ast.assign_textbox_imagebox_box(p[1], int(p[6]), int(p[8]), int(p[10]), int(p[12]))

def p_textbox_assign_font(p):
    '''statement : ID '.' FONTMEMBER '=' STRING ';' '''
    ast.assign_textbox_font(p[1], p[5])

def p_textbox_assign_fontsize(p):
    '''statement : ID '.' FONTSIZEMEMBER '=' NUMBER ';' '''
    ast.assign_textbox_fontsize(p[1], int(p[5]))

def p_imagebox_decl(p):
    '''statement : IMAGEBOX ID ';' '''
    ast.declare(p[2], Imagebox())

def p_imagebox_assign_image(p):
    '''statement : ID '.' IMAGEMEMBER '=' ID ';' '''
    ast.assign_imagebox_image(p[1], p[5])

def p_imagebox_assign_opacity(p):
    '''statement : ID '.' OPACITYMEMBER '=' NUMBER ';' '''
    ast.assign_imagebox_opacity(p[1], float(p[5])/100.0)

def p_id_list(p):
    '''idlist : ID '''
    p[0] = list([p[1]])

def p_id_list_recursive(p):
    '''idlist : idlist ',' ID '''
    p[0] = p[1] + list([p[3]])

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print(p)

class CMLex:
    def __init__(self, token_list):
        self.t = token_list
        self.i = 0
    def token(self):
        if self.i < len(self.t):
            self.i += 1
            return self.t[self.i-1]
        else:
            return None

def parse(token_list):
    global ast
    lexer = CMLex(token_list)
    parser = yacc.yacc(debug=False, write_tables=False, errorlog=yacc.NullLogger())
    ast = AST()
    parser.parse(lexer=lexer)
    return ast

