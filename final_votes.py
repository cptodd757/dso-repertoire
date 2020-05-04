import pandas as pd 
import numpy as np 


def score(filename, point_values):
    df = pd.read_csv('survey-responses/votes.csv')

    points = {'First choice': point_values[0],
            'Second choice': point_values[1],
            'Third choice': point_values[2]}

    for option in points.keys():
        df = df.replace(option, points[option])

    totals = {}

    def rename(name):
        return name[(name.find('[')+1):-1]
    def get_totals(column):
        if 'stamp' in column.name:
            return
        column.name = rename(column.name)
        totals[column.name] = column.sum()

    df.apply(get_totals)
    results = pd.DataFrame.from_dict(totals, orient='index')
    results = results.sort_values(by=0,ascending=False)
    results.to_csv('results/' + filename + '.csv')

scorings = {'weighted':[3,2,1],
            'total-counts':[1,1,1],
            'firsts-only':[1,0,0]}

for s in scorings.keys():
    score(s,scorings[s])
