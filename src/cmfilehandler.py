import sys
import os

path = ''

def readfile(filename):
    global path
    closest = filename.rfind('/')
    if closest >= 0:
        path = filename[0:closest+1]
    try:
        f = open(filename, 'r')
        data = f.read()
        f.close()
    except IOError:
        print('Could not find file ' + filename)
        sys.exit(-1)

    return data

