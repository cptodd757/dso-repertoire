import pandas as pd 
import numpy as np
from collections import Counter
from copy import copy

df = pd.read_csv('repertoire.csv')

pieces = []

# standardize composer names
nicknames = {'tchaik':'tchaikovsky',
             'rach':'rachmaninoff',
             'rachmaninov':'rachmaninoff',
             'shosty':'shostakovich'}
def handle_nickname(nickname):
    if nickname in nicknames.keys():
        return nicknames[nickname]
    return nickname 

# standardize piece names
# name: one person's version of naming a piece.
def consolidate(name):
    if 'romeo' in name:
        if 'tchaik' in name:
            return "tchaik romeo and juliet"
        if "prok" in name:
            return "prokofiev romeo and juliet"
    if "firebird" in name:
        return "firebird"
    if "scheh" in name:
        return "scheherazade"

    answer = name
    number = -1
    for i in range(1,10):
        if name.find(str(i)) != -1:
            composer = name[:name.find(' ')]
            answer = handle_nickname(composer) + ' ' + str(i)
            return answer
    return answer

def compile_pieces(row):
    global pieces
    pieces = pieces + [consolidate(name) for name in row['What pieces? (separate by commas)'].lower().split(', ')]

df.apply(compile_pieces,axis=1)

# count unique values, export to two lists, one sorted by name and one by count
counter = Counter(np.array(pieces))
counts = pd.DataFrame.from_dict(dict(counter),orient='index')
names = copy(counts)
names = names.sort_index()
names.to_csv('pieces_sorted.csv')

counts = counts.sort_values(by=0,ascending=False)
counts.to_csv('counts_sorted.csv')