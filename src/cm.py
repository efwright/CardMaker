import cmfilehandler
from cmfilehandler import readfile
from cmlex import tokenize
from cmpreprocess import preprocess
from cmparse import parse
from cardmaker import make_card
from symbols import load_symbols

import sys

def get_name(filename):
    dot = filename.rfind('.')
    fslash = filename.rfind('/')
    if dot >= 0 and fslash >= 0:
        return filename[fslash+1:dot]

def run(filename, sympath, outdir):
    data = readfile(filename)
    tokens = tokenize(data)
    tokens = preprocess(tokens)
    ast = parse(tokens)
    symbols = load_symbols(sympath)
    card = make_card(ast, symbols)
    if ast.card_name == '':
        card.save(outdir + get_name(filename) + '.png')
    else:
        card.save(outdir + ast.card_name + '.png')

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3])

