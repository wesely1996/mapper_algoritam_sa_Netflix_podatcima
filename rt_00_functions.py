import pandas as pd


def selectTop(dat, topSize=100):
    frqTo = dat['to'].sort(['to'], ascending=False)[1:topSize]
    frqFrom = dat['from'].sort(['from'], ascending=False)[1:topSize]
    topList = pd.DataFrame(data=[frqTo, frqFrom]).unique()
    return dat[dat['to'].isin(topList['to']) & dat['from'].isin(topList['from'])]
