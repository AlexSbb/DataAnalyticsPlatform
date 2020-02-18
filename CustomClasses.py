from flask import jsonify
import numpy as np
import pandas as pd
import temp_test.read_csv_data as rcd
import json
import pycode.Team2Functions as T2F

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
        self.realMin = min(data)
        self.realMax = max(data)
        self.size = len(data)
        self.median = np.median(data)

        self.window = 2
        self.smoothingType = backward

        self.selectedMin = 0.0
        self.selectedMax = 1.0
        self.maxMinMatrix = []
        self.stdDevMaxMinMatrix = []
        self.stdDevFactor =  1.0
        self.interpolationType = linear #true for linear and false for quadratic interpolation
        self.interpolationArray = []
        self.replaceArray = []
        self.beforeSmoothingArray = []
        self.afterSmoothingArray = []

        self.error = ''

    def resetError():
        self.error = ''

    def setError(errorText):
        self.error = errorText


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
             
