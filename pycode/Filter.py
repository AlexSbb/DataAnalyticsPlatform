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

"""Filter class is comprising methods for  data filtering and smooting functionality."""
class Filter():
    
    Error= 'error'
    success = 'success'
    Error_msg1 = 'File can not be processed'
    Error_msg2 = 'For fixed moving average provide odd numbers of window '
    Error_msg3 = 'Window is bigger than the input length.'
    Error_msg4 = 'Number of input values less than 3'
    Error_msg5 = 'Provide a proper moving average type' 
    Error_msg6 = 'Provide a Integer value '
    inputNo = 3
    stdDevFactorMax = 6
    stdDevFactorMin = 1

    """This is the initializer.   
       def __init__(self):
        pass

        #self.name = name""" 

    """
    *****************************************************************************************************************************
    method maxMin       : 
        inputArray      : input array provided to fid outlier
        stdDevFactor    : Factor that multiply the Standard Deviation and is used to calculate the MaxValue and MinValue for the limits.

    variables:
 
        stdDevNum        : Calculates the Standard Deviation of the Data
        stdMeanNum       : Calculates the Mean of the Data
            
     return:
        valPercent         : Calculates de amount of data that is identyfied as an Outlier with respect to the total data.  Calculated in [%]
        replaceMatrixIndex : Array with identyfied rows that are detected as Outliers.
        flag               : success or error
        msg                : success or error massage reason
        maxValue           : Calculates the Maximum Value limit 
        minValue           : Calculates the Minimum Value limit 
    *****************************************************************************************************************************"""    

    def maxMin(self,inputArray, maxValue, minValue):
        
        replaceMatrixIndex = []
        val_percent = 0
        flag = Filter.success
        msg = ''
        try:
            #checking valid length of array
            if(len(inputArray) < Filter.inputNo):
                msg = Filter.Error_msg4 #'Number of input values less than 3'
                flag = Filter.Error #'error'
                return flag,val_percent, replaceMatrixIndex,msg
            
            if(maxValue < minValue ):
                flag = Filter.Error
                msg = 'Max value is lower than Min value'
            elif(maxValue == minValue):
                flag = Filter.Error
                msg = 'Max value equal to than Min value'
            else:
                
                for index in range(len(inputArray)):
                    if inputArray[index] > maxValue or inputArray[index] < minValue:
                        replaceMatrixIndex.append(index)
                        val_percent = len(replaceMatrixIndex) * 100 / len(inputArray)   

        except:
            flag = Filter.Error
            msg = Filter.Error_msg1 
                     

        return flag,val_percent, replaceMatrixIndex,msg 
    
    """
    *****************************************************************************************************************************
    method stdDev       : This method measure of the amount of variation or dispersion of a set of values parameters:
        inputArray      : input array provided to fid outlier
        stdDevFactor    : Factor that multiply the Standard Deviation and is used to calculate the MaxValue and MinValue for the limits.

    variables:
 
        stdDevNum        : Calculates the Standard Deviation of the Data
        stdMeanNum       : Calculates the Mean of the Data
            
     return:
        valPercent         : Calculates de amount of data that is identyfied as an Outlier with respect to the total data.  Calculated in [%]
        replaceMatrixIndex : Array with identyfied rows that are detected as Outliers.
        flag               : success or error
        msg                : success or error massage reason
        maxValue           : Calculates the Maximum Value limit 
        minValue           : Calculates the Minimum Value limit 
    *****************************************************************************************************************************"""    
    
    
    def stdDev(self,inputArray, stdDevFactor):
        
         
        replaceMatrixIndex = []#initializing array
        flag = Filter.success
        msg = '' 
        
        #providing try block to handle exceptions
        try:
            #initializing variables
            valPercent = 0
            maxValue   = 0
            minValue   = 0
            
            if type(stdDevFactor) != int :
                msg = Filter.Error_msg6  #'Provide a Integer value '
                flag = Filter.Error #'error' 
                return flag, valPercent, replaceMatrixIndex, maxValue, minValue,msg
            #check the range of standard deviation factor
            if stdDevFactor > Filter.stdDevFactorMax or stdDevFactor < Filter.stdDevFactorMin :

                msg  = 'standard deviation factor should be between ' + str(Filter.stdDevFactorMin) + ' and '+ str(Filter.stdDevFactorMax)
                flag = Filter.Error #'error' 
                return flag, valPercent, replaceMatrixIndex, maxValue, minValue,msg
            
            #checking valid length of array
            if(len(inputArray) < Filter.inputNo):
                msg = Filter.Error_msg4 #'Number of input values less than 3'
                flag = Filter.Error #'error'
                return flag, valPercent, replaceMatrixIndex, maxValue, minValue,msg #returing flag(error),0,[],0,0, message
            
            #calculation with valid length of array
            else:
                stdDevNum = np.std(inputArray, axis=0)
                stdMeanNum = np.mean(inputArray, axis=0)
                maxValue = stdMeanNum+(stdDevNum*stdDevFactor)
                minValue = stdMeanNum-(stdDevNum*stdDevFactor)
                flag,valPercent, replaceMatrixIndex,msg = Filter.maxMin(self, inputArray, maxValue, minValue)

        except:
            flag = Filter.Error
            msg  = Filter.Error_msg1

        return flag, valPercent, replaceMatrixIndex, maxValue, minValue,msg
    
   
     
    """
    *****************************************************************************************************************************    
    method movingAvg    : is the moving average for the data to move forward,backward or fixed by the number of windows 
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
    
    def movingAvg(self,inputArray, window, avgType):
    
        
        flag = Filter.success
        msg  = ''
        
        #providing try block to handle exceptions
        try:
            
            if avgType is None :
                avgType = 'backward'#checking if moving average type is null and setting default value   
                
            #initializing  array
            values=[]
            newarr = [] 
            revisedInputarr1 = []
            revisedInputarr = []
            
            #checking wondow is integer
            if type(window) != int :
                msg = Filter.Error_msg6  #'Provide a Integer value '
                flag = Filter.Error #'error' 
                return flag,revisedInputarr,newarr,msg
            

            weights = np.repeat(1.0, window)/window #array of window size with value 1.0/window 
            inputArrayLen = len(inputArray)#calculating number of input
            

            
            #checking valid length of array
            if(len(inputArray[0]) < Filter.inputNo):
                msg = Filter.Error_msg4 #'Number of input values less than 3'
                flag = Filter.Error #'error'
                return flag,revisedInputarr,newarr,msg 
       
            # checking the window not crossing 1 and length of input data
            if( window == 1 or window > len(inputArray[0]) ):
                flag = Filter.Error #'error'
                if(window == 1):
                    msg = 'window should not be 1'                
                else:
                    msg = Filter.Error_msg3 #'Window is bigger than the input length.'
                return flag,revisedInputarr,newarr,msg 
                
            #if window is in range     
            else:
                for i in range(inputArrayLen):# loop for 1 or more data input
                    values = np.convolve(inputArray[i], weights, 'valid') # calculating moving average 
                    newarr.append(values) # appending smoothed data
                    if avgType == 'forward':
                        for i in range(inputArrayLen):
                            revisedInputarr.append(np.flip(np.delete(np.flip(inputArray[i]),np.s_[0: int(window - 1) :]))) #deleting extra data from backside of input array
                    
                    elif avgType == 'backward':
                        for i in range(inputArrayLen):
                            revisedInputarr.append(np.delete(inputArray[i],np.s_[0: window - 1 :]))#deleting extra data from front of input array
                    
                    elif avgType == 'fixed':
                        if(window % 2 != 0):
                            for i in range(inputArrayLen):
                                revisedInputarr1.append(np.flip(np.delete(np.flip(inputArray[i]),np.s_[0: int((window - 1)/2) :])))#deleting extra data from backside of input array
                            for j in range(inputArrayLen):
                                revisedInputarr.append(np.delete(revisedInputarr1[i],np.s_[0: int((window - 1)/2) :])) #deleting extra data from front of input array
                        else:
                            flag = Filter.Error #'error'
                            msg = Filter.Error_msg2 #'For fixed moving average provide odd numbers of window '
                    else:
                        flag = Filter.Error #'error'
                        msg = Filter.Error_msg5 #'Provide a proper moving average type'
                        
        #handling exceptions in except block
        except:
            flag = Filter.Error #'error'
            msg = Filter.Error_msg1 #unexpected error 'File can not be processed'
        return flag,revisedInputarr,newarr,msg #returing flag(success or error),reviced input array,smoothed array, messsage
    
    def countConsec(self,val, OutlierMatrix):
        
        count = 0
        index_prev = OutlierMatrix[val]
        index_next =0
                   
            
        for index in range(val,len(OutlierMatrix)-1):

            if OutlierMatrix[index+1] == OutlierMatrix[index]+1:
                count+=1
                index_next = OutlierMatrix[index+1]
            else:
                if(count!=0):
                    break
        index_prev = OutlierMatrix[(index+1) - count]
        return index_prev,index_next,index
        
    
    
    def count(self,OutlierMatrix):
        count = 0
        count1 = 0
        for index in range(len(OutlierMatrix)-1):
            if OutlierMatrix[index+1] == OutlierMatrix[index]+1:
                count = count +1
            else:
                if count != 0:
                    count1 = count1 + 1
                    count = 0
            if count != 0:
                count1 = count1+1
        return count1 
    

    
    
    def interpolation(self,OriginalMatrix,OutlierMatrix, Kind,maxVal,minVal):
        flag = ''
        msg = ''
        try:
            InterpolatedMatrix = []
            InterpolatedMatrix = OriginalMatrix
            oldMatrix = OriginalMatrix.copy()

            if Kind == 0:
                
                InterpolatedMatrixIndex = np.zeros([len(OutlierMatrix), 3])
                for index in range(len(OutlierMatrix)):
                    if(OutlierMatrix[index] == 0) :
                        if(abs(OriginalMatrix[OutlierMatrix[index]] - maxVal) > abs(OriginalMatrix[OutlierMatrix[index]] - minVal) ):
                            InterpolatedMatrixIndex [index][0] = minVal
                        else:
                            InterpolatedMatrixIndex [index][0] = maxVal
                    else:
                        InterpolatedMatrixIndex [index][0] = OriginalMatrix[OutlierMatrix[index]-1]
                    InterpolatedMatrixIndex [index][1] = OriginalMatrix[OutlierMatrix[index]]
                    if(OutlierMatrix[index]+1 >= len(OriginalMatrix)):
                        if(abs(OriginalMatrix[OutlierMatrix[index]] - maxVal) > abs(OriginalMatrix[OutlierMatrix[index]] - minVal) ):
                            InterpolatedMatrixIndex [index][2] = minVal
                        else:
                            InterpolatedMatrixIndex [index][2] = maxVal
                    else:
                        InterpolatedMatrixIndex [index][2] = OriginalMatrix[OutlierMatrix[index]+1]
                    f = interpolate.interp1d([OutlierMatrix[index]-1, OutlierMatrix[index]+1], [InterpolatedMatrixIndex [index][0], InterpolatedMatrixIndex[index][2]],  kind = 'linear')
                    InterpolatedMatrix [OutlierMatrix[index]] = f(OutlierMatrix[index])
                    
                InterpolatedMatrix2 = OriginalMatrix
                counter = Filter.count(self,OutlierMatrix)
                val = 0
                
                while counter != 0:
                    counter = counter - 1
                    index_prev,index_end,val = Filter.countConsec(self,val,OutlierMatrix)
                    val = val+1
                    for index in range(0,index_end - index_prev):
                        InterpolatedMatrixIndex2 = np.zeros([index_end - index_prev , 3])
                        val2 = index_prev + index
                        if(index_prev == 0) :
                            if(abs(OriginalMatrix[index_prev] - maxVal) > abs(OriginalMatrix[index_prev] - minVal) ):
                                InterpolatedMatrixIndex2 [index][0] = minVal
                            else:
                                InterpolatedMatrixIndex2 [index][0] = maxVal
                        else:
                            InterpolatedMatrixIndex2 [index][0] = OriginalMatrix[index_prev-1]
                        InterpolatedMatrixIndex2 [index][1] = OriginalMatrix[val2]
                        if(index_end+1 >=len(OriginalMatrix)):
                            if(abs(OriginalMatrix[index_end] - maxVal) > abs(OriginalMatrix[index_end] - minVal) ):
                                InterpolatedMatrixIndex2 [index][2] = minVal
                            else:
                                InterpolatedMatrixIndex2 [index][2] = maxVal
                        else:
                            InterpolatedMatrixIndex2 [index][2] = OriginalMatrix[index_end+1]
                        f = interpolate.interp1d([index_prev-1, index_end+1], [InterpolatedMatrixIndex2 [index][0], InterpolatedMatrixIndex2[index][2]],  kind = 'linear')
                        InterpolatedMatrix2 [val2] = f(val2)
            elif Kind == 1:
                InterpolatedMatrixIndex = np.zeros([len(OutlierMatrix), 5])
                for index in range(len(OutlierMatrix)):
                    if(OutlierMatrix[index] == 0):
                        if(abs(OriginalMatrix[index_end] - maxVal) > abs(OriginalMatrix[index_end] - minVal)):
                            InterpolatedMatrixIndex[index][0] = minVal
                            InterpolatedMatrixIndex[index][1] = minVal
                        else:
                            InterpolatedMatrixIndex[index][0] = maxVal
                            InterpolatedMatrixIndex[index][1] = maxVal 
                    else:
                        InterpolatedMatrixIndex[index][0] = OriginalMatrix[OutlierMatrix[index] - 2]
                        InterpolatedMatrixIndex[index][1] = OriginalMatrix[OutlierMatrix[index] - 1]
                    InterpolatedMatrixIndex[index][2] = OriginalMatrix[OutlierMatrix[index]]
                    if(OutlierMatrix[index]+1 >= len(OriginalMatrix)):
                        if(abs(OutlierMatrix[index] - maxVal) > abs(OutlierMatrix[index] - minVal) ):
                            InterpolatedMatrixIndex [index][3] = minVal
                            InterpolatedMatrixIndex [index][4] = minVal
                        else:
                            InterpolatedMatrixIndex [index][3] = maxVal
                            InterpolatedMatrixIndex [index][4] = maxVal
                    else:
                        InterpolatedMatrixIndex [index][3] = OriginalMatrix[OutlierMatrix[index]+1]
                        InterpolatedMatrixIndex [index][4] = OriginalMatrix[OutlierMatrix[index]+2]
                    f = interpolate.interp1d([OutlierMatrix[index]-2, OutlierMatrix[index]-1, OutlierMatrix[index]+1, OutlierMatrix[index]+2], [InterpolatedMatrixIndex [index][0], InterpolatedMatrixIndex [index][1], InterpolatedMatrixIndex[index][3], InterpolatedMatrixIndex [index][4]],  kind = 'quadratic')
                    InterpolatedMatrix [OutlierMatrix[index]] = f(OutlierMatrix[index])
                    
                InterpolatedMatrix2 = OriginalMatrix
                counter = Filter.count(self,OutlierMatrix)
                val = 0

                while counter != 0:
                    counter = counter - 1
                    index_prev,index_end,val = Filter.countConsec(self,val,OutlierMatrix)
                    val = val+1
                    for index in range(0,index_end - index_prev ):
                        InterpolatedMatrixIndex2 = np.zeros([index_end - index_prev , 3])
                        val2 = index_prev + index
                        if(index_prev == 0) :
                            if(abs(OriginalMatrix[index_prev] - maxVal) > abs(OriginalMatrix[index_prev] - minVal) ):
                                InterpolatedMatrixIndex2 [index][0] = minVal
                            else:
                                InterpolatedMatrixIndex2 [index][0] = maxVal
                        else:
                            InterpolatedMatrixIndex2 [index][0] = OriginalMatrix[index_prev-1]
                        InterpolatedMatrixIndex2 [index][1] = OriginalMatrix[val2]
                        if(index_end+1 >=len(OriginalMatrix)):
                            if(abs(OriginalMatrix[index_end] - maxVal) > abs(OriginalMatrix[index_end] - minVal) ):
                                InterpolatedMatrixIndex2 [index][2] = minVal
                            else:
                                InterpolatedMatrixIndex2 [index][2] = maxVal
                        else:
                            InterpolatedMatrixIndex2 [index][2] = OriginalMatrix[index_end+1]
                        f = interpolate.interp1d([index_prev-1, index_end+1], [InterpolatedMatrixIndex2 [index][0], InterpolatedMatrixIndex2[index][2]],  kind = 'linear')
                        InterpolatedMatrix2 [val2] = f(val2)

        except:
            flag = Filter.Error
            msg = Filter.Error_msg1 

        return flag,OriginalMatrix,msg
        
        
        
    def smoothing_plot (self,filename, window,avg_type):
        old_array = Filter.makearray(self,filename)
        print(old_array)
        #flag,old_array1,new_array =  Filter.moving_avg(self,old_array,window,avg_type)
        flag,old_array1,new_array,msg =  Filter.moving_avg(self,old_array,window, avg_type)
        print(old_array1)
        print(new_array)
        for i in range(len(old_array1)):
            plt.plot(old_array1[i])
            plt.plot(new_array[i],color = 'red')
       
        plt.show()
        
        
        
    def minmax_plot (self,filename, minmaxmatrix):
        old_array = Filter.makearray(self,filename)
        
        #flag,old_array1,new_array =  Filter.moving_avg(self,old_array,window,avg_type)
        flag,old_array1,outlier =  Filter.maxMin(self,old_array.tolist(), minmaxmatrix)
        print(old_array1)
        print(outlier)
          
    
    def makearray (self,file_name2):
        with open(file_name2 ,'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            x = list(plots)
            result = np.array(x).astype("float")
            result2 = result.T
       
        return result2
    
    



