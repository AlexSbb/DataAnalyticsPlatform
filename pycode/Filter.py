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
    Error_msg2 = 'For fixed moving average provide odd no window '

    """This is the initializer.   
    def __init__(self):
        pass

        #self.name = name""" 
    
     
    """method moving_avg_forward: is the moving average for the data which moved forward by the number
    of periods determined by the trader
    parameters:
        input_array : input array provided to smooth
        window : window to calculate moving average
    variables:
        values : array to capture intermediate values after convolution
        weights : array calulated with numpy Repeat method anf geting output of size window and
                  value 1.0/window
        input_array_len : length of input_array
            
    return:
        newarr : array to capture intermediate values after convolution
    
    """
    

    
    def maxMin(self,OriginalMatrix, MaxValue, MinValue):
        
        ReplaceMatrixIndex = []
        val_percent = 0
        flag = Filter.success
        msg = ''
        try:
            if(MaxValue < MinValue ):
                flag = Filter.Error
                msg = 'Max value is lower than Min value'
            elif(MaxValue == MinValue):
                flag = Filter.Error
                msg = 'Max value equal to than Min value'
            else:
                
                for index in range(len(OriginalMatrix)):
                    if OriginalMatrix[index] > MaxValue or OriginalMatrix[index] < MinValue:
                        ReplaceMatrixIndex.append(index)
                        val_percent = len(ReplaceMatrixIndex) * 100 / len(OriginalMatrix)   

        except:
            flag = Filter.Error
            msg = Filter.Error_msg1 
                     

        return flag,val_percent, ReplaceMatrixIndex,msg 
    


    
    
    
    def stdDev(self,OriginalMatrix, StdDevFactor):
        ReplaceMatrixIndex = []
        flag = Filter.success
        msg = ''        
        try:
            StdDevNum = np.std(OriginalMatrix, axis=0)
            StdMeanNum = np.mean(OriginalMatrix, axis=0)
            MaxValue = StdMeanNum+(StdDevNum*StdDevFactor)
            MinValue = StdMeanNum-(StdDevNum*StdDevFactor)
            flag,val_percent, ReplaceMatrixIndex,msg = Filter.maxMin(self, OriginalMatrix, MaxValue, MinValue)
        except:
            flag = Filter.Error
            msg = Filter.Error_msg1

        return flag, val_percent, ReplaceMatrixIndex, MaxValue, MinValue,msg
    

    
    
    def movingAvg(self,input_array, window, avg_type):
        flag = ''
        msg = ''
        try:
            values=[]
            newarr = []
            revised_inputarr1 = []
            revised_inputarr = []
            flag = Filter.success
            weights = np.repeat(1.0, window)/window 
            input_array_len = len(input_array)
            if( window == 1):
                msg = 'Provide a proper window'
                flag = Filter.Error
            else:
                for i in range(input_array_len):
                    values = np.convolve(input_array[i], weights, 'valid')
                    newarr.append(values)
                    if avg_type == 'forward':
                        for i in range(input_array_len):
                            revised_inputarr.append(np.flip(np.delete(np.flip(input_array[i]),np.s_[0: int(window - 1) :])))
                    elif avg_type == 'backward':
                        for i in range(input_array_len):
                            revised_inputarr.append(np.delete(input_array[i],np.s_[0: window - 1 :]))
                    elif avg_type == 'fixed':
                        if(window % 2 != 0):
                            for i in range(input_array_len):
                                revised_inputarr1.append(np.flip(np.delete(np.flip(input_array[i]),np.s_[0: int((window - 1)/2) :])))
                            for j in range(input_array_len):
                                revised_inputarr.append(np.delete(revised_inputarr1[i],np.s_[0: int((window - 1)/2) :]))
                        else:
                            msg = Filter.Error_msg2
                            flag = Filter.Error
                    else:
                        flag = Filter.Error
        except:
            flag = Filter.Error
            msg = Filter.Error_msg2
            
    
        return flag,revised_inputarr,newarr,msg
    
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
        index_prev = OutlierMatrix[index - count]
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
    
    



