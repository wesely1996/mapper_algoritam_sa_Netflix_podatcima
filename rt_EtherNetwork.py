import os
import pandas as pd
import rt_00_functions as rtf


class EtherNetwork:
    modelName = None
    networkDF = None
    origFrq = None
    afterFrq = None
    trimmed = False
    A = None
    B = None
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
        self.tkOutFolder = outFolder + '\\' + modelName
        try:
            os.mkdir(self.tkOutFolder)
        except OSError():
            print("Creation of the directory %s failed" % self.tkOutFolder)

    def dropExtreme(self, percentage=1 / 500):
        if not self.trimmed:
            rankDrop = len(self.networkDF) * percentage
            self.A = self.networkDF.sort_values(by=['value'], ascending=True)[rankDrop]
            self.A = self.networkDF.sort_values(by=['value'], ascending=False)[rankDrop]

            self.networkDF = self.networkDF[self.networkDF['value'] > self.A &
                                            self.networkDF['value'] < self.B]
            self.afterFrq = pd.crosstab(self.networkDF, 'time')
            self.trimmed = True
        else:
            print("The data set has already been trimmed.")

    def record(self):
        fileLoc = self.tkOutFolder + "\\dataSummary.txt"
        file = open(fileLoc, "w+")

        file.write("Original:\n")
        file.write(self.origFrq)
        file.write("Valid range: [" + self.A + ", " + self.B + "]\n")
        file.write("Value summery:\n")
        file.write(self.networkDF['value'].describe())

        file.close()

    def normalValues(self):
        value_list = self.networkDF['value']
        self.networkDF['value2'] = round(
            value_list.apply(lambda x: 1 / 1 + x - self.A) * (self.b - self.a) / (self.B - self.A), 5)

    def procOriginal(self, recordFolder, distFolder):
        recordFolder = self.tkOutFolder + "\\" + recordFolder
        distFolder = self.tkOutFolder + "\\" + distFolder

        try:
            os.mkdir(recordFolder)
        except OSError():
            print("Creation of the directory %s failed" % recordFolder)

        try:
            os.mkdir(distFolder)
        except OSError():
            print("Creation of the directory %s failed" % distFolder)

        self.periodList = self.networkDF['time'].unique()
        totalInfo = None
        file = open(recordFolder + "\\log.txt")
        for cur in self.periodList:
            periodDF = self.networkDF[self.networkDF['time'] == cur]
            file.write(cur)
            periodDF = rtf.selectTop(periodDF, topSize=len(self.networkDF))
            # TODO - finish function
