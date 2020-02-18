import numpy as np
import json
import pycode.Team2Functions as T2F
import pycode.Filter as Smoothing


global inputData
global outputData
global modifiedInputData
global modifiedOutputData
linear = True
quadratic = False

backward = 'backward'
middle = 'fixed'
forward = 'forward'

inputData = ['none']
outputData = ['none']

global dataObject

class DataSeries:
    def __init__(self, name, dataSeries):

        self.currentData = dataSeries
        self.originalData = dataSeries
        self.name = name
        self.realMin = min(self.currentData)
        self.realMax = max(self.currentData)
        self.size = len(self.currentData)
        self.median = np.median(self.currentData)

        self.window = 2
        self.smoothingType = backward

        self.selectedMin = 0.0
        self.selectedMax = 1.0
        self.maxMinMatrix = []
        self.stdDevMaxMinMatrix = [] # what is this???
        self.stdDevFactor =  1.0
        self.interpolationType = linear #true for linear and false for quadratic interpolation
        self.interpolationArray = []
        self.replaceArray = []
        self.beforeSmoothingArray = []
        self.afterSmoothingArray = []

        self.error = ''

    def resetError(self):
        self.error = ''

    def setError(self, errorText):
        self.error = errorText
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def maxMin (self):
        self.replaceArray=T2F.MaxMin(self.currentData,self.selectedMax,self.selectedMin)

    def stdDev(self):
        self.replaceArray=T2F.StdDev(self.currentData,self.stdDevFactor)

    def interpolation(self):
        return('We dont have this function yet')   
   
    def smoothing(self):
        flag = False
        fil =  Smoothing.Filter()       
        # Amrita use an array of arrays like the input 
        smooothInput= [self.currentData] 
        flag, beforeSmoothingArray, afterSmoothingArray, self.error = fil.moving_avg(smooothInput,self.window,self.smoothingType)
        # Amrita use an array of arrays like the output also, so I use only the first array
        self.beforeSmoothingArray = list(beforeSmoothingArray[0])
        self.afterSmoothingArray = list(afterSmoothingArray[0])


class DataObject:
    def __init__(self, dataSeries, fileName):
         self.dataSeriesArray = []
         if fileName != '':
             fileName = 'series_'
         for i in range(len(dataSeriesArray)):
             print(i)
             print(dataSeriesArray[i])
             print(self.dataSeriesArray)
             self.dataSeriesArray.append(DataSeries(fileName + str(i), dataSeries[i]))


testDataSeries = DataSeries('myTestData',list(np.random.rand(100)))
# print (testDataSeries.currentData)
print ('realMax=',testDataSeries.realMax)
print ('realMin=',testDataSeries.realMin)
print ('median=',testDataSeries.median)
print ('_'*80)
# Test maxMin Function
testDataSeries.selectedMax = 0.9
testDataSeries.selectedMin = 0.1
testDataSeries.maxMin()
print ('replaceArray=',testDataSeries.replaceArray)
print ('_'*80)
# Test stdDev Function
testDataSeries.stdDev()
print ('replaceArray=',testDataSeries.replaceArray)
print ('_'*80)
# Test smoothing Function
testDataSeries.smoothing()
print (testDataSeries.error)
print ('beforeSmoothingArray')
print (testDataSeries.beforeSmoothingArray)
print ('afterSmoothingArray')
print (testDataSeries.afterSmoothingArray)

#print (testDataSeries.toJSON())
