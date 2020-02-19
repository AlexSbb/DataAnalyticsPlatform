import numpy as np
import json
import pycode.Team2Functions as T2F
import pycode.Filter as Smoothing
import pycode.NeuralNetworkFn as NN

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
        fil =  Smoothing.Filter()       
        # Amrita use an array of arrays like the input 
        smooothInput= [self.currentData]
        flag, beforeSmoothingArray, afterSmoothingArray, self.error = fil.moving_avg(smooothInput,self.window,self.smoothingType)
        # Amrita use an array of arrays like the output also, so I use only the first array
        self.beforeSmoothingArray = list(beforeSmoothingArray[0])
        self.afterSmoothingArray = list(afterSmoothingArray[0])

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

    def getDataSeriesDict(self):
         return self.dataSeriesDict
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    # def neuralNetwork(self, inputDataSeries, outputDataSeries, testSize, activationFunction, hiddenLayersInput, solverInput, iterationNumber, scalingOnOff):
    #     self.neuralNetworkResults = NN.NeuralNet(NN.NN_inputs(inputDataSeries,outputDataSeries,testSize,activationFunction,hiddenLayersInput,solverInput,iterationNumber,scalingOnOff))


    def changeDataSeriesForm(self, dataSeriesArray):
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
testDataSeries.smoothing()
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
inputSeries1.stdDev()
inputSeries1.smoothing()

print('original data \n', inputSeries1.originalData)
print('afterSmoothingArray \n', inputSeries1.afterSmoothingArray)

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

mergedSeries = testDataObject.changeDataSeriesForm([inputSeries1.originalData, inputSeries2.originalData])
print(mergedSeries)

print(inputSeries1.originalData)
print(inputSeries2.originalData)

# NN_outputs1 = NeuralNet(NN_inputs1)


# #Printing outputs
# print('Predicted Output:       ', NN_outputs1.y_test)
# print('test input:             ', NN_outputs1.X_test)
# print('expected output:        ', NN_outputs1.y_actual)
# print('length of output array: ', NN_outputs1.length)
# print('Mean Square error:      ', NN_outputs1.tst_mse)
# print('Accuracy:               ', NN_outputs1.tst_accrc)

