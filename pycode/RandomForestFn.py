import numpy as np 
import pandas as pd
from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from typing import NamedTuple

#DEFINITIONS-----------------------------------------------------------------------
#Error codes
eIoSize         = "Input and output array size does not match"
eTestSize       = "Test size should be in range 0.1 to 0.9"
eNoOfTrees      = "Number of trees should be in range 1 to 1000"
eUnexpected     = "Something went wrong"

#Flags
error = "error"
success = "success"

#Constants
maxTrees        = 1000
minTrees        = 1
minTst_siz      = 0.1
maxTst_siz      = 0.9
column          = 1
row             = 0
minColumn       = 2
firstRow        = 0
firstColumn     = 0
defSplit        = 40
defSplitLeaf    = 42
maxAccuracy     = 100.0


# Input structure for Neural Network
class RF_inputs(NamedTuple):
    X: float
    y: float
    trees: int
    tst_siz: float
    his_dat: bool

# Output structure for Neural Network
class RF_outputs(NamedTuple):
    flag:       str
    y_test:     float
    X_test:     float 
    y_actual:   float
    length:     int
    tst_mse:    float
    tst_accrc:  float
    msg:        str
#END OF DEFINITIONS--------------------------------------------------------------------

#IMPORTING DATA------------------------------------------------------------------------
# input dataset 
X1 = [   [4.5,6.7],
        [8.9,3.8],
        [9,6.8],
        [12.3,8.8] ]

# output dataset            
y1 = [8.55055,5.53195,9.1547,11.91745]
#END OF IMPORTING DATA----------------------------------------------------------------

# Input initialization
RF_inputs1 = RF_inputs(X1,y1,300,0.5,True)

# Random Forest regressor function----------------------------------------------------
def RFreg(RF_inputs):
    try:
        #Error Checks
        #check size of input and output
        if  len(RF_inputs.X) != len(RF_inputs.y):
            RF_outputs.flag = error
            RF_outputs.msg  = eIoSize
            return RF_outputs
        elif RF_inputs.trees < minTrees or RF_inputs.trees > maxTrees:
            RF_outputs.flag = error
            RF_outputs.msg  = eNoOfTrees
            return RF_outputs
        elif RF_inputs.tst_siz < minTst_siz or RF_inputs.tst_siz > maxTst_siz:
            RF_outputs.flag = error
            RF_outputs.msg  = eTestSize
            return RF_outputs
        else:
            #Take historical input as second input if the passed input series has only one input
            c = np.shape(RF_inputs.X)[column]
            r = np.shape(RF_inputs.X)[row]
            if c < minColumn and RF_inputs.his_dat:
                X3 = np.delete(RF_inputs.X,r-1,firstColumn)
                RF_inputs.X = np.delete(RF_inputs.X,firstRow,firstColumn)
                RF_inputs.X = np.append(RF_inputs.X,X3,axis=1)
                RF_inputs.y = np.delete(RF_inputs.y,firstRow,firstColumn)
            else:
                pass
            regressor = RandomForestRegressor(n_estimators = RF_inputs.trees, random_state = defSplitLeaf) 
            #Train the model with training data and test it with test data  (80% train and 20% test)
            X_train, RF_outputs.X_test, y_train, RF_outputs.y_actual = train_test_split(RF_inputs.X, RF_inputs.y, test_size= RF_inputs.tst_siz, random_state=defSplit)
            # fit the regressor with x and y data 
            regressor.fit(X_train, y_train)   
            # test the output by changing values 
            RF_outputs.y_test = regressor.predict(RF_outputs.X_test)
            RF_outputs.y_test = np.ndarray.tolist(RF_outputs.y_test)
            RF_outputs.length = len(RF_outputs.y_test)
            #Formatting X_test
            RF_outputs.X_test = np.column_stack(RF_outputs.X_test)
            RF_outputs.X_test = np.ndarray.tolist(RF_outputs.X_test)
            #Mean squared error and accuracy
            RF_outputs.tst_mse = mean_squared_error(RF_outputs.y_actual, RF_outputs.y_test)
            RF_outputs.tst_accrc = maxAccuracy -  RF_outputs.tst_mse
            #RF_outputs.tst_accrc = maxAccuracy / 0
            return RF_outputs
    except:
        RF_outputs.flag = error
        RF_outputs.msg  = eUnexpected
        return RF_outputs
#End of Random forest function---------------------------------------------------------

# Function call
RF_outputs1 = RFreg(RF_inputs1)

if RF_outputs1.flag == error:
    print(RF_outputs1.msg)
else:
    #Printing outputs
    print('Predicted Output:       ', RF_outputs1.y_test)
    print('test input:             ', RF_outputs1.X_test)
    print('expected output:        ', RF_outputs1.y_actual)
    print('length of output array: ', RF_outputs1.length)
    print('Mean Square error:      ', RF_outputs1.tst_mse)
    print('Accuracy:               ', RF_outputs1.tst_accrc)