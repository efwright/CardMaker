import cmlex
import cmfilehandler
from cmfilehandler import readfile
import sys

def preprocess(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index].type == 'USE':
            if index+1 >= len(tokens):
                print('Expected filename after "use" but saw end-of-file')
                sys.exit(-1)
            elif tokens[index+1].type == 'STRING':
                if index+2 >= len(tokens):
                    print('Expected ; after filename but saw end-of-file')
                    sys.exit(-1)
                elif tokens[index+2].type == ';':
                    data = readfile(cmfilehandler.path + tokens[index+1].value)
                    use_tokens = cmlex.tokenize(data)
                    tokens = tokens[:index] + use_tokens + tokens[index+3:]
                else:
                    print('Expected ; after filename.')
                    sys.exit(-1)
            else:
                print('Expected filename after "use".')
                sys.exit(-1)
        else:
            index += 1
    return tokens

