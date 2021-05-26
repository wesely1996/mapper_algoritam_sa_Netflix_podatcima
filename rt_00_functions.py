import pandas as pd
import matplotlib.pyplot as plt

def selectTop(dat, topSize=100):
    frqTo = dat['to'].sort(['to'], ascending=False)[1:topSize]
    frqFrom = dat['from'].sort(['from'], ascending=False)[1:topSize]
    topList = pd.DataFrame(data=[frqTo, frqFrom]).unique()
    return dat[dat['to'].isin(topList['to']) & dat['from'].isin(topList['from'])]

def plotGraph(edgeList, edgeWeight, x_label="edges", y_label="weights"):
    plt.plot(edgeList, edgeWeight)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def graphInfo(edgeList, edgeWeight):
    # TODO - napravi strukturu Stablo
    info = {'orgEdges': len(edgeList), 'orgNodes': len(edgeWeight), 'orgAvgDegree': None,
            'trimmedEdges': None, 'trimmedNodes': None, 'trimmedAvgDegree': None}
