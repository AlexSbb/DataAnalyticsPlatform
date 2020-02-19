import numpy as np 
#import matplotlib.pyplot as plt 
import pandas as pd 
from typing import NamedTuple

#Error codes
eIoSize         = "Input and output array size does not match"
eNoOfHiddLyr    = "Number of hidden layers should be within 1 and 10"
eNeuronCount    = "Number of Neurons should is in range 1 to 1000"
eIterCount      = "Number of Iteration should be in range 1 to 2000"
eTestSize       = "Test size should be in range 0.1 to 0.9"
eNoOfTrees      = "Number of trees should be within 1000"

# Input structure for Neural Network
class RF_inputs(NamedTuple):
    X: float
    y: float
    trees: int
    tst_siz: float
   
# Output structure for Neural Network
class RF_outputs(NamedTuple):
    y_test: float
    X_test: float 
    y_actual: float
    length: int
    tst_mse: float
    tst_accrc: float

# input dataset 
X1 = [   [4.5,6.7],
        [8.9,3.8],
        [9,6.8],
        [12.3,8.8] ]

# output dataset            
y1 = [8.55055,5.53195,9.1547,11.91745]

# Input initialization
RF_inputs1 = RF_inputs(X1,y1,1000,0.2)

# Random Forest regressor function 
def RFreg(RF_inputs):
    from sklearn.ensemble import RandomForestRegressor 
    #regressor = RandomForestRegressor(n_estimators = 100, random_state = 0) 
    regressor = RandomForestRegressor(n_estimators = RF_inputs.trees, random_state = 42) 
    #Train the model with training data and test it with test data  (80% train and 20% test)
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    X_train, RF_outputs.X_test, y_train, RF_outputs.y_actual = train_test_split(RF_inputs.X, RF_inputs.y, test_size= RF_inputs.tst_siz, random_state=40)
    # fit the regressor with x and y data 
    regressor.fit(X_train, y_train)   
    # test the output by changing values 
    RF_outputs.y_test = regressor.predict(RF_outputs.X_test)
    RF_outputs.length = len(RF_outputs.X_test)
    RF_outputs.tst_mse = mean_squared_error(RF_outputs.y_actual, RF_outputs.y_test)
    RF_outputs.tst_accrc = 100.0 -  RF_outputs.tst_mse
    return RF_outputs

# Function call
RF_outputs1 = RFreg(RF_inputs1)

#Printing outputs
print('Predicted Output:       ', RF_outputs1.y_test)
print('test input:             ', RF_outputs1.X_test)
print('expected output:        ', RF_outputs1.y_actual)
print('length of output array: ', RF_outputs1.length)
print('Mean Square error:      ', RF_outputs1.tst_mse)
print('Accuracy:               ', RF_outputs1.tst_accrc)