# -*- coding: utf-8 -*-
"""
"""
import numpy as np
from scipy import interpolate

np.nan


"""
    *****************************************************************************************************************************
    Filter class is comprising methods for  data filtering and smoothing functionality
    
    constants:: used in methods as a fix value
    
    Flags used in methods to identify whether the method is successfull or failure.   
    error      : 'error'
    success    : 'success'
    
    Error messages used in different methods.
    eMsg1  : 'Internal Error'
    eMsg2  : 'For fixed moving average provide odd numbers of window '
    eMsg3  : 'Window is bigger than the input length.'
    eMsg4  : 'Number of input values less than 3'
    eMsg5  : 'Provide a proper moving average type'
    eMsg6  : 'Provide a Integer value '
    eMsg7  : 'There is no outlier values to interpolate'
    eMsg8  : 'Outlier percentage is 100 %. Put proper Max and min values'
    eMsg9  : 'Provide a valid interpolation type'
    
    arrayLenLimit   : lower limit for number of data in input array i.e 3
    stdDevFactorMax : standard deviation factor upper limit i.e 6
    stdDevFactorMin : standard deviation factor lower limit i.e 1
        
    methods::
    maxMin(inDataArray, inMaxLim, inMinLim) : Finding outlier indexes of input array or input data based on max and min limit provided by the user.
    stdDev(inDataArray, inStdDevFact)       : This measures the amount of variation or dispersion in the input array or input data depending on the standard deviation factor.
    movingAvg(inDataArray, inWindow, inMavgType) : This calculates the moving average for the data to move forward,backward or fixed by the number of windows.
    countConsec(indexVal, inOutlierArray)  : This methods calculates the 1st consecutive dataset in a given array staring from a given index
    count(inOutlierArray):  This methods calculates number of consecutive data sets
    interpolation(inDataArray, inOutlierArray, inIntpTyp, inMaxLim, inMinLim): method to construct new data points within the range of a discrete set of known data points
    
                                                   
    *****************************************************************************************************************************"""


class Filter():
    
    # creates constructor with the instance self to access the attributes and methods of the class
    def __init__(self):
        pass  #null operator
        
        
    error      = 'error'
    success    = 'success'
    eMsg1      = 'Internal Error'
    eMsg2      = 'For fixed moving average provide odd numbers of window '
    eMsg3      = 'Window is bigger than the input length.'
    eMsg4      = 'Number of input values less than 3'
    eMsg5      = 'Provide an proper moving average type'
    eMsg6      = 'Provide an Integer value '
    eMsg7      = 'There is no outlier values to interpolate'
    eMsg8      = 'Outlier percentage is 100 %. Put proper Max and min values'
    eMsg9      = 'Provide a valid interpolation type'
    cArrayLenLimit = 3
    cStdDevFactMax = 6
    cStdDevFactMin = 1

    """
    ******************************************************************************************************************************************
    method maxMin          : Finding outlier indexes based on max and min limit provided by user
        inDataArray        : input array provided to find outlier
        inMaxLim           : Max limit provided by user
        inMinLim           : Min limit provided by user

    variables:
 
        arrayMaxval        : Max value in input array
        arrayMinval        : Min value in input array
            
     return:
        flag               : success or error         
        outOPercent        : Calculates de amount of data that is identyfied as an Outlier with respect to the total data.  Calculated in [%]
        outOutlierArray    : Array with identyfied rows that are detected as Outliers.
        msg                : success or error massage reason 
    *******************************************************************************************************************************************"""

    def maxMin(self, inDataArray, inMaxLim, inMinLim):

        #initializing
        outOutlierArray = []
        outOPercent = 0
        
        flag = Filter.success
        msg = ''
        
        # providing try block to handle exceptions
        try:
            # checking valid length of array
            if (len(inDataArray) < Filter.cArrayLenLimit):
                msg = Filter.eMsg4  # 'Number of input values less than 3'
                flag = Filter.error  
                return flag, outOPercent, outOutlierArray, msg
            
            # checking if max value provided is less than min value 
            if (inMaxLim < inMinLim):
                flag = Filter.error
                msg = 'Max value is lower than Min value'
                
            # checking if max value provided is equal to min value
            elif (inMaxLim == inMinLim):
                flag = Filter.error
                msg = 'Max value equal to than Min value'
            else:
                arrayMaxVal = max(inDataArray) #getting max input data
                arrayMinVal = min(inDataArray) #getting min input data
                
                #checking if there is any outlier values
                if(inMaxLim >= arrayMaxVal  and inMinLim <= arrayMinVal):
                    flag = Filter.error      
                    msg  = Filter.eMsg7      # meassage 'There is no outlier values to interpolate'
                    return flag, outOPercent, outOutlierArray, msg

                #fininding outlier index of original array
                for index in range(len(inDataArray)):
                    
                    if inDataArray[index] > inMaxLim or inDataArray[index] < inMinLim:
                        outOutlierArray.append(index)
                        outOPercent = len(outOutlierArray) * 100 / len(inDataArray) #percentage of outlier
                        
                #checking if 100 percent of data is outliers
                if (outOPercent == 100):
                    flag = Filter.error 
                    msg  = Filter.eMsg8
                        
        # handling exceptions in except block                        
        except:
            flag = Filter.error 
            msg  = Filter.eMsg1  # unexpected error

        return flag, outOPercent, outOutlierArray, msg # returing flag(sucess or error),outlier percentage,outlier index, message

    """
    *****************************************************************************************************************************
    method stdDev          : This method provide measure of the amount of variation or dispersion in input data using standard deviation factor.
        inDataArray        : input array provided to find outlier
        inStdDevFact       : Factor that multiply the Standard Deviation and is used to calculate the MaxValue and MinValue for the limits.
                             currenty using standard deviation factor only for values 1 to 6

    variables:
        stdDev             : Calculates the Standard Deviation of the Data
        stdMean            : Calculates the Mean of the Data
            
     return:
        flag               : success or error         
        outOPercent        : Calculates the amount of data that is identyfied as an Outlier with respect to the total data.  Calculated in [%]
        outOutlierArray    : Array with identyfied rows that are detected as Outliers.
        outMaxLim          : Calculates the Maximum Value limit 
        outMinLim          : Calculates the Minimum Value limit
        msg                : success or error massage reason        
    *****************************************************************************************************************************"""

    def stdDev(self, inDataArray, inStdDevFact):

        outOutlierArray = []  # initializing array
        flag = Filter.success
        msg = ''

        # providing try block to handle exceptions
        try:
            # initializing variables
            outOPercent = 0
            outMaxLim = 0
            outMinLim = 0

            #catch error that the StdDevFact should be an integer value
            if type(inStdDevFact) != int:
                msg = Filter.eMsg6   # 'Provide a Integer value '
                flag = Filter.error
                return flag, outOPercent, outOutlierArray, outMaxLim, outMinLim, msg


            # check the range of standard deviation factor
            if inStdDevFact > Filter.cStdDevFactMax or inStdDevFact < Filter.cStdDevFactMin:
                msg = 'standard deviation factor should be between ' + str(Filter.cStdDevFactMin) + ' and ' + str(
                    Filter.cStdDevFactMax)
                flag = Filter.error  
                return flag, outOPercent, outOutlierArray, outMaxLim, outMinLim, msg  # returing flag(error),0,[],0,0, message

            # checking valid length of array
            if len(inDataArray) < Filter.cArrayLenLimit:
                msg = Filter.eMsg4  # 'Number of input values less than 3'
                flag = Filter.error 
                return flag, outOPercent, outOutlierArray, outMaxLim, outMinLim, msg  # returing flag(error),0,[],0,0, message

            # calculation with valid length of array
            else:
                
                stdDev = np.std(inDataArray, axis=0)          #calculated standard deviation
                stdMean = np.mean(inDataArray, axis=0)        #calculated min
                outMaxLim = stdMean + (stdDev * inStdDevFact) # calculated max limit
                outMinLim = stdMean - (stdDev * inStdDevFact) #calculated min limit

                # calls the maxMin to detect the outliers based on calculated MaxLim and MinLim
                flag, outOPercent, outOutlierArray, msg = Filter.maxMin(self, inDataArray, outMaxLim, outMinLim)
                
        # handling exceptions in except block
        except:
            flag = Filter.error 
            msg  = Filter.eMsg1  # unexpected error
            

        return flag, outOPercent, outOutlierArray, outMaxLim, outMinLim, msg  # returing flag(success or error),outlier percentage,outlier index,max limit,min limit, message

    """
    *****************************************************************************************************************************    
    method movingAvg    : This calculate the moving average for the data to move forward,backward or fixed by the number of windows 
                          determined by the trader or the user
    parameters:
        inDataArray     : input array provided to smooth data
        inWindow        : window to calculate moving average
        inMavgType      : type of moving average.default avgType = bakward 
                          the values can be either of these three values according to user.
                          1.forward
                          2.bakward
                          3.fixed
    variables:
        values           : array to capture intermediate values after convolution
        weights          : array calulated with numpy Repeat method anf geting output of size window and  value 1.0/window
                          
        revArray         : intermediate array to calcuate final array
        inputArrayLen    : number of input
        i,j,k            : used for looping
            
     return:
        flag             : success or error         
        outSmArray           : array containing smoothed data
        outRevArray      : revised input data according to type of moving average and window
        msg              : success or error massage reason
    *****************************************************************************************************************************"""

    def movingAvg(self, inDataArray, inWindow, inMavgType):

        flag = Filter.success
        msg = ''

        # providing try block to handle exceptions
        try:

            if inMavgType is None:
                inMavgType = 'backward'  # checking if moving average type is null and setting default value

            # initializing  array
            values = []
            outSmArray = []
            revArray = []
            outRevArray = []

            # checking wondow is integer
            if type(inWindow) != int:
                msg = Filter.eMsg6   #message 'Provide a Integer value '
                flag = Filter.error 
                return flag, outRevArray, outSmArray, msg

            weights = np.repeat(1.0, inWindow) / inWindow  # array of window size with value 1.0/window
            inputArrayLen = len(inDataArray)               # calculating number of input

            # checking valid length of array
            if (len(inDataArray[0]) < Filter.cArrayLenLimit):
                msg = Filter.eMsg4   #message 'Number of input values less than 3'
                flag = Filter.error 
                return flag, outRevArray, outSmArray, msg

            # checking the window not crossing 1 and length of input data
            if (inWindow == 1 or inWindow > len(inDataArray[0])):
                flag = Filter.error  
                if (inWindow == 1):
                    msg = 'window should not be 1'
                else:
                    msg = Filter.eMsg3  # 'Window is bigger than the input length.'
                return flag, outRevArray, outSmArray, msg

                # if window is in range
            else:
                for i in range(inputArrayLen):       # loop for 1 or more data input
                    values = np.convolve(inDataArray[i], weights, 'valid')  # calculating moving average
                    outSmArray.append(values)        # appending smoothed data
                    if inMavgType == 'forward':
                        for j in range(inputArrayLen):
                            outRevArray.append(np.flip(np.delete(np.flip(inDataArray[j]), np.s_[0: int(
                                inWindow - 1):])))   # deleting extra data from backside of input array

                    elif inMavgType == 'backward':
                        for j in range(inputArrayLen):
                            outRevArray.append(np.delete(inDataArray[j],
                                                         np.s_[0: inWindow - 1:]))  # deleting extra data from front of input array

                    elif inMavgType == 'fixed':
                        if (inWindow % 2 != 0):
                            for j in range(inputArrayLen):
                                revArray.append(np.flip(np.delete(np.flip(inDataArray[j]), np.s_[0: int(
                                    (inWindow - 1) / 2):])))  # deleting extra data from backside of input array
                            for k in range(inputArrayLen):
                                outRevArray.append(np.delete(revArray[k], np.s_[0: int(
                                    (inWindow - 1) / 2):]))   # deleting extra data from front of input array
                        else:
                            flag = Filter.error  
                            msg = Filter.eMsg2   # message 'For fixed moving average provide odd numbers of window '
                    else:
                        flag = Filter.error  
                        msg = Filter.eMsg5  # message 'Provide a proper moving average type'

        # handling exceptions in except block
        except:
            flag = Filter.error  
            msg = Filter.eMsg1  # unexpected error
        return flag, outRevArray, outSmArray, msg  # returing flag(success or error),reviced input array,smoothed array, messsage

    """
    *****************************************************************************************************************************    
    method countConsec  : This methods calculates the 1st consecutive dataset in a given array staring from a given index
    parameters:
        indexVal        : starting index for the search of consecutive dataset
        inOutlierArray  : Array containg all outlier data index of original data set 

    variables:
        count           : used for intermediate counting 
                          
     return:
        outIndexBegin   : begining of consecutive data
        outIndexEnd     : end of consecutive data
        i               : outlierMatrix array index where the current dataset seaching stoppep 
    *****************************************************************************************************************************"""

    def countConsec(self, indexVal, inOutlierArray):
        
        #initializing
        count = 0
        outIndexEnd = 0
        outIndexBegin = inOutlierArray[indexVal]

        #looping through all data in outlierMatrix to find consecutive data set
        for i in range(indexVal, len(inOutlierArray) - 1):
            #searching if there is any data set equals to its next data set
            if inOutlierArray[i + 1] == inOutlierArray[i] + 1:
                count += 1 # counting a value how many times the loop is executing for a specific consecutive sequence
                if count == 1:
                    outIndexBegin = inOutlierArray[i] # assigning the begining index of consecutive sequence
                outIndexEnd = inOutlierArray[i + 1] # assighing the last index of consecuitive sequence
                
            else:
                if (count != 0):
                    break #breacking out the loop if we have already found a consecutive sequence

        return outIndexBegin, outIndexEnd, i #returning begining ,ending of consecuive sequence,stopping index where the search stopped
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

    def count(self, inOutlierArray):

        # initializing
        count = 0
        count1 = 0

        # looping through for count how many consecutives values are in the inOutlierArray
        for i in range(len(inOutlierArray) - 1):
            if inOutlierArray[i + 1] == inOutlierArray[i] + 1:
                count += 1
            else:
                if count != 0:
                    count1 = count1 + 1
                    count = 0
        if count != 0:
            count1 += 1

        return count1
    
    """
    *****************************************************************************************************************************    
    method::
        interpolation   :  method to construct new data points within the range of a discrete set of known data points
    parameters::
        inDataArray     : input array provided to find interpolated data set
        inOutlierArray  : Array containg all outlier data index of original data set
        inIntpTyp       : Type of Interpolation 
                          0 = Linear
                          1 = Quadratic
                          
        inMaxLim        : Max limit provided by user or calculated using standard deviation
        inMinLim        : Min limit provided by user or calculated using standard deviation

    variables::
        intpArrayIndex1 : intermediate array to calculate linear interpolation
        indexVal        : index value for consecutive values
        indexBegin      : index Begin for consecutive values
        indexEnd        : index End for consecutive values
        counter         : counter for number of different consecutives outliers to replace 
     return::
        flag            : success or error         
        outSmArray      : array containing smoothed data
        outRevArray     : revised input data according to type of moving average and window
        msg             : success or error massage reason
        count1          : number of consecutive data set
    *****************************************************************************************************************************"""


    def interpolation(self, inDataArray, inOutlierArray, inIntpTyp, inMaxLim, inMinLim):
        
        #initializing with default values
        flag = Filter.success
        msg = ''
        outIntpArray = []

        #convert 0 to False and 1 to True
        if inIntpTyp == 0 or inIntpTyp == 'Linear':
            inIntpTyp = False
        elif inIntpTyp == 1 or inIntpTyp == 'Quadratic':
            inIntpTyp = True
        
        # providing try block to handle exceptions        
        try:
            # checking valid length of array
            if len(inDataArray) < Filter.cArrayLenLimit:
                msg = Filter.eMsg4  # 'Number of input values less than 3'
                flag = Filter.error  # activates flag
                return flag, outIntpArray, msg

            # checking if max value provided is less than min value
            if (inMaxLim < inMinLim):
                flag = Filter.error
                msg = 'Max value is lower than Min value'

            # checking if max value provided is equal to min value
            elif (inMaxLim == inMinLim):
                flag = Filter.error
                msg = 'Max value equal to than Min value'

            # cheching the inIntpTyp is a true or false value
            elif type(inIntpTyp) != bool:
                msg = Filter.eMsg9   # 'Provide a Boolean value '
                flag = Filter.error
                return flag, outIntpArray, msg

            else:

                outIntpArray = inDataArray.copy()                        # coping original data
                # Linear interpolation
                if inIntpTyp == False:
                    intpArrayIndex1 = np.zeros([len(inOutlierArray), 3]) # creating intermediate array to calculate linear interpolation
                    for i in range(len(inOutlierArray)):                 # looping through range of number of outlier data

                        # handing case for 1st data as it is in boundary
                        if inOutlierArray[i] == 0:

                            #checking data is near to max limit or min limit
                            if (abs(inDataArray[inOutlierArray[i]] - inMaxLim) >
                                    abs(inDataArray[inOutlierArray[i]] - inMinLim)):
                                intpArrayIndex1[i][0] = inMinLim         # taking min limit to interpolate
                            else:
                                intpArrayIndex1[i][0] = inMaxLim         # taking max limit to interpolate

                        else:
                            intpArrayIndex1[i][0] = inDataArray[inOutlierArray[i] - 1] # taking previous value to interpolate

                        intpArrayIndex1[i][1] = inDataArray[inOutlierArray[i]] # taking current value to interpolate

                        # handing case for last data as it is in boundary
                        if (inOutlierArray[i] + 1) >= len(inDataArray):

                            #checking data is near to max limit or min limit
                            if abs(inDataArray[inOutlierArray[i]] - inMaxLim) > \
                                    abs(inDataArray[inOutlierArray[i]] - inMinLim):
                                intpArrayIndex1[i][2] = inMinLim        # taking min limit to interpolate
                            else:
                                intpArrayIndex1[i][2] = inMaxLim        # taking max limit to interpolate
                        else:
                            intpArrayIndex1[i][2] = inDataArray[inOutlierArray[i] + 1] # taking next value to interpolate

                        #load the values for the interpolation.
                        f = interpolate.interp1d([inOutlierArray[i] - 1, inOutlierArray[i] + 1],
                                                 [intpArrayIndex1[i][0], intpArrayIndex1[i][2]],
                                                 kind='linear')
                        #Replace Outlier value with the interpolation at the outlier position
                        outIntpArray[inOutlierArray[i]] = round(float(f(inOutlierArray[i])), 4)

                    counter = Filter.count(self, inOutlierArray) #number of consecutive iteration

                    #initializing
                    indexVal = 0

                    #while there is consecutive data set below code will execute
                    while counter != 0:
                        counter = counter - 1
                        indexBegin, indexEnd, indexVal = Filter.countConsec(self, indexVal, inOutlierArray) #getting begin and end data of one cosecutive data set
                        indexVal += 1

                        # looping through range of number of consecutive outlier data
                        for i in range(indexEnd - indexBegin + 1):
                            intpArrayIndex2 = np.zeros([indexEnd - indexBegin + 1, 3])  # creating intermediate array to calculate linear interpolation
                            intpVal = indexBegin + i  # increase initial intpVal for consecutive loops

                            # handling case for first data as the consecutive value
                            if indexBegin == 0:

                                #checking data is near to max limit or min limit
                                if abs(inDataArray[indexBegin] - inMaxLim) > abs(inDataArray[indexBegin] - inMinLim):
                                    intpArrayIndex2[i][0] = inMinLim  # taking min limit to interpolate
                                else:
                                    intpArrayIndex2[i][0] = inMaxLim  # taking max limit to interpolate
                            else:
                                intpArrayIndex2[i][0] = inDataArray[indexBegin - 1] # taking previous data to interpolate

                            intpArrayIndex2[i][1] = inDataArray[intpVal]  # taking current value to interpolate

                            # handling case for last data as a consecutive value
                            if (indexEnd + 1) >= len(inDataArray):

                                #checking data is near to max limit or min limit
                                if abs(inDataArray[indexEnd] - inMaxLim) > abs(inDataArray[indexEnd] - inMinLim):
                                    intpArrayIndex2[i][2] = inMinLim  # taking min limit to interpolate
                                else:
                                    intpArrayIndex2[i][2] = inMaxLim  # taking max limit to interpolate
                            else:
                                intpArrayIndex2[i][2] = inDataArray[indexEnd + 1] # taking next data to interpolate

                            # load the values for the interpolation.
                            f = interpolate.interp1d([indexBegin - 1, indexEnd + 1],
                                                     [intpArrayIndex2[i][0],
                                                      intpArrayIndex2[i][2]],
                                                     kind='linear')
                            # Replace Outlier value with the interpolation at the outlier position
                            outIntpArray[intpVal] = round(float(f(intpVal)), 4)


                # Quadratic interpolation
                elif inIntpTyp == True:
                    intpArrayIndex1 = np.zeros([len(inOutlierArray), 5]) # creating intermediate array to calculate linear interpolation
                    for i in range(len(inOutlierArray)):                 # looping through range of number of outlier data

                        # handling case for first data as it is in boundary
                        if inOutlierArray[i] == 0:

                            #checking data is near to max limit or min limit
                            if abs(inDataArray[inOutlierArray[i]] - inMaxLim) > \
                                    abs(inDataArray[inOutlierArray[i]] - inMinLim):
                                intpArrayIndex1[i][0] = inMinLim   # taking min limit to interpolate
                                intpArrayIndex1[i][1] = inMinLim  # taking min limit to interpolate
                            else:
                                intpArrayIndex1[i][0] = inMaxLim  # taking max limit to interpolate
                                intpArrayIndex1[i][1] = inMaxLim  # taking max limit to interpolate

                        # handing case for second data as it use one value out of boundary
                        elif inOutlierArray[i] == 1:
                            #checking data is near to max limit or min limit
                            if abs(inDataArray[inOutlierArray[i]] - inMaxLim) > \
                                    abs(inDataArray[inOutlierArray[i]] - inMinLim):
                                intpArrayIndex1[i][0] = inMinLim   # taking min limit to interpolate
                                intpArrayIndex1[i][1] = inDataArray[inOutlierArray[i] - 1] # taking previos value to interpolate
                            else:
                                intpArrayIndex1[i][0] = inMaxLim   # taking max limit to interpolate
                                intpArrayIndex1[i][1] = inDataArray[inOutlierArray[i] - 1] # taking previos value to interpolate

                        else:
                            intpArrayIndex1[i][0] = inDataArray[inOutlierArray[i] - 2]  # taking previous to previos value to interpolate
                            intpArrayIndex1[i][1] = inDataArray[inOutlierArray[i] - 1]  # taking previos value to interpolate

                        intpArrayIndex1[i][2] = inDataArray[inOutlierArray[i]] # taking current value to interpolate

                        # handling case for last data as a consecutive value
                        if (inOutlierArray[i] + 1) >= len(inDataArray):

                            #checking data is near to max limit or min limit
                            if abs(inDataArray[inOutlierArray[i]] - inMaxLim) > \
                                    abs(inDataArray[inOutlierArray[i]] - inMinLim):
                                intpArrayIndex1[i][3] = inMinLim # taking min limit to interpolate
                                intpArrayIndex1[i][4] = inMinLim # taking min limit to interpolate
                            else:
                                intpArrayIndex1[i][3] = inMaxLim # taking max limit to interpolate
                                intpArrayIndex1[i][4] = inMaxLim # taking max limit to interpolate

                        # handling case for previous to last data as a consecutive value
                        elif (inOutlierArray[i] + 2) >= len(inDataArray):

                            #checking data is near to max limit or min limit
                            if abs(inDataArray[inOutlierArray[i]] - inMaxLim) > \
                                    abs(inDataArray[inOutlierArray[i]] - inMinLim):
                                intpArrayIndex1[i][3] = inDataArray[inOutlierArray[i] + 1] # taking next value to interpolate
                                intpArrayIndex1[i][4] = inMinLim # taking min limit to interpolate
                            else:
                                intpArrayIndex1[i][3] = inDataArray[inOutlierArray[i] + 1] # taking next value to interpolate
                                intpArrayIndex1[i][4] = inMaxLim # taking max limit to interpolate
                        else:
                            intpArrayIndex1[i][3] = inDataArray[inOutlierArray[i] + 1] # taking next value to interpolate
                            intpArrayIndex1[i][4] = inDataArray[inOutlierArray[i] + 2] # taking next to next value to interpolate

                        # load the values for the interpolation.
                        f = interpolate.interp1d([inOutlierArray[i] - 2, inOutlierArray[i] - 1,
                                                  inOutlierArray[i] + 1, inOutlierArray[i] + 2],
                                                 [intpArrayIndex1[i][0], intpArrayIndex1[i][1],
                                                  intpArrayIndex1[i][3], intpArrayIndex1[i][4]],
                                                 kind='quadratic')
                        # Replace Outlier value with the interpolation at the outlier position
                        outIntpArray[inOutlierArray[i]] = round(float(f(inOutlierArray[i])), 4)

                    counter = Filter.count(self, inOutlierArray) # number of consecutive iteration

                    # initializing
                    indexVal = 0

                    # while there is consecutive data set below code will execute
                    while counter != 0:
                        counter = counter - 1
                        indexBegin, indexEnd, indexVal = Filter.countConsec(self, indexVal, inOutlierArray) # getting begin and end data of one cosecutive data set
                        indexVal += 1

                        # looping through range of number of consecutive outlier data
                        for i in range(0, indexEnd - indexBegin + 1):
                            intpArrayIndex2 = np.zeros([indexEnd - indexBegin + 1, 5]) # creating intermediate array to calculate linear interpolation
                            intpVal = indexBegin + i # increase initial intpVal for consecutive loops

                            # handling case for first data as it is in boundary
                            if indexBegin == 0:

                                #checking data is near to max limit or min limit
                                if abs(inDataArray[indexBegin] - inMaxLim) > abs(inDataArray[indexBegin] - inMinLim):
                                    intpArrayIndex2[i][0] = inMinLim # taking min limit to interpolate
                                    intpArrayIndex2[i][1] = inMinLim # taking min limit to interpolate
                                else:
                                    intpArrayIndex2[i][0] = inMaxLim # taking max limit to interpolate
                                    intpArrayIndex2[i][1] = inMaxLim # taking max limit to interpolate

                            # handing case for consecutive value in second data as it uses one value out of boundary
                            elif indexBegin == 1:
                                #checking data is near to max limit or min limit
                                if abs(inDataArray[indexBegin] - inMaxLim) > abs(inDataArray[indexBegin] - inMinLim):
                                    intpArrayIndex2[i][0] = inMinLim # taking min limit to interpolate
                                    intpArrayIndex2[i][1] = inDataArray[indexBegin - 1] # taking previous value to interpolate
                                else:
                                    intpArrayIndex2[i][0] = inMaxLim # taking max limit to interpolate
                                    intpArrayIndex2[i][1] = inDataArray[indexBegin - 1] # taking previous value to interpolate
                            else:
                                intpArrayIndex2[i][0] = inDataArray[indexBegin - 2] # taking previous to previos value to interpolate
                                intpArrayIndex2[i][1] = inDataArray[indexBegin - 1] # taking previous value to interpolate

                            intpArrayIndex2[i][2] = inDataArray[intpVal] # taking current value to interpolate

                            # handling case for last data as a consecutive value
                            if (indexEnd + 1) >= len(inDataArray):

                                #checking data is near to max limit or min limit
                                if abs(inDataArray[indexEnd] - inMaxLim) > abs(inDataArray[indexEnd] - inMinLim):
                                    intpArrayIndex2[i][3] = inMinLim # taking min limit to interpolate
                                    intpArrayIndex2[i][4] = inMinLim # taking min limit to interpolate
                                else:
                                    intpArrayIndex2[i][3] = inMaxLim # taking max limit to interpolate
                                    intpArrayIndex2[i][4] = inMaxLim # taking max limit to interpolate

                            # handling case for previous to last data as a consecutive value
                            elif (indexEnd + 2) >= len(inDataArray):

                                #checking data is near to max limit or min limit
                                if abs(inDataArray[indexEnd] - inMaxLim) > abs(inDataArray[indexEnd] - inMinLim):
                                    intpArrayIndex2[i][3] = inDataArray[indexEnd + 1] # taking next value to interpolate
                                    intpArrayIndex2[i][4] = inMinLim # taking min limit to interpolate
                                else:
                                    intpArrayIndex2[i][3] = inDataArray[indexEnd + 1] # taking next value to interpolate
                                    intpArrayIndex2[i][4] = inMaxLim # taking max limit to interpolate

                            else:
                                intpArrayIndex2[i][3] = inDataArray[indexEnd + 1] # taking next value to interpolate
                                intpArrayIndex2[i][4] = inDataArray[indexEnd + 2] # taking next to next value to interpolate

                            # load the values for the interpolation.
                            f = interpolate.interp1d([indexBegin - 2, indexBegin - 1, indexEnd + 1, indexEnd + 2],
                                                     [intpArrayIndex2[i][0],
                                                      intpArrayIndex2[i][1],
                                                      intpArrayIndex2[i][3],
                                                      intpArrayIndex2[i][4]],
                                                     kind='quadratic')
                            # Replace Outlier value with the interpolation at the outlier position
                            outIntpArray[intpVal] = round(float(f(intpVal)), 4)
                    """
                    ***********************************************************************************
                    # # Special condition for Quadratic Interpolation # #
                    #If there are still Outliers values after running quadratic interpolation,
                    # the values are replaced by Max or Min limit values using the maxMin method again.
                    ***********************************************************************************"""

                    newOutlierArray = Filter.maxMin(self, outIntpArray, inMaxLim, inMinLim)[2]

                    for i in range(len(newOutlierArray)):
                        # checking data is near to max limit or min limit
                        if abs(outIntpArray[newOutlierArray[i]] - inMaxLim) > abs(
                                outIntpArray[newOutlierArray[i]] - inMinLim):
                            outIntpArray[newOutlierArray[i]] = inMinLim # taking min limit to interpolate
                        else:
                            outIntpArray[newOutlierArray[i]] = inMaxLim # taking max limit to interpolate
                    """"*********************************************************************************"""
                # handling inIntpTyp error
                else:
                    flag = Filter.error
                    msg = Filter.eMsg1 # unexpected error

        # handling exceptions in except block
        except:
            flag = Filter.error
            msg = Filter.eMsg1 # unexpected error

        return flag, outIntpArray, msg  # returning flag(sucess or error), outIntpArray(Interpolated Array), message