
class EtherNetwork:

	modelName = None
	networkDF = None
	origFrq = None
	afterFrq = None
	trimed = False
	A = NA
	B = NA
	a = 1
	b = 10
	periodList = None
	orgInfo = None
	topInfo = None
	tkOutFolder = None
	
	def __init__(modelName, fileLoc, timeFormat, outFolder):
		self.modelName = modelName
		#read data from data folder
