import numpy as np
import json
import pycode.Filter as Filter
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
        self.interpolationType = linear 
        # 0 - Linear Interpolation
        # 1 - Quadratic Interpolation
        self.interpolationArray = []
        self.replaceArray = []
        self.valPercent = 0
        self.beforeSmoothingArray = []
        self.afterSmoothingArray = []

        self.PredictedOutput = []
        self.ExpectedOutput = []
        self.TestInput = []
        
        self.MeanSquareError =0
        self.Accuracy=0


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
        self.valPercent = 0
        self.beforeSmoothingArray = []
        self.afterSmoothingArray = []
        self.error = ''
        self.neuralNetworkResults = []
        self.PredictedOutput = []
        self.ExpectedOutput = []
        self.TestInput = []
        
        self.MeanSquareError =0
        self.Accuracy=0


    def resetError(self):
        self.error = ''

    def setError(self, errorText):
        self.error = errorText
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def maxMin (self):
        print("I am in maxMin in maxMin")
        filterObj = Filter.Filter()
        flag,valPercent,replaceArray,msg =filterObj.maxMin(self.originalData, self.selectedMax, self.selectedMin)
        if flag == 'error':
            print('Error:')
            print(msg)
            self.error=msg
        else:
            self.replaceArray = replaceArray
            self.valPercent = valPercent

    def standardDeviation(self, stdDevFactor=None):
        if stdDevFactor is None:
            if self.stdDevFactor is None:
                self.stdDevFactor = 1
        else:
            self.stdDevFactor = stdDevFactor
        # TO DO / QUESTION (Dessi Thursday): 
        # What does maxValue and minValue mean here? Do we really want to overwrite our self.selectedMax, self.selectedMin? 
        # I thought we are only using max and min for the hard limits.
        filterObj = Filter.Filter()
        flag, valPercent, replaceArray, selectedMax, selectedMin, msg = filterObj.stdDev(self.originalData,self.stdDevFactor)
        if flag == 'error':
            print('Error:')
            print(msg)
            self.error=msg
        else:
            self.replaceArray = replaceArray
            self.valPercent = valPercent
            self.selectedMax = selectedMax
            self.selectedMin = selectedMin
    
    def interpolation(self, max=None, min=None, interpolationType=None):
        if max is None:
            if self.selectedMax is None:
                self.selectedMax = self.realMax
        else: 
            self.selectedMax = max
        if min is None:
            if self.selectedMin is None:
                self.selectedMin = self.realMin
        else:
            self.selectedMin = min
        # We are not setting the replace array anywhere. Either we or them needs to run their max min method, so that it is produced. 
        filterObj = Filter.Filter()
        # print("selectedMax= ", self.selectedMax)
        # print("selectedMin= ", self.selectedMin)
        # print("interpolationType= ", self.interpolationType)
        # print('0 - Linear Interpolation, 1 - Quadratic Interpolation ')
        flag, InterpolatedMatrix, msg = filterObj.interpolation(self.originalData, self.replaceArray, self.interpolationType, self.selectedMax, self.selectedMin)
        if flag == 'error':
            print('Error:')
            print(msg)
            self.error=msg
        else:
            self.currentData = InterpolatedMatrix

   
    def smoothing(self, smoothingType=None, window=None):
        print("Hi, I'm smoothing")
        filterObj = Filter.Filter()    
        smoothInput= [self.currentData]
        flag, revisedInputarr, newarr, msg = filterObj.movingAvg(smoothInput,self.window,self.smoothingType)
        if flag == 'error':
            print('Error:')
            print(msg)
            self.error=msg
        else:
            self.currentData = list(newarr[0])
            self.originalData = list(revisedInputarr[0])
            # Amrita use an array of arrays like the output also, so I use only the first array
            # self.beforeSmoothingArray = list(beforeSmoothingArray[0])
            # self.afterSmoothingArray = list(afterSmoothingArray[0])
    
    def randonForest(self, inputSeriesData,trees,testSize,historyOnOff):
        print('Hi, Im random forest')
        rfInput = RF.RF_inputs(changeDataSeriesForm(inputSeriesData), self.currentData,trees,testSize/100,historyOnOff)
        RF_outputs=RF.RFreg(rfInput)
        if (RF_outputs.flag=="success"): 
            self.ExpectedOutput=RF_outputs.y_actual
            self.PredictedOutput = RF_outputs.y_test
            self.TestInput =  RF_outputs.X_test
            self.MeanSquareError = RF_outputs.test_mean_squared_error
            self.Accuracy= RF_outputs.test_accuracy
        else:
            print('Error:')
            print(RF_outputs.message)
            self.error = RF_outputs.message
        #Printing outputs
        # print('Predicted Output:       ', RF_outputs.y_test)
        # print('test input:             ', RF_outputs.X_test)
        # print('expected output:        ', RF_outputs.y_actual)
        # print('length of output array: ', RF_outputs.length)
        # print('Mean Square error:      ', RF_outputs.tst_mse)
        # print('Accuracy:               ', RF_outputs.tst_accrc)
        # print('flag:                   ', RF_outputs.flag)
    def neuralNetwork(self,inputSeriesData, testSize,activeFunction,hiddenLayers,solverFunction,iterations,scalingOnOff ):
        print('Hi, Im neuralNetwork')

        NnInput = NN.NN_inputs(changeDataSeriesForm(inputSeriesData), self.currentData, testSize/100, activeFunction.lower(), hiddenLayers, solverFunction.lower(), iterations, scalingOnOff)
      
        # print("inputSeriesData",NnInput.X)
        # print("NnInput.y",NnInput.y)
        # print("NnInput.test_size)",NnInput.test_size)
        # print("activation_fun)",NnInput.activation_fun)
        # print("hidden_layers)",NnInput.hidden_layers)
        # print("solver_fun)",NnInput.solver_fun)
        # print("iterations)",NnInput.iterations)
        # print("scaling",NnInput.scaling)
        NN_outputs = NN.NeuralNet(NnInput)
        if (NN_outputs.flag=="success"): 
            self.ExpectedOutput     = NN_outputs.y_actual
            self.PredictedOutput    = NN_outputs.y_test
            self.TestInput          = NN_outputs.X_test
            self.MeanSquareError    = NN_outputs.test_mean_squared_error
            self.Accuracy           = NN_outputs.test_accuracy
        else:
            print('Error:')
            print(NN_outputs.message)
            self.error = NN_outputs.message      
        # print('flag:                   ', NN_outputs.flag)
        # print('Predicted Output:       ', NN_outputs.y_test)
        # print('test input:             ', NN_outputs.X_test)
        # print('expected output:        ', NN_outputs.y_actual)
        # print('length of output array: ', NN_outputs.length)
        # print('Mean Square error:      ', NN_outputs.test_mean_squared_error)
        # print('Accuracy:               ', NN_outputs.test_accuracy)



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







# testDataSeries = DataSeries('myTestData',list(np.random.rand(100)))
# inputSeries1 = DataSeries('input1',list(np.random.rand(100)))
# inputSeries2 = DataSeries('input2',list(np.random.rand(100)))
# outputSeries = DataSeries('output',list(np.random.rand(100)))

# print ('realMax=',testDataSeries.realMax)
# print ('realMin=',testDataSeries.realMin)
# print ('median=',testDataSeries.median)
# print ('_'*80)
# Test maxMin Function
# testDataSeries.selectedMax = 0.9
# testDataSeries.selectedMin = 0.1
# testDataSeries.maxMin()


# Test stdDev Function
# testDataSeries.standardDeviation()
# print ('replaceArray=',testDataSeries.replaceArray)
# print ('_'*80)

# print(testDataSeries.currentData)
# print ('replaceArray=',testDataSeries.replaceArray)
# print(testDataSeries.selectedMax)
# print(testDataSeries.selectedMin)


# testDataSeries.interpolation()

# Test smoothing Function
# testDataSeries.smoothing("backward", 2)
#print (testDataSeries.error)
#print ('beforeSmoothingArray')
#print (testDataSeries.beforeSmoothingArray)
#print ('afterSmoothingArray')
#print (testDataSeries.afterSmoothingArray)

#print (testDataSeries.toJSON())

# inputSeries1 = DataSeries('input1',list(np.random.rand(20)))
# inputSeries2 = DataSeries('input2',list(np.random.rand(20)))
# outputSeries = DataSeries('output',list(np.random.rand(20)))

# testDataObject = DataObject([inputSeries1.originalData ,inputSeries2.originalData], 'input')
# testDataObject.addSeries([list(np.random.rand(10)), list(np.random.rand(10))], 'output')
# print (testDataObject.getDataSeriesDict())

#NN_inputs1 = NN_inputs(X1,y1,0.2,actv1[3],hid_lyrs1,slvr1[1],200,False)     # Activation=relu, solver=sgd
# actv1 = ("identity", "logistic", "tanh", "relu")
# slvr1 = ("lbfgs", "sgd", "adam")
#Tuple of hidden layers in Neural Networks
# hid_lyrs1 = (8,4,4)

# inputSeries1.selectedMax = 0.9
# inputSeries1.selectedMin = 0.1
# inputSeries1.maxMin()
# inputSeries1.stdDev()
# inputSeries1.smoothing()

# print('original data \n', inputSeries1.originalData)
# print('afterSmoothingArray \n', inputSeries1.afterSmoothingArray)

# Input array (In final implementation there should be a choice to select between processed input and raw input)
# X1 = [   [4.5,6.7],
#          [8.9,3.8],
#          [9,6.8],
#          [12.3,8.8] ]

# output dataset (raw or processed selection)           
# y1 = [8.55055,5.53195,9.1547,11.91745]
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


