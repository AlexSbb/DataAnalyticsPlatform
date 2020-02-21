# -*- coding: utf-8 -*-
"""

"""
 
    
###Smoothing testing cases #####
from Filter import Filter 
obj = Filter();

#To test the moving average for array size 
testVal = obj.movingAvg([[2,3]],2,'backward')#not working
 
if testVal[0] == 'error':

    testMovingAvg1 = True
    print('Test case: wrong array size check -> passed')
else:
    testMovingAvg1 = False
    print('Test case: wrong array size  -> not passed::', testVal[3])

#To test the moving average for backward
testVal = obj.movingAvg([[2,3,5,7,8]],2,'backward')
 
if testVal[0] == 'success':

    testMovingAvg2 = True
    print('Test case: normal backward moving average -> passed')

else:
    testMovingAvg2 = False
    print('Test case: normal backward moving average -> not passed::', testVal[3])
    
#To test the moving average for forward   
testVal = obj.movingAvg([[2,3,5,7,8]],2,'forward')
if testVal[0] == 'success':

    testMovingAvg3 = True
    print('Test case: normal forward moving average -> passed')
else:
    testMovingAvg3 = False
    print('Test case: normal forward moving average -> not passed')

    
#To test the moving average for fixed  with even wondow size
testVal = obj.movingAvg([[2,3,5,7,8]],4,'fixed')
if testVal[0] == 'error':
  
    testMovingAvg4 = True
    print('Test case: ',testVal[3],'--> passed')

else:
    testMovingAvg4 = False
    print('Test case: wondow size should not be even for fixed moving average -> not passed')
    
  
#To test the moving average for fixed with odd wondow size
testVal = obj.movingAvg([[2,3,5,7,8]],3,'fixed')
if testVal[0] == 'success':

    testMovingAvg5 = True
    print('Test case: wondow size should be odd for fixed moving average -> passed')

else:
    testMovingAvg5 = False
    print('Test case: wondow size should be odd for fixed moving average -> not passed')


#To test the moving average for  wondow size bigger than array size 
testVal =  obj.movingAvg([[2,3,5,7,8]],7,'backward')    
if testVal[0] == 'error':

    testMovingAvg6 = True
    print('Test case: ',testVal[3],'--> passed')
else:
    testMovingAvg6 = False
    print('Test case: wondow size should not be bigger than array size  -> not passed')
    
#To test the moving average for  wondow size 1 
testVal =  obj.movingAvg([[2,3,5,7,8]],1,'backward')    
if testVal[0] == 'error':

    testMovingAvg8 = True
    print('Test case: ',testVal[3],'--> passed')
else:
    testMovingAvg8 = False
    print('Test case: window should not be 1 -> not passed')

#To test the moving average for  wondow is integer
testVal =  obj.movingAvg([[2,3,5,7,8]],'a','backward')    
if testVal[0] == 'error':

    testMovingAvg7 = True
    print('Test case: ',testVal[3],'--> passed')

else:
    testMovingAvg7 = False
    print('Test case: window should be an integer -> not passed')


if testMovingAvg1 and testMovingAvg2 and testMovingAvg3 and testMovingAvg4 and testMovingAvg5 and testMovingAvg6 and testMovingAvg7 == True and  testMovingAvg8 == True:
    print('****Moving Averages all Testcases : PASSED --> see previous message for passed  test cases')
else:
    print('****Moving Averages all or some of Testcases : NOT PASSED --> see previous messages for passed and not passed scenarios ')
    
###Max and Min testcases ###

#normal max min test case 
testVal = obj.maxMin([2,3,5,7,8,15,24],15,3)
if testVal[0] == 'success':

    testmaxMin1 = True
    print('Test case: normal max min function --> passed')
else:
    testmaxMin1 = False
    print('Test case: normal max min function --> not passed::',testVal[3])

# test case : Outlier percentage is 100 %.    
testVal = obj.maxMin([2,3,5,7,8],15, 10)

if testVal[0] == 'error':
    
    testmaxMin2 = True
    print('Test case: ',testVal[3],'--> passed')
else:
    testmaxMin2 = False
    print('Test case:  Outlier percentage is 100 %. Put proper Max and min values --> not passed ')  

# test case : Max value is lower than Min value
testVal = obj.maxMin([2,3,5,7,8],5, 10)    
if testVal[0] == 'error':
    
    testmaxMin3 = True
    print('Test case: ',testVal[3],'--> passed')
else:
    testmaxMin3 = False
    print('Test case:  Max value is lower than Min value --> not passed')

# test case : Max value equal to Min value
testVal = obj.maxMin([2,3,5,7,8],17, 17)
if testVal[0] == 'error':

    testmaxMin4 = True
    print('Test case: ',testVal[3],'--> passed')
else:
    testmaxMin4 = False
    print('Test case:  Max value equal to Min value --> not passed')

#To test the max min for array size 
testVal = obj.maxMin([2],9,1)
 
if testVal[0] == 'error':

    testmaxMin5 = True
  
    print('Test case: ',testVal[3],'--> passed')
else:
    testmaxMin5 = False
    print('Test case: wrong array size  --> not passed')
 
#test case for there is no outlier values    
testVal = obj.maxMin([2,4,6,7,8],8,1)
 
if testVal[0] == 'error':

    testmaxMin6 = True
  
    print('Test case: ',testVal[3],'--> passed')
else:
    testmaxMin6 = False
    print('Test case: wrong array size  -> not passed')

if testmaxMin1 and testmaxMin2 and testmaxMin3 and testmaxMin4 == True and testmaxMin5 == True and testmaxMin6 == True:
    print('****Max Min all Testcases : PASSED --> see previous message for passed  test cases')
else:
    print('****Max Min all or some of Testcases : NOT PASSED --> see previous messages for passed and not passed scenarios')


###Standard Deviation ###
#normal standard deviation test case
testVal = obj.stdDev([2,3,5,7,8,15,24],1)
if testVal[0] == 'success':

    teststdDev1 = True
    print('Test case: normal standard deviation --> passed')
else:
    teststdDev1 = False
    print('Test case: normal standard deviation --> passed:: ',testVal[5])
    

testVal = obj.stdDev([2,3,5,7,8,15,24],'a')
if testVal[0] == 'error':

    teststdDev2 = True
    print('Test case: ',testVal[5],'--> passed')
else:
    teststdDev2 = False
    print('Test case: window should be an integer -> not passed')

#test case standard deviation factor should be between 1 and 6 
testVal = obj.stdDev([2,3,5,7,8,15,24],9)    
if testVal[0] == 'error':

    teststdDev3 = True
    print('Test case: ',testVal[5],'--> passed')
else:
    teststdDev3 = False
    print('Test case: standard deviation factor should be between 1 and 6 -> not passed')


#To test the standard deviation for array size      
testVal = obj.stdDev([2],2)

if testVal[0] == 'error':

    teststdDev4 = True
  
    print('Test case: ',testVal[5],'--> passed')
else:
    teststdDev4 = False
    print('Test case: wrong array size  --> not passed')
    
if teststdDev1 and teststdDev2 and teststdDev3 == True:
    print('****Standard Deviation all Testcases : PASSED')
else:
    print('****Standard Deviation all or some Testcases : NOT PASSED')   

###Interpolation Test cases###

#test normal linear interpolation  
testVal = obj.interpolation([2,3,5,7,8,15,24,47],[0, 1, 5, 6, 7],0,11,5)  
if testVal[0] == 'success':

    testinterpolation1 = True
    print('Test case: linear standard deviation --> passed')
    
else:
    testinterpolation1 = False
    print('Test case: linear standard deviation --> not passed:: ',testVal[2])    
    
#test normal quadratic interpolation 
testVal = obj.interpolation([2,3,5,7,8,15,24,47],[0, 1, 5, 6, 7],1,11,5)
if testVal[0] == 'success':

    testinterpolation2 = True
    print('Test case: quadratic standard deviation --> passed')
else:
    testinterpolation2 = False
    print('Test case: quadratic standard deviation --> not passed:: ',testVal[2]) 

#test linear interpolation for consecutive outliers at 1st position of array 
testVal = obj.interpolation([2,3,15,5,7,8,6,8,9,1,7,4,10,2],[0, 1, 2, 9, 11, 13],0,11,5)
if testVal[0] == 'success':

    testinterpolation3 = True
    print('Test case: linear interpolation for consecutive outliers at 1st position of array  --> passed')
else:
    testinterpolation3 = False
    print('Test case: linear interpolation for consecutive outliers at 1st position of array  --> not passed::',testVal[2])
#test quadratic interpolation for consecutive outliers at 1st position of array  
testVal = obj.interpolation([2,3,15,5,7,8,6,8,9,1,7,4,10,2],[0, 1, 2, 9, 11, 13],1,11,5)
if testVal[0] == 'success':

    testinterpolation4 = True
    print('Test case: quadratic interpolation for consecutive outliers at 1st position of array  --> passed')
else:
    testinterpolation4 = False
    print('Test case: quadratic interpolation for outlier at last position of array  --> not passed::',testVal[2])    
    
#test last position as outlier for linear interpolation 
testVal = obj.interpolation([3,8,6,8,9,1,7,4,10,2,2,3],[0, 5, 7, 9, 10, 11],0,11,5)
if testVal[0] == 'success':
 
    testinterpolation5 = True
    print('Test case: linear interpolation for  outliers at last position of array  --> passed')
else:
    testinterpolation5 = False
    print('Test case: linear interpolation for  outliers at last position of array  --> not passed::',testVal[2])
    

#test last position as outlier for linear interpolation
testVal =  obj.interpolation([3,8,6,8,9,1,7,4,10,2,2,3],[0, 5, 7, 9, 10, 11],1,11,5)  
if testVal[0] == 'success':

    testinterpolation6 = True
    print('Test case: quadratic consecutive interpolation for  outliers at last position of array  --> passed')
else:
    testinterpolation6 = False
    print('Test case: quadratic consecutive interpolation for  outliers at last position of array  --> not passed::',testVal[2])
    
if obj.interpolation([1,8,76,8,9,7,10,4,2,2,3,10,7,15,8,98],[0, 2, 7, 8, 9, 10, 13, 15],0,11,5)[0] == 'success':
   
    testinterpolation7 = True
    print('Test case passed')
else:
    testinterpolation7 = False
    print('Test case not passed')
    
if obj.interpolation([1,8,76,8,9,7,10,4,2,2,3,10,7,15,8,98],[0, 2, 7, 8, 9, 10, 13, 15],1,11,5)[0] == 'success':

    testinterpolation8 = True
    print('Test case passed')
else:
    testinterpolation8 = False
    print('Test case not passed')
    
if obj.interpolation([1,3,76,8,-2,7,10,4,2,2,10,-6,7,15,0,98],[0, 1, 2, 4, 7, 8, 9, 11, 13, 14, 15],0,11,5)[0] == 'success':

    testinterpolation9 = True
    print('Test case passed')
else:
    testinterpolation9 = False
    print('Test case not passed')
    
if obj.interpolation([1,3,76,8,-2,7,10,4,2,2,10,-6,7,15,0,98],[0, 1, 2, 4, 7, 8, 9, 11, 13, 14, 15],1,11,5)[0] == 'success':

    testinterpolation10 = True
    print('Test case passed')
else:
    testinterpolation10 = False
    print('Test case not passed')

if testinterpolation1 and testinterpolation2 and testinterpolation3 and testinterpolation4 and testinterpolation5 and testinterpolation6 and testinterpolation7 and testinterpolation8 and testinterpolation9 and testinterpolation10 == True:
    print('****Interpolation all Testcases : PASSED')
else:
    print('****Interpolation all  or some Testcases : NOT PASSED')


    

    
    
    




  
                
            
    

    
    
        