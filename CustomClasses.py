import numpy as np
import json
import pycode.Team2Functions as T2F
import pycode.Filter as Smoothing
import pycode.NeuralNetworkFn as NN
import pycode.RandomForestFn as RF

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

        self.neuralNetworkResults = []

    def resetToOriginalData(self):
        self.currentData = self.originalData
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
        self.neuralNetworkResults = []

    def resetError(self):
        self.error = ''

    def setError(self, errorText):
        self.error = errorText
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def maxMin (self, selectedMax=None, selectedMin=None):
        if selectedMax is None or selectedMin is None:
            if self.selectedMax is None or self.selectedMin is None:
                self.selectedMax = self.realMax
                self.selectedMin = self.realMin
        elif selectedMax != None and selectedMin != None:
            self.selectedMax = selectedMax
            self.selectedMin = selectedMin
        self.replaceArray=T2F.MaxMin(self.currentData, self.selectedMax, self.selectedMin)

    def stdDev(self, stdDevFactor=None):
        if stdDevFactor is None:
            if self.stdDevFactor is None:
                self.stdDevFactor = 1
        else:
            self.stdDevFactor = stdDevFactor
        self.replaceArray=T2F.StdDev(self.currentData,self.stdDevFactor)

    def interpolation(self):
        return('We dont have this function yet')   
   
    def smoothing(self, smoothingType, window):
        fil =  Smoothing.Filter()       
        # Amrita use an array of arrays like the input 
        smoothInput= [self.currentData]
        # flag, beforeSmoothingArray, afterSmoothingArray, self.error = fil.moving_avg(smoothInput,self.window,self.smoothingType)
        # Amrita use an array of arrays like the output also, so I use only the first array
        # self.beforeSmoothingArray = list(beforeSmoothingArray[0])
        # self.afterSmoothingArray = list(afterSmoothingArray[0])

class DataObject:
    def __init__(self, dataSeries, fileName):
         self.dataSeriesDict = {} #stores the dataseries in a dictionary
         if fileName == '':
             fileName = 'series_'
         for i in range(len(dataSeries)):
             self.dataSeriesDict[fileName + '_' + str(i+1)] = DataSeries(fileName + '_' + str(i+1), dataSeries[i])
             
    def addSeries(self, dataSeries, fileName):
         if fileName == '':
             fileName = 'series_'
         for i in range(len(dataSeries)):
             seriesNameTemp = fileName + '_'  + str(i+1)
             while seriesNameTemp in self.dataSeriesDict:
                 seriesNameTemp = seriesNameTemp + '_' + str(i+1)
             self.dataSeriesDict[seriesNameTemp] = DataSeries(seriesNameTemp, dataSeries[i])

    #checks if a series with that name is in the dictionary and deletes it if it is.
    def deleteSeries(self, seriesName):
        if seriesName in self.dataSeriesDict:
            self.dataSeriesDict.pop(seriesName)

    def clearSeries(self):
         self.dataSeriesDict.clear()

    def resetToOriginalData(self):
        for i in range(len(self.dataSeriesDict)):
            self.dataSeriesDict[i].resetToOriginalData()

    def getDataSeriesDict(self):
         return self.dataSeriesDict
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    # def neuralNetwork(self, inputDataSeries, outputDataSeries, testSize, activationFunction, hiddenLayersInput, solverInput, iterationNumber, scalingOnOff):
    #     self.neuralNetworkResults = NN.NeuralNet(NN.NN_inputs(inputDataSeries,outputDataSeries,testSize,activationFunction,hiddenLayersInput,solverInput,iterationNumber,scalingOnOff))

def changeDataSeriesForm(dataSeriesArray):
    convertedArray = []
    if len(dataSeriesArray) == 0:
        return 'ERROR: no arrays attached'
    for i in range(len(dataSeriesArray)):
        if len(dataSeriesArray[0]) != len(dataSeriesArray[i]):
            return 'ERROR: arrays of different sizes'
    for i in range(len(dataSeriesArray[0])): #the length of the arrays
        tempArray = []
        for ii in range(len(dataSeriesArray)): #the number of arrays
            tempArray.append(dataSeriesArray[ii][i])
        convertedArray.append(tempArray)
    return convertedArray


testDataSeries = DataSeries('myTestData',list(np.random.rand(100)))
inputSeries1 = DataSeries('input1',list(np.random.rand(100)))
inputSeries2 = DataSeries('input2',list(np.random.rand(100)))
outputSeries = DataSeries('output',list(np.random.rand(100)))
# print (testDataSeries.currentData)
# print ('realMax=',testDataSeries.realMax)
# print ('realMin=',testDataSeries.realMin)
# print ('median=',testDataSeries.median)
# print ('_'*80)
# Test maxMin Function
testDataSeries.selectedMax = 0.9
testDataSeries.selectedMin = 0.1
testDataSeries.maxMin()
#print ('replaceArray=',testDataSeries.replaceArray)
#print ('_'*80)
# Test stdDev Function
testDataSeries.stdDev()
#print ('replaceArray=',testDataSeries.replaceArray)
#print ('_'*80)
# Test smoothing Function
testDataSeries.smoothing("backward", 2)
#print (testDataSeries.error)
#print ('beforeSmoothingArray')
#print (testDataSeries.beforeSmoothingArray)
#print ('afterSmoothingArray')
#print (testDataSeries.afterSmoothingArray)

#print (testDataSeries.toJSON())

inputSeries1 = DataSeries('input1',list(np.random.rand(20)))
inputSeries2 = DataSeries('input2',list(np.random.rand(20)))
outputSeries = DataSeries('output',list(np.random.rand(20)))

testDataObject = DataObject([inputSeries1.originalData ,inputSeries2.originalData], 'input')
testDataObject.addSeries([list(np.random.rand(10)), list(np.random.rand(10))], 'output')
# print (testDataObject.getDataSeriesDict())

#NN_inputs1 = NN_inputs(X1,y1,0.2,actv1[3],hid_lyrs1,slvr1[1],200,False)     # Activation=relu, solver=sgd
actv1 = ("identity", "logistic", "tanh", "relu")
slvr1 = ("lbfgs", "sgd", "adam")
#Tuple of hidden layers in Neural Networks
hid_lyrs1 = (8,4,4)

inputSeries1.selectedMax = 0.9
inputSeries1.selectedMin = 0.1
inputSeries1.maxMin()
# inputSeries1.stdDev()
# inputSeries1.smoothing()

# print('original data \n', inputSeries1.originalData)
# print('afterSmoothingArray \n', inputSeries1.afterSmoothingArray)

# Input array (In final implementation there should be a choice to select between processed input and raw input)
X1 = [   [4.5,6.7],
         [8.9,3.8],
         [9,6.8],
         [12.3,8.8] ]

# output dataset (raw or processed selection)           
y1 = [8.55055,5.53195,9.1547,11.91745]
# print(outputSeries.originalData)
# print('above is the output array')
# NN_outputs1 = NN.NeuralNet(NN.NN_inputs([inputSeries1, inputSeries2], outputSeries, 0.2, actv1[3], hid_lyrs1, slvr1[1], 200, False))

# # #Printing outputs
# print('Predicted Output:       ', NN_outputs1.y_test)
# print('test input:             ', NN_outputs1.X_test)
# print('expected output:        ', NN_outputs1.y_actual)
# print('length of output array: ', NN_outputs1.length)
# print('Mean Square error:      ', NN_outputs1.tst_mse)
# print('Accuracy:               ', NN_outputs1.tst_accrc)

#TESTING THE NEURAL NETWORKS
# NN_outputs1 = NN.NeuralNet(NN.NN_inputs(changeDataSeriesForm([inputSeries1.originalData, inputSeries2.originalData]), outputSeries.originalData, 0.5, actv1[3], hid_lyrs1, slvr1[1], 200, False))

# #Printing outputs
# print('Predicted Output:       ', NN_outputs1.y_test)
# print('test input:             ', NN_outputs1.X_test)
# print('expected output:        ', NN_outputs1.y_actual)
# print('length of output array: ', NN_outputs1.length)
# print('Mean Square error:      ', NN_outputs1.tst_mse)
# print('Accuracy:               ', NN_outputs1.tst_accrc)

# # Input structure for Neural Network
# class RF_inputs(NamedTuple):
#     X: float
#     y: float
#     trees: int
#     tst_siz: float

# # Output structure for Neural Network
# class RF_outputs(NamedTuple):
#     flag:       str
#     y_test:     float
#     X_test:     float 
#     y_actual:   float
#     length:     int
#     tst_mse:    float
#     tst_accrc:  float
#     msg:        str
# # Function call

#TESTING THE RANDOM FOREST

# RF_outputs1 = RF.RFreg(RF.RF_inputs(changeDataSeriesForm([inputSeries1.originalData, inputSeries2.originalData]),outputSeries.originalData,1000,0.2))

# #Printing outputs
# print('Predicted Output:       ', RF_outputs1.y_test)
# print('test input:             ', RF_outputs1.X_test)
# print('expected output:        ', RF_outputs1.y_actual)
# print('length of output array: ', RF_outputs1.length)
# print('Mean Square error:      ', RF_outputs1.tst_mse)
# print('Accuracy:               ', RF_outputs1.tst_accrc)
