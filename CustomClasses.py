import numpy as np
import json
import pycode.Filter as Filter
import pycode.NeuralNetworkFn as NN
import pycode.RandomForestFn as RF

# Defining the global variables
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

# Defining the global variable containing all 
# the data series and their respective attributes
global dataObject

# Defining the DataSeries class
# This class contains each data series and its attributes.
# The class has a number of functions to import, change and delete its attributes.
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

        self.stdDevFactor =  1.0
        self.interpolationType = linear 
        # 0 - Linear Interpolation
        # 1 - Quadratic Interpolation
        self.interpolationArray = []
        self.replaceArray = []
        self.valPercent = 0

        self.PredictedOutput = []
        self.ExpectedOutput = []
        self.TestInput = []
        
        self.MeanSquareError =0
        self.Accuracy=0

        self.error = ''

        self.maxMinMatrix = []
        self.stdDevMaxMinMatrix = [] 

    # resets all attributes to their original values and deletes any information about
    # manipulation of the data series
    def resetToOriginalData(self):
        self.currentData = self.originalData
        self.window = 2
        self.smoothingType = backward
        self.selectedMin = 0.0
        self.selectedMax = 1.0
        self.maxMinMatrix = []
        self.stdDevMaxMinMatrix = [] 
        self.stdDevFactor =  1.0
        self.interpolationType = linear 
        self.interpolationArray = []
        self.replaceArray = []
        self.valPercent = 0
        self.error = ''

        self.PredictedOutput = []
        self.ExpectedOutput = []
        self.TestInput = []
        
        self.MeanSquareError =0
        self.Accuracy=0

    # resets error to ''
    def resetError(self):
        self.error = ''

    # sets the error text
    def setError(self, errorText):
        self.error = errorText
    
    # converts the object to json to enable data transfer to the frontend
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    # calls the maxMin method from the Filter.py file and stores the result in the data series object
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

    # calls the standardDeviation method from the Filter.py file and stores the result in the data series object
    # Performs data verifications before calling it
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
    
    # calls the interpolation method from the Filter.py file and stores the result in the data series object
    # Performs data verifications before calling it
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

    # calls the smoothing method from the Filter.py file and stores the result in the data series object
    def smoothing(self, smoothingType=None, window=None):
        print("Hi, I'm smoothing")
        filterObj = Filter.Filter()    
        smoothInput= [self.currentData]
        if (smoothingType is not None):
            self.smoothingType = smoothingType
        if (window is not None):
            self.window = window
        flag, revisedInputarr, newarr, msg = filterObj.movingAvg(smoothInput,self.window,self.smoothingType)
        if flag == 'error':
            print('Error:')
            print(msg)
            self.error=msg
        else:
            self.currentData = list(newarr[0])
            self.originalData = list(revisedInputarr[0])

    # Calls the randonForest method from the Filter.py file and stores the result in the data series object
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
    
    # Calls the neuralNetwork method from the Filter.py file and stores the result in the data series object
    def neuralNetwork(self,inputSeriesData, testSize,activeFunction,hiddenLayers,solverFunction,iterations,scalingOnOff ):
        print('Hi, Im neuralNetwork')

        NnInput = NN.NN_inputs(changeDataSeriesForm(inputSeriesData), self.currentData, testSize/100, activeFunction.lower(), hiddenLayers, solverFunction.lower(), iterations, scalingOnOff)
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


# Defining the DataObject class
# This class contains all of the data series objects (i.e. the actual data series and all of their attributes).
# The class has a number of functions to import, change and delete its attributes.
class DataObject:
    def __init__(self, dataSeries, fileName):
         self.dataSeriesDict = {} #stores the dataseries in a dictionary
         if fileName == '':
             fileName = 'series_'
         for i in range(len(dataSeries)):
             self.dataSeriesDict[fileName + '_' + str(i+1)] = DataSeries(fileName + '_' + str(i+1), dataSeries[i])
    
    # Method adds a set of data series (1 to 100+ data series) 
    def addSeries(self, dataSeries, fileName):
         if fileName == '':
             fileName = 'series_'
         for i in range(len(dataSeries)):
             seriesNameTemp = fileName + '_'  + str(i+1)
             while seriesNameTemp in self.dataSeriesDict:
                 seriesNameTemp = seriesNameTemp + '_' + str(i+1)
             self.dataSeriesDict[seriesNameTemp] = DataSeries(seriesNameTemp, dataSeries[i])

    # Method checks if a series with that name is in the dictionary and deletes it if it is.
    def deleteSeries(self, seriesName):
        if seriesName in self.dataSeriesDict:
            self.dataSeriesDict.pop(seriesName)

    # Method deletes all data series from the DataObject.
    def clearSeries(self):
         self.dataSeriesDict.clear()

    # Method iterates through the data series objects in it and resets the values in each of them
    # to the original data uploaded and the original attributes at the initialization.
    def resetToOriginalData(self):
        for i in range(len(self.dataSeriesDict)):
            self.dataSeriesDict[i].resetToOriginalData()

    # Method returns the dictionary with all the data series.
    def getDataSeriesDict(self):
         return self.dataSeriesDict
    
    # Method converts to json format to enable communication with the frontend.
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)



# Method converts to an array of selected data series into a format 
# that the Neural Network modeling method requires.
# The format is the following:
# Initial format [[1,2,3],[5,6,7],[9,10,11]]
# Format of final output [[1,5,9],[2,6,10],[3,7,11]].
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




