# import rt_00_functions
import os
import pandas as pd


class EtherNetwork:
    modelName = None
    networkDF = None
    origFrq = None
    afterFrq = None
    trimmed = False
    A = 'NA'
    B = 'NA'
    a = 1
    b = 10
    periodList = None
    orgInfo = None
    topInfo = None
    tkOutFolder = None

    def __init__(self, modelName, fileLoc, timeFormat, outFolder):
        self.modelName = modelName
        self.networkDF = pd.DataFrame(columns=['from', 'to', 'time', 'value'])
        self.networkDF.read_csv(fileLoc, sep=' ')
        # TODO - change networkDF.time to appropriate format
        self.origFrq = pd.crosstab(self.networkDF, 'time')
        self.tkOutFolder = outFolder + '/' + modelName
        try:
            os.mkdir(self.tkOutFolder)
        except OSError():
            print("Creation of the directory %s failed" % self.tkOutFolder)
