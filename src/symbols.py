import csv
import sys
from PIL import Image


class Symbols:
    def __init__(self):
        self.sym = dict()
    def add(self, ID, filename):
        try:
            img = Image.open(filename)
            img = img.convert('RGBA')
            self.sym[ID] = img
        except IOError:
            print('Could not open ' + filename)
            sys.exit(-1)
    def get(self, ID):
        return self.sym[ID]
    def get_resized(self, ID, size):
        img = self.sym[ID]
        img = img.resize((size, size), resample=Image.LANCZOS)
        return img

def get_path(fullpath):
    i = fullpath.rfind('/')
    if i >= 0:
        return fullpath[0:i+1]
    else:
        return './'

def load_symbols(symfile):
    path = get_path(symfile)
    sym = Symbols()
    with open(symfile, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if len(row) < 2:
                continue
            sym.add(row[0].strip(), path+row[1].strip())
    return sym

