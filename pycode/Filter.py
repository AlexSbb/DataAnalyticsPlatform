# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:13:13 2020

@author: Amrita Sen 
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import statistics as st
import scipy
from scipy.interpolate import griddata
from scipy import interpolate
from scipy.interpolate import interp1d

np.nan


"""
    *****************************************************************************************************************************
    Filter class is comprising methods for  data filtering and smooting functionality
    
    constants:: used in methods as a fix value
    
    Flags used in methods to identify whether the method is successfull or failure.   
    Error       : 'error'
    success     : 'success'
    
    Error messages used in different methods.
    Error_msg1  : 'File can not be processed'
    Error_msg2  : 'For fixed moving average provide odd numbers of window '
    Error_msg3  : 'Window is bigger than the input length.'
    Error_msg4  : 'Number of input values less than 3'
    Error_msg5  : 'Provide a proper moving average type'
    Error_msg6  : 'Provide a Integer value '
    Error_msg7  : 'There is no outlier values to interpolate'
    
    inputNo         : lower limit for number of data in input array i.e 3
    stdDevFactorMax : standard deviation factor upper limit i.e 6
    stdDevFactorMin : standard deviation factor lower limit i.e 1
        
    methods::
    maxMin(inputArray, maxValue, minValue) : Finding outlier indexes of input array or input data based on max and min limit provided by user
    stdDev(inputArray, stdDevFactor)       : This method measure of the amount of variation or dispersion in input array or input data 
                                                   depending on standard deviation factor.
    movingAvg(inputArray, window, avgType) : This calculate the moving average for the data to move forward,backward or fixed by the number of windows
                                                   
    *****************************************************************************************************************************"""


class Filter():
    
    
    def __init__(self):
        pass
        
        
    Error           = 'error'
    success         = 'success'
    Error_msg1      = 'File can not be processed'
    Error_msg2      = 'For fixed moving average provide odd numbers of window '
    Error_msg3      = 'Window is bigger than the input length.'
    Error_msg4      = 'Number of input values less than 3'
    Error_msg5      = 'Provide a proper moving average type'
    Error_msg6      = 'Provide a Integer value '
    Error_msg7      = 'There is no outlier values to interpolate'
    inputNo         = 3
    stdDevFactorMax = 6
    stdDevFactorMin = 1

    """
    ******************************************************************************************************************************************
    method maxMin          : Finding outlier indexes based on max and min limit provided by user
        inputArray         : input array provided to find outlier
        maxValue           : Max limit provided by user
        minValue           : Min limit provided by user

    variables:
 
        arrayMaxval        : Max value in input array
        arrayMinval        : Min value in input array
            
     return:
        valPercent         : Calculates de amount of data that is identyfied as an Outlier with respect to the total data.  Calculated in [%]
        replaceMatrixIndex : Array with identyfied rows that are detected as Outliers.
        flag               : success or error
        msg                : success or error massage reason
        maxValue           : Calculates the Maximum Value limit 
        minValue           : Calculates the Minimum Value limit 
    *******************************************************************************************************************************************"""

    def maxMin(self, inputArray, maxValue, minValue):

        #initializing
        replaceMatrixIndex = []
        valPercent = 0
        
        flag = Filter.success
        msg = ''
        
        # providing try block to handle exceptions
        try:
            # checking valid length of array
            if (len(inputArray) < Filter.inputNo):
                msg = Filter.Error_msg4  # 'Number of input values less than 3'
                flag = Filter.Error  # 'error'
                return flag, valPercent, replaceMatrixIndex, msg
            
            # checking if max value provided is less than min value 
            if (maxValue < minValue):
                flag = Filter.Error
                msg = 'Max value is lower than Min value'
                
            # checking if max value provided is equal to min value
            elif (maxValue == minValue):
                flag = Filter.Error
                msg = 'Max value equal to than Min value'
            else:
                arrayMaxval = max(inputArray) #getting max input data
                arrayMinval = min(inputArray) #getting min input data
                
                #checking if there is any outlier values
                if(maxValue >= arrayMaxval  and minValue <= arrayMinval ):
                    flag = Filter.Error      #error
                    msg  = Filter.Error_msg7 # 'There is no outlier values to interpolate'
                    return flag, valPercent, replaceMatrixIndex,msg

                #fininding outlier index of original array
                for index in range(len(inputArray)):
                    if inputArray[index] > maxValue or inputArray[index] < minValue:
                        replaceMatrixIndex.append(index)
                        valPercent = len(replaceMatrixIndex) * 100 / len(inputArray) #percentage of outlier
                        
        # handling exceptions in except block                        
        except:
            flag = Filter.Error #error
            msg  = Filter.Error_msg1  # unexpected error 'File can not be processed'

        return flag, valPercent, replaceMatrixIndex, msg # returing flag(sucess or error),outlier percentage,outlier index, message

    """
    *****************************************************************************************************************************
    method stdDev          : This method provide measure of the amount of variation or dispersion in input data using standard deviation factor.
        inputArray         : input array provided to find outlier
        stdDevFactor       : Factor that multiply the Standard Deviation and is used to calculate the MaxValue and MinValue for the limits.
                             currenty using standard deviation factor only for values 1 to 6

    variables:
        stdDevNum          : Calculates the Standard Deviation of the Data
        stdMeanNum         : Calculates the Mean of the Data
            
     return:
        flag               : success or error         
        valPercent         : Calculates the amount of data that is identyfied as an Outlier with respect to the total data.  Calculated in [%]
        replaceMatrixIndex : Array with identyfied rows that are detected as Outliers.
        maxValue           : Calculates the Maximum Value limit 
        minValue           : Calculates the Minimum Value limit
        msg                : success or error massage reason        
    *****************************************************************************************************************************"""

    def stdDev(self, inputArray, stdDevFactor):

        replaceMatrixIndex = []  # initializing array
        flag = Filter.success
        msg = ''

        # providing try block to handle exceptions
        try:
            # initializing variables
            valPercent = 0
            maxValue = 0
            minValue = 0

            if type(stdDevFactor) != int:
                msg = Filter.Error_msg6  # 'Provide a Integer value '
                flag = Filter.Error  # 'error'
                return flag, valPercent, replaceMatrixIndex, maxValue, minValue, msg
            # check the range of standard deviation factor
            if stdDevFactor > Filter.stdDevFactorMax or stdDevFactor < Filter.stdDevFactorMin:
                msg = 'standard deviation factor should be between ' + str(Filter.stdDevFactorMin) + ' and ' + str(
                    Filter.stdDevFactorMax)
                flag = Filter.Error  # 'error'
                return flag, valPercent, replaceMatrixIndex, maxValue, minValue, msg  # returing flag(error),0,[],0,0, message

            # checking valid length of array
            if (len(inputArray) < Filter.inputNo):
                msg = Filter.Error_msg4  # 'Number of input values less than 3'
                flag = Filter.Error  # 'error'
                return flag, valPercent, replaceMatrixIndex, maxValue, minValue, msg  # returing flag(error),0,[],0,0, message

            # calculation with valid length of array
            else:
                
                stdDevNum = np.std(inputArray, axis=0) #calculated standard deviation
                stdMeanNum = np.mean(inputArray, axis=0) #calculated min
                maxValue = stdMeanNum + (stdDevNum * stdDevFactor) # calculated max limit
                minValue = stdMeanNum - (stdDevNum * stdDevFactor) #calculated min limit
                flag, valPercent, replaceMatrixIndex, msg = Filter.maxMin(self, inputArray, maxValue, minValue)
                
        # handling exceptions in except block
        except:
            flag = Filter.Error # 'error'
            msg  = Filter.Error_msg1  # unexpected error 'File can not be processed'

        return flag, valPercent, replaceMatrixIndex, maxValue, minValue, msg  # returing flag(success or error),outlier percentage,outlier index,max limit,min limit, message

    """
    *****************************************************************************************************************************    
    method movingAvg    : This calculate the moving average for the data to move forward,backward or fixed by the number of windows 
                          determined by the trader or the user
    parameters:
        inputArray      : input array provided to smooth data
        window          : window to calculate moving average
        avgType         : type of moving average.default avgType = bakward 
                          the values can be either of these three values according to user.
                          1.forward
                          2.bakward
                          3.fixed
    variables:
        values           : array to capture intermediate values after convolution
        weights          : array calulated with numpy Repeat method anf geting output of size window and  value 1.0/window
                          
        revisedInputarr1 : intermediate array to calcuate final array
        inputArrayLen    : number of input
        i,j              : used for looping
            
     return:
        newarr           : array containing smoothed data
        revisedInputarr  : revised input data according to type of moving average and window
        flag             : success or error
        msg              : success or error massage reason
    *****************************************************************************************************************************"""

    def movingAvg(self, inputArray, window, avgType):

        flag = Filter.success
        msg = ''

        # providing try block to handle exceptions
        try:

            if avgType is None:
                avgType = 'backward'  # checking if moving average type is null and setting default value

            # initializing  array
            values = []
            newarr = []
            revisedInputarr1 = []
            revisedInputarr = []

            # checking wondow is integer
            if type(window) != int:
                msg = Filter.Error_msg6  # 'Provide a Integer value '
                flag = Filter.Error  # 'error'
                return flag, revisedInputarr, newarr, msg

            weights = np.repeat(1.0, window) / window  # array of window size with value 1.0/window
            inputArrayLen = len(inputArray)  # calculating number of input

            # checking valid length of array
            if (len(inputArray[0]) < Filter.inputNo):
                msg = Filter.Error_msg4  # 'Number of input values less than 3'
                flag = Filter.Error  # 'error'
                return flag, revisedInputarr, newarr, msg

                # checking the window not crossing 1 and length of input data
            if (window == 1 or window > len(inputArray[0])):
                flag = Filter.Error  # 'error'
                if (window == 1):
                    msg = 'window should not be 1'
                else:
                    msg = Filter.Error_msg3  # 'Window is bigger than the input length.'
                return flag, revisedInputarr, newarr, msg

                # if window is in range
            else:
                for i in range(inputArrayLen):  # loop for 1 or more data input
                    values = np.convolve(inputArray[i], weights, 'valid')  # calculating moving average
                    newarr.append(values)  # appending smoothed data
                    if avgType == 'forward':
                        for i in range(inputArrayLen):
                            revisedInputarr.append(np.flip(np.delete(np.flip(inputArray[i]), np.s_[0: int(
                                window - 1):])))  # deleting extra data from backside of input array

                    elif avgType == 'backward':
                        for i in range(inputArrayLen):
                            revisedInputarr.append(np.delete(inputArray[i], np.s_[
                                                                            0: window - 1:]))  # deleting extra data from front of input array

                    elif avgType == 'fixed':
                        if (window % 2 != 0):
                            for i in range(inputArrayLen):
                                revisedInputarr1.append(np.flip(np.delete(np.flip(inputArray[i]), np.s_[0: int(
                                    (window - 1) / 2):])))  # deleting extra data from backside of input array
                            for j in range(inputArrayLen):
                                revisedInputarr.append(np.delete(revisedInputarr1[i], np.s_[0: int(
                                    (window - 1) / 2):]))  # deleting extra data from front of input array
                        else:
                            flag = Filter.Error  # 'error'
                            msg = Filter.Error_msg2  # 'For fixed moving average provide odd numbers of window '
                    else:
                        flag = Filter.Error  # 'error'
                        msg = Filter.Error_msg5  # 'Provide a proper moving average type'

        # handling exceptions in except block
        except:
            flag = Filter.Error  # 'error'
            msg = Filter.Error_msg1  # unexpected error 'File can not be processed'
        return flag, revisedInputarr, newarr, msg  # returing flag(success or error),reviced input array,smoothed array, messsage

    """
    *****************************************************************************************************************************    
    method countConsec  : This methods calculates the 1st consecutive dataset in a given array staring from a given index
    parameters:
        val             : starting index for the search of consecutive dataset
        outlierMatrix   : Array containg all outlier data index of original data set 

    variables:
        count           : used for intermediate counting 
        index           : used to loop through index of input outlierMatrix
                          
     return:
        indexBegin      : begining of consecutive data
        indexEnd        : end of consecutive data
        index           : outlierMatrix array index where the current dataset seaching stoppep 
    *****************************************************************************************************************************"""

    def countConsec(self, val, outlierMatrix):
        
        #initializing
        count = 0
        indexEnd = 0
        indexBegin = outlierMatrix[val]

        #looping through all data in outlierMatrix to find consecutive data set
        for index in range(val, len(outlierMatrix) - 1):
            #searching if there is any data set equals to its next data set
            if outlierMatrix[index + 1] == outlierMatrix[index] + 1:
                count += 1 # counting a value how many times the loop is executing for a specific consecutive sequence
                if count == 1:
                    indexBegin = outlierMatrix[index] # assigning the begining index of consecutive sequence
                indexEnd = outlierMatrix[index + 1] # assighing the last index of consecuitive sequence
                
            else:
                if (count != 0):
                    break #breacking out the loop if we have already found a consecutive sequence

        return indexBegin, indexEnd, index #returning begining ,ending of consecuive sequence,stopping index where the search stopped
    """
    *****************************************************************************************************************************    
    method count         : This methods calculates number of consecutive data sets
    parameters:
        outlierMatrix   : Array containg all outlier data index of original data set 

    variables:
        count           : used for intermediate counting 
        index           : used to loop through index of input outlierMatrix
                          
     return:
        count1         : nuber of consecuitive data set
    *****************************************************************************************************************************"""

    def count(self, OutlierMatrix):
        count = 0
        count1 = 0
        for index in range(len(OutlierMatrix) - 1):
            if OutlierMatrix[index + 1] == OutlierMatrix[index] + 1:
                count += 1
            else:
                if count != 0:
                    count1 = count1 + 1
                    count = 0

        if count != 0:
            count1 += 1

        return count1

    def interpolation(self, OriginalMatrix, OutlierMatrix, Kind, maxVal, minVal):
        flag = Filter.success
        msg = ''
        try:
            InterpolatedMatrix = OriginalMatrix.copy()
            if Kind == 0:
                InterpolatedMatrixIndex = np.zeros([len(OutlierMatrix), 3])
                for index in range(len(OutlierMatrix)):
                    if OutlierMatrix[index] == 0:
                        if (abs(OriginalMatrix[OutlierMatrix[index]] - maxVal) >
                                abs(OriginalMatrix[OutlierMatrix[index]] - minVal)):
                            InterpolatedMatrixIndex[index][0] = minVal
                        else:
                            InterpolatedMatrixIndex[index][0] = maxVal
                    else:
                        InterpolatedMatrixIndex[index][0] = OriginalMatrix[OutlierMatrix[index] - 1]

                    InterpolatedMatrixIndex[index][1] = OriginalMatrix[OutlierMatrix[index]]

                    if (OutlierMatrix[index] + 1) >= len(OriginalMatrix):
                        if abs(OriginalMatrix[OutlierMatrix[index]] - maxVal) > \
                                abs(OriginalMatrix[OutlierMatrix[index]] - minVal):
                            InterpolatedMatrixIndex[index][2] = minVal
                        else:
                            InterpolatedMatrixIndex[index][2] = maxVal
                    else:
                        InterpolatedMatrixIndex[index][2] = OriginalMatrix[OutlierMatrix[index] + 1]

                    f = interpolate.interp1d([OutlierMatrix[index] - 1, OutlierMatrix[index] + 1],
                                             [InterpolatedMatrixIndex[index][0], InterpolatedMatrixIndex[index][2]],
                                             kind='linear')
                    InterpolatedMatrix[OutlierMatrix[index]] = round(float(f(OutlierMatrix[index])), 4)

                counter = Filter.count(self, OutlierMatrix)
                val = 0

                while counter != 0:
                    counter = counter - 1
                    index_prev, index_end, val = Filter.countConsec(self, val, OutlierMatrix)
                    val += 1
                    for index in range(index_end - index_prev + 1):
                        InterpolatedMatrixIndex2 = np.zeros([index_end - index_prev + 1, 3])
                        val2 = index_prev + index
                        if index_prev == 0:
                            if abs(OriginalMatrix[index_prev] - maxVal) > abs(OriginalMatrix[index_prev] - minVal):
                                InterpolatedMatrixIndex2[index][0] = minVal
                            else:
                                InterpolatedMatrixIndex2[index][0] = maxVal
                        else:
                            InterpolatedMatrixIndex2[index][0] = OriginalMatrix[index_prev - 1]

                        InterpolatedMatrixIndex2[index][1] = OriginalMatrix[val2]

                        if (index_end + 1) >= len(OriginalMatrix):
                            if abs(OriginalMatrix[index_end] - maxVal) > abs(OriginalMatrix[index_end] - minVal):
                                InterpolatedMatrixIndex2[index][2] = minVal
                            else:
                                InterpolatedMatrixIndex2[index][2] = maxVal
                        else:
                            InterpolatedMatrixIndex2[index][2] = OriginalMatrix[index_end + 1]

                        f = interpolate.interp1d([index_prev - 1, index_end + 1],
                                                 [InterpolatedMatrixIndex2[index][0],
                                                  InterpolatedMatrixIndex2[index][2]],
                                                 kind='linear')
                        InterpolatedMatrix[val2] = round(float(f(val2)), 4)


            elif Kind == 1:
                InterpolatedMatrixIndex = np.zeros([len(OutlierMatrix), 5])
                for index in range(len(OutlierMatrix)):
                    if OutlierMatrix[index] == 0:
                        if abs(OriginalMatrix[OutlierMatrix[index]] - maxVal) > \
                                abs(OriginalMatrix[OutlierMatrix[index]] - minVal):
                            InterpolatedMatrixIndex[index][0] = minVal
                            InterpolatedMatrixIndex[index][1] = minVal
                        else:
                            InterpolatedMatrixIndex[index][0] = maxVal
                            InterpolatedMatrixIndex[index][1] = maxVal
                    else:
                        InterpolatedMatrixIndex[index][0] = OriginalMatrix[OutlierMatrix[index] - 2]
                        InterpolatedMatrixIndex[index][1] = OriginalMatrix[OutlierMatrix[index] - 1]

                    InterpolatedMatrixIndex[index][2] = OriginalMatrix[OutlierMatrix[index]]

                    if (OutlierMatrix[index] + 1) >= len(OriginalMatrix):
                        if abs(OriginalMatrix[OutlierMatrix[index]] - maxVal) > \
                                abs(OriginalMatrix[OutlierMatrix[index]] - minVal):
                            InterpolatedMatrixIndex[index][3] = minVal
                            InterpolatedMatrixIndex[index][4] = minVal
                        else:
                            InterpolatedMatrixIndex[index][3] = maxVal
                            InterpolatedMatrixIndex[index][4] = maxVal
                    elif (OutlierMatrix[index] + 2) >= len(OriginalMatrix):
                        if abs(OriginalMatrix[OutlierMatrix[index]] - maxVal) > \
                                abs(OriginalMatrix[OutlierMatrix[index]] - minVal):
                            InterpolatedMatrixIndex[index][3] = OriginalMatrix[index + 1]
                            InterpolatedMatrixIndex[index][4] = minVal
                        else:
                            InterpolatedMatrixIndex[index][3] = OriginalMatrix[index + 1]
                            InterpolatedMatrixIndex[index][4] = maxVal
                    else:
                        InterpolatedMatrixIndex[index][3] = OriginalMatrix[OutlierMatrix[index] + 1]
                        InterpolatedMatrixIndex[index][4] = OriginalMatrix[OutlierMatrix[index] + 2]

                    f = interpolate.interp1d([OutlierMatrix[index] - 2, OutlierMatrix[index] - 1,
                                              OutlierMatrix[index] + 1, OutlierMatrix[index] + 2],
                                             [InterpolatedMatrixIndex[index][0], InterpolatedMatrixIndex[index][1],
                                              InterpolatedMatrixIndex[index][3], InterpolatedMatrixIndex[index][4]],
                                             kind='quadratic')
                    InterpolatedMatrix[OutlierMatrix[index]] = round(float(f(OutlierMatrix[index])), 4)

                counter = Filter.count(self, OutlierMatrix)
                val = 0

                while counter != 0:
                    counter = counter - 1
                    index_prev, index_end, val = Filter.countConsec(self, val, OutlierMatrix)
                    val += 1
                    for index in range(0, index_end - index_prev + 1):
                        InterpolatedMatrixIndex2 = np.zeros([index_end - index_prev + 1, 5])
                        val2 = index_prev + index
                        if index_prev == 0:
                            if abs(OriginalMatrix[index_prev] - maxVal) > abs(OriginalMatrix[index_prev] - minVal):
                                InterpolatedMatrixIndex2[index][0] = minVal
                                InterpolatedMatrixIndex2[index][1] = minVal
                            else:
                                InterpolatedMatrixIndex2[index][0] = maxVal
                                InterpolatedMatrixIndex2[index][1] = maxVal
                        else:
                            InterpolatedMatrixIndex2[index][0] = OriginalMatrix[index_prev - 2]
                            InterpolatedMatrixIndex2[index][1] = OriginalMatrix[index_prev - 1]

                        InterpolatedMatrixIndex2[index][2] = OriginalMatrix[val2]

                        if (index_end + 1) >= len(OriginalMatrix):
                            if abs(OriginalMatrix[index_end] - maxVal) > abs(OriginalMatrix[index_end] - minVal):
                                InterpolatedMatrixIndex2[index][3] = minVal
                                InterpolatedMatrixIndex2[index][4] = minVal
                            else:
                                InterpolatedMatrixIndex2[index][3] = maxVal
                                InterpolatedMatrixIndex2[index][4] = maxVal
                        elif (index_end + 2) >= len(OriginalMatrix):
                            if abs(OriginalMatrix[index_end] - maxVal) > abs(OriginalMatrix[index_end] - minVal):
                                InterpolatedMatrixIndex2[index][3] = OriginalMatrix[index_end + 1]
                                InterpolatedMatrixIndex2[index][4] = minVal
                            else:
                                InterpolatedMatrixIndex2[index][3] = OriginalMatrix[index_end + 1]
                                InterpolatedMatrixIndex2[index][4] = maxVal

                        else:
                            InterpolatedMatrixIndex2[index][3] = OriginalMatrix[index_end + 1]
                            InterpolatedMatrixIndex2[index][4] = OriginalMatrix[index_end + 2]

                        f = interpolate.interp1d([index_prev - 2, index_prev - 1, index_end + 1, index_end + 2],
                                                 [InterpolatedMatrixIndex2[index][0],
                                                  InterpolatedMatrixIndex2[index][1],
                                                  InterpolatedMatrixIndex2[index][3],
                                                  InterpolatedMatrixIndex2[index][4]],
                                                 kind='quadratic')
                        InterpolatedMatrix[val2] = round(float(val2), 4)

        except:
            flag = Filter.Error
            msg = Filter.Error_msg1

        return flag, InterpolatedMatrix, msg