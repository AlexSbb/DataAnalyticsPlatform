import numpy as np 
import pandas as pd
from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from typing import NamedTuple

#DEFINITIONS-------------------------------------------------------------------------------------------------
#Error codes
eInputOutputSize         = "Input and output array size does not match"
eTestSize                = "Test size should be in range 0.1 to 0.9"
eNoOfTrees               = "Number of trees should be in range 1 to 1000"
eUnexpected              = "Internal Error"
#Warning code
wAccuracy                = "Selected data is not appropriate to predict data"

#Flags
error   = "error"
success = "success"
warning = "Warning" 

#Constants
maxTrees              = 1000
minTrees              = 1
minTest_size          = 0.1
maxTest_size          = 0.9
column                = 1
row                   = 0
minColumn             = 2
firstRow              = 0
firstColumn           = 0
defSplit              = 40
defSplitLeaf          = 42
maxAccuracy           = 100.0
recommendedAccuracy   = 70

# Input structure for Neural Network
class RF_inputs(NamedTuple):
    X:                  float # input
    y:                  float # output
    trees:              int   # Number Of Trees
    test_size:          float # test size
    historical_data:    bool  # Historical Data

# Output structure for Neural Network
class RF_outputs(NamedTuple):
    flag:                           str    # flag check
    y_test:                         float  # resulting output
    X_test:                         float  # test input
    y_actual:                       float  # expected output
    length:                         int    # length of y_test
    test_mean_squared_error:        float  # mean square error
    test_accuracy:                  float  # accuracy
    message:                        str    # string
#END OF DEFINITIONS------------------------------------------------------------------------------------------

#IMPORTING DATA----------------------------------------------------------------------------------------------
# input dataset 

# X1 = [  [4.5,6.7],
#         [8.9,3.8],
#         [9,6.8],
#        [12.3,8.8] ]

# output dataset            
#y1 = [8.55055,5.53195,9.1547,11.91745]
#END OF IMPORTING DATA---------------------------------------------------------------------------------------

# Input initialization
#RF_inputs1 = RF_inputs(X1,y1,300,0.5,False)

# Random Forest regressor function---------------------------------------------------------------------------
def RFreg(RF_inputs):
    try:
        #Error Checks
        #Check size of input and output
        if  len(RF_inputs.X) != len(RF_inputs.y):                                           
            RF_outputs.flag = error
            RF_outputs.message  = eInputOutputSize

        #Check number of trees is in range 1 to 1000   
        elif RF_inputs.trees < minTrees or RF_inputs.trees > maxTrees:                      
            RF_outputs.flag = error
            RF_outputs.message  = eNoOfTrees

        #Check test size is in range 0.1 to 0.9   
        elif RF_inputs.test_size < minTest_size or RF_inputs.test_size > maxTest_size:      
            RF_outputs.flag = error
            RF_outputs.message  = eTestSize
           
        else:
            #Take historical input as second input if the passed input series has only one input
            c = np.shape(RF_inputs.X)[column]
            r = np.shape(RF_inputs.X)[row]
            if c < minColumn and RF_inputs.historical_data:
                rfX1 = np.delete(RF_inputs.X,r-1,firstColumn)
                rfX2 = np.delete(RF_inputs.X,0,0)
                rfX2 = np.append(rfX2,rfX1,axis=1)
                rfy1 = np.delete(RF_inputs.y,firstRow,firstColumn)
            else:
                rfX2 = RF_inputs.X
                rfy1 = RF_inputs.y
            regressor = RandomForestRegressor(n_estimators = RF_inputs.trees, random_state = defSplitLeaf) 
            #Train the model with training data and test it with test data  (80% train and 20% test)
            X_train, RF_outputs.X_test, y_train, RF_outputs.y_actual = train_test_split(rfX2, rfy1, 
            test_size= RF_inputs.test_size, random_state=defSplit)
            # fit the regressor with x and y data 
            regressor.fit(X_train, y_train)   
            # Predicting the test output values 
            RF_outputs.y_test = regressor.predict(RF_outputs.X_test)
            #Formatting the y_test values and finding it's length
            RF_outputs.y_test = np.ndarray.tolist(RF_outputs.y_test)
            RF_outputs.length = len(RF_outputs.y_test)
            #Formatting X_test
            RF_outputs.X_test = np.column_stack(RF_outputs.X_test)
            RF_outputs.X_test = np.ndarray.tolist(RF_outputs.X_test)
            #Mean squared error and accuracy
            RF_outputs.test_mean_squared_error = mean_squared_error(RF_outputs.y_actual, RF_outputs.y_test)
            RF_outputs.test_accuracy = maxAccuracy -  RF_outputs.test_mean_squared_error
            if RF_outputs.test_accuracy < recommendedAccuracy:
                RF_outputs.flag = warning
                RF_outputs.message  = wAccuracy
            else:
                RF_outputs.flag = success
                    
    except:
        RF_outputs.flag = error
        RF_outputs.message  = eUnexpected
       
    finally:
        return RF_outputs    
#End of Random forest function-------------------------------------------------------------------------------

# # Function call
# RF_outputs1 = RFreg(RF_inputs1)

# # Output result
# if RF_outputs1.flag == error:
#     print(RF_outputs1.message)
# else:
#     #Printing outputs
#     print('flag:                   ', RF_outputs1.flag)
#     print('Predicted Output:       ', RF_outputs1.y_test)
#     print('test input:             ', RF_outputs1.X_test)
#     print('expected output:        ', RF_outputs1.y_actual)
#     print('length of output array: ', RF_outputs1.length)
#     print('Mean Square error:      ', RF_outputs1.test_mean_squared_error)
#     print('Accuracy:               ', RF_outputs1.test_accuracy)
#     if RF_outputs1.flag == warning:
#         print(RF_outputs1.message)
