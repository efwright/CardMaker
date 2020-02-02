import cmfilehandler
from cmfilehandler import readfile
from cmlex import tokenize
from cmpreprocess import preprocess
from cmparse import parse
from cardmaker import make_card
from symbols import load_symbols

import sys

def run(filename, sympath, outdir):
    data = readfile(filename)
    tokens = tokenize(data)
    tokens = preprocess(tokens)
    ast = parse(tokens)
    symbols = load_symbols(sympath)
    card = make_card(ast, symbols)
    card.save(outdir + ast.card_name + '.png')

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3])

