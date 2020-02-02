# Build all cards from version 0.1 (early-alpha)

import sys
import os

import cm

if not os.path.exists('build'):
    os.makedirs('build')

for card_dir in os.listdir('cards'):
    card_full_dir = os.path.join('cards', card_dir)
    for f in os.listdir(card_full_dir):
        if f.endswith('.card'):
           card = os.path.join(card_full_dir, f)
           cm.run(card, '../../SymbolTable.csv', 'build/')

