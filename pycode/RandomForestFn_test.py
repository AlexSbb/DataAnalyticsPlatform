import numpy as np 
import pandas as pd
import RandomForestFn as RF

# input dataset 
X0 = [  [4.5],
        [8.9],
        [9],
        [12.3] ]
X1 = [  [4.5,6.7],
        [8.9,3.8],
        [9,6.8],
        [12.3,8.8] ]
X2 = [  [4.5,6.7],
        [8.9,3.8],
        [9,6.8] ]        

# output dataset            
y1 = [8.55055,5.53195,9.1547,11.91745]
y2 = [8.55055,5.53195,9.1547]

RF_inputs1 = RF.RF_inputs(X0,y1,300,0.5,True)
RF_inputs2 = RF.RF_inputs(X1,y1,300,0.5,False)

RF_inputs3 = RF.RF_inputs(X2,y1,300,0.5,True)
RF_inputs4 = RF.RF_inputs(X1,y2,300,0.5,True)
RF_inputs5 = RF.RF_inputs(X1,y1,300,1.1,True)
RF_inputs6 = RF.RF_inputs(X1,y1,3000,0.5,True)



#Positive cases----------------------------------------------------------

#Normal inputs should not produce error
# Function call
print('\nNormal inputs should not produce error')
RF_outputs1 = RF.RFreg(RF_inputs1)
if RF_outputs1.flag == RF.success:
    print('Case1 Run1: Pass')
else:
    print('Case1 Run1: Fail')

RF_outputs1 = RF.RFreg(RF_inputs2)
if RF_outputs1.flag == RF.success:
    print('Case1 Run2: Pass \n')
else:
    print('Case1 Run2: Fail \n')
    
#Negative cases----------------------------------------------------------

#Test input and output sizes
print('Test input and output sizes')
RF_outputs1 = RF.RFreg(RF_inputs3)
if RF_outputs1.flag == RF.error and RF_outputs1.message == RF.eInputOutputSize:
    print('Case2 Run1: Pass')
else:
    print('Case2 Run1: Fail')

RF_outputs1 = RF.RFreg(RF_inputs4)
if RF_outputs1.flag == RF.error and RF_outputs1.message == RF.eInputOutputSize:
    print('Case2 Run2: Pass \n')
else:
    print('Case2 Run2: Fail \n')

#Test testsize error
print('Test testsize error')
RF_outputs1 = RF.RFreg(RF_inputs5)
if RF_outputs1.flag == RF.error and RF_outputs1.message == RF.eTestSize:
    print('Case3 Run1: Pass \n')
else:
    print('Case3 Run1: Fail \n')

#Test illegal no of trees error
print('Test illegal no of trees error')
RF_outputs1 = RF.RFreg(RF_inputs6)
if RF_outputs1.flag == RF.error and RF_outputs1.message == RF.eNoOfTrees:
    print('Case4 Run1: Pass \n')
else:
    print('Case4 Run1: Fail \n')

#Test unecpected error

#Test minimum accuracy check
print('Selected data is not appropriate to train the model')
RF_outputs1 = RF.RFreg(RF_inputs7)
if RF_outputs1.flag == RF.warning and RF_outputs1.message == RF.wAccuracy:
    print('Case5 Run1: Pass \n')
else:
    print('Case5 Run1: Fail \n')