# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:13:13 2020

@author: Amrita Sen
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv


"""Filter class is comprising methods for  data filtering and smooting functionality."""
class Filter():
    
    Error= 'error'
    success = 'success'

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
    def moving_avg(self,input_array, window, avg_type):
        
        try:
            values=[]
            newarr = []
            revised_inputarr1 = []
            revised_inputarr = []
            flag = Filter.success
            weights = np.repeat(1.0, window)/window 
            input_array_len = len(input_array)
            msg = ''
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
                for i in range(input_array_len):
                    revised_inputarr1.append(np.flip(np.delete(np.flip(input_array[i]),np.s_[0: int((window - 1)/2) :])))
                for j in range(input_array_len):
                    revised_inputarr.append(np.delete(revised_inputarr1[i],np.s_[0: int((window - 1)/2) :]))
            else:
                flag = Filter.Error
        except:
            flag = Filter.Error
            msg = 'File can not be processed'
            
            
        return flag,revised_inputarr,newarr,msg
        
        
    

    
    


   
    
    def smoothing_plot (self,filename, window,avg_type):
        old_array = Filter.makearray(self,filename)
        
        #flag,old_array1,new_array =  Filter.moving_avg(self,old_array,window,avg_type)
        flag,old_array1,new_array,msg =  Filter.moving_avg(self,old_array,window, avg_type)
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



