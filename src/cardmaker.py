from cmparse import Imagebox, Textbox, AST
from symbols import Symbols
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

symbols = None

def process_imagebox(card, ast, ib):
    dim = ib.box
    img = ast.symtable[ib.image]
    opacity = ib.opacity
    img.putalpha(int(opacity*255))
    w, h = img.size
    offset = (dim[0], dim[1])
    if w != dim[2] or h != dim[3]:
        print("Warning: width of image does not match.")
    card.alpha_composite(img, offset)
    return card

def create_font(font, fontsize):
    return ImageFont.truetype('../fonts/' + font, fontsize)

def get_max_size(font):
    max_w = 0
    max_h = 0
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
        w, h = font.getsize(c)
        max_w = max(max_w, w)
        max_h = max(max_h, h)
    return (max_w, max_h)

def get_sentence_size(font, text):
    return font.getsize(text)

def text_to_image(font, text):
    size = get_sentence_size(font, text)
    img = Image.new('RGBA', size)
    d = ImageDraw.Draw(img)
    d.text((0,0), text, font=font, fill=(0,0,0))
    return img

class Sentence:
    def __init__(self, font, word):
        self.text = word
        self.image = text_to_image(font, word)
        self.font = font
    def size(self):
        return self.image.size
    def append(self, word):
        self.text += ' ' + word
        self.image = text_to_image(self.font, self.text)
    def pop(self):
        i = self.text.rfind(' ')
        if i >= 0:
            self.text = self.text[:i]
            self.image = text_to_image(self.font, self.text)
        elif len(self.text) > 0:
            self.text = ''
            self.image = text_to_image(self.font, self.text)
    def empty(self):
        return len(self.text) <= 0

def load_symbol(sym, size, gap):
    img = symbols.get_resized(sym, size)
    w,h = img.size
    gapimg = Image.new('RGBA', (w+gap*2,h))
    gapimg.alpha_composite(img, (gap, 0))
    return gapimg

class Symbol:
    def __init__(self, font, sym):
        self.font = font
        self.symbol = sym[2:-1]
        w, h = get_max_size(font)
        self.image = load_symbol(self.symbol, w, self.get_gap())
    def size(self):
        return self.image.size
    def get_gap(self):
        w,h = get_sentence_size(self.font, ' ')
        return w

class Line:
    def __init__(self, font):
        self.font = font
        self.parts = list()
        w, h = get_max_size(font)
        self.height = h
        self.image = Image.new('RGBA', (0,0))
    def get_height(self):
        height = 0
        for part in self.parts:
            w,h = part.size()
            height = max(height, h)
        return height
    def get_width(self):
        width = 0
        for part in self.parts:
            w,h = part.size()
            width += w
        return width
    def update_image(self):
        width = self.get_width()
        height = self.get_height()
        self.image = Image.new('RGBA', (width, height))
        x = 0
        for part in self.parts:
            w,h = part.size()
            h_off = height-h
            self.image.alpha_composite(part.image, (x, h_off))
            x += w
    def add_word(self, word):
        if len(self.parts) <= 0:
            self.parts.append(Sentence(self.font, word))
        elif isinstance(self.parts[-1], Symbol):
            self.parts.append(Sentence(self.font, word))
        else:
            self.parts[-1].append(word)
        self.update_image()
    def add_symbol(self, symbol):
        self.parts.append(Symbol(self.font, symbol))
        self.update_image()
    def size(self):
        return self.image.size
    def pop(self):
        if len(self.parts) <= 0:
            return
        elif isinstance(self.parts[-1], Symbol):
            self.parts = self.parts[:-1]
        else:
            self.parts[-1].pop()
            if self.parts[-1].empty():
                self.parts = self.parts[:-1]
        self.update_image()
    def empty(self):
        return len(self.parts) <= 0

def create_paragraph(font, width, fulltext):
    lines = list()
    lines.append(Line(font))
    words = fulltext.split(' ')
    for word in words:
        if word[0] == '$':
            lines[-1].add_symbol(word)
        else:
            lines[-1].add_word(word)
        w,h = lines[-1].size()
        if w > width:
            w,h = lines[-1].size()
            if w > 0:
                lines[-1].pop()
                lines.append(Line(font))
                if word[0] == '$':
                    lines[-1].add_symbol(word)
                else:
                    lines[-1].add_word(word)
    max_w,max_h = get_max_size(font)
    h = 0
    img = Image.new('RGBA', (width, max_h*len(lines)))
    for line in lines:
        img.alpha_composite(line.image, (0, h))
        h += max_h
    return img

def make_textbox(paragraphs, width, height):
    img = Image.new('RGBA', (width, height))
    tot_height = 0
    for p in paragraphs:
        w,h = p.size
        tot_height += h
    gap = int((float(height - tot_height)/2.0)/len(paragraphs))
    y = gap
    for p in paragraphs:
        w,h = p.size
        img.alpha_composite(p, (0, y))
        y += h + gap
    return img

def process_textbox(card, ast, tb):
    width = tb.box[2]
    height = tb.box[3]
    fontsize = tb.fontsize
    while fontsize > 0:
        font = create_font(tb.font, fontsize)

        paragraphs = list()
        for ID in tb.text:
            text = ast.symtable[ID]
            paragraphs.append(create_paragraph(font, width, text))
        min_height = 0
        for paragraph in paragraphs:
            w,h = paragraph.size
            min_height += h

        if min_height <= height:
            textbox_img = make_textbox(paragraphs, width, height)
            break

        fontsize -= 1
        
    card.alpha_composite(textbox_img, (tb.box[0], tb.box[1]))
    return card

def make_card(ast, sym):
    global symbols
    symbols = sym

    if ast.card_fill[0] < 0:
        card = Image.new('RGBA', ast.card_size)
    else:
        color = (ast.card_fill[0], ast.card_fill[1], ast.card_fill[2], 255)
        card = Image.new('RGBA', ast.card_size, color)
    for key, value in ast.symtable.items():
        if isinstance(value, str):
            continue
        if isinstance(value, Image.Image):
            continue
        if isinstance(value, Imagebox):
            card = process_imagebox(card, ast, value)
        if isinstance(value, Textbox):
            card = process_textbox(card, ast, value)
    return card

