import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from typing import NamedTuple

#DEFINITIONS-------------------------------------------------------------------------------------------------
#Error codes
eInputOutputSize         = "Input and output array size does not match"
eNoOfHiddLyr             = "Number of hidden layers should be within 1 and 10"
eNeuronCount             = "Number of Neurons should be in range 1 to 1000"
eIterationCount          = "Number of Iteration should be in range 1 to 2000"
eTestSize                = "Test size should be in range 0.1 to 0.9"
eNoOfTrees               = "Number of trees should be within 1000"
eUnexpected              = "Internal Error"
eInvalidActivation       = "Invalid Activation function selection"
eInvalidSolver           = "Invalid Solver function selection"
#Waring code
wAccuracy                = "Selected data is not appropriate to predict data"

#Flags
error   = "error"
success = "success"
warning = "Warning" 

#Constants
minTest_size          = 0.1
maxTest_size          = 0.9
maxIteration          = 2000
minIteration          = 0
maxNeurons            = 1000
hidden_layerslen      = 10
maxAccuracy           = 100
defSplit              = 40
defSplitLeaf          = 1
recommendedAccuracy   = 70

# Neural Net paramenters selected by user should remain in the following range:
activation_fun1 = ("identity", "logistic", "tanh", "relu")
solver_fun1 = ("lbfgs", "sgd", "adam")

#Tuple of hidden layers in Neural Networks
hidden_layers1 = (8,4,5)

# Input structure for Neural Network
class NN_inputs(NamedTuple):
    X:                      float  # input
    y:                      float  # output
    test_size:              float  # test size
    activation_fun:         tuple  # activation function
    hidden_layers:          tuple  # size of hidden layer and number of neurons in each layer
    solver_fun:             tuple  # solver function
    iterations:             int    # number of iterations
    scaling:                bool   # scaling

# Output structure for Neural Network
class NN_outputs(NamedTuple):
    flag:                       str   # flag check
    y_test:                     float # resulting output
    X_test:                     float # test input
    y_actual:                   float # expected output
    length:                     int   # length of y_test
    test_mean_squared_error:    float # mean square error
    test_accuracy:              float # accuracy
    message:                    str   # string
#END OF DEFINITIONS------------------------------------------------------------------------------------------


 
#IMPORTING DATA----------------------------------------------------------------------------------------------
# Input array (In final implementation there should be a choice to select between processed 
# input and raw input)
# X1 = [   [4.5,6.7],
#          [8.9,3.8],
#          [9,6.8],
#          [12.3,8.8] ]

# output dataset (raw or processed selection)           
# y1 = [8.55055,5.53195,9.1547,11.91745]
#END OF IMPORTING DATA---------------------------------------------------------------------------------------

# Input initialization
# NN_inputs1 = NN_inputs(X1,y1,0.2,activation_fun1[3],hidden_layers1,solver_fun1[1],200,False)     
# Activation=relu, solver=sgd

# Neural Network function definition-------------------------------------------------------------------------
def NeuralNet(NN_inputs):
    try:
        #Error check
        # check for number of neurons in each layer    
            for i in range(len(NN_inputs.hidden_layers)):          
                if NN_inputs.hidden_layers[i] > maxNeurons:
                   NN_outputs.flag = error
                   NN_outputs.message = eNeuronCount
                   return NN_outputs
                else:
                    # Check if Activation function entry is valid
                    for i in range(len(activation_fun1)): 
                        if NN_inputs.activation_fun == activation_fun1[i]:
                            break
                        elif i == len(activation_fun1)-1:
                            NN_outputs.flag = error
                            NN_outputs.message = eInvalidActivation
                            return NN_outputs
                        else:
                            # Check if Activation function entry is valid
                            for i in range(len(solver_fun1)): 
                                if NN_inputs.solver_fun == solver_fun1[i]:
                                    break
                                elif i == len(solver_fun1)-1:
                                    NN_outputs.flag = error
                                    NN_outputs.message = eInvalidSolver
                                    return NN_outputs
                                else:
                                    pass
                                
            # check for number of iterations
            if  NN_inputs.iterations > maxIteration or NN_inputs.iterations < minIteration:                   
                NN_outputs.flag = error
                NN_outputs.message = eIterationCount 
              
            # check for test size
            elif NN_inputs.test_size < minTest_size or NN_inputs.test_size > maxTest_size:                    
                 NN_outputs.flag = error
                 NN_outputs.message = eTestSize
             
            # check for number of hidden layers
            elif len(NN_inputs.hidden_layers) > hidden_layerslen:  
                 NN_outputs.flag = error
                 NN_outputs.message = eNoOfHiddLyr

            # check size of input and output    
            elif len(NN_inputs.X)!= len(NN_inputs.y):              
                 NN_outputs.flag = error
                 NN_outputs.message  = eInputOutputSize
              
            else:     
                if NN_inputs.scaling == True:
                   sc = StandardScaler()
                   nnX1 = sc.fit_transform(NN_inputs.X)
                else:
                    nnX1 = NN_inputs.X
                #Train the model with training data and test it with test data  (80% train and 20% test)
                X_train, NN_outputs.X_test, y_train, NN_outputs.y_actual = train_test_split(nnX1, 
                NN_inputs.y, test_size= NN_inputs.test_size, random_state=defSplitLeaf)
                #Neural network model
                reg = MLPRegressor(hidden_layer_sizes = NN_inputs.hidden_layers, 
                activation = NN_inputs.activation_fun, solver = NN_inputs.solver_fun, 
                learning_rate = 'adaptive', max_iter = NN_inputs.iterations, random_state = defSplit)
                reg.fit(X_train,y_train)
                #Prediction of the unseen test data
                NN_outputs.y_test = reg.predict(NN_outputs.X_test)
                NN_outputs.y_test = np.ndarray.tolist(NN_outputs.y_test)
                NN_outputs.length = len(NN_outputs.y_test)
                #Formatting X_test
                NN_outputs.X_test = np.column_stack(NN_outputs.X_test)
                NN_outputs.X_test = np.ndarray.tolist(NN_outputs.X_test)
                #Mean squared error and accuracy
                NN_outputs.test_mean_squared_error = mean_squared_error(NN_outputs.y_actual, 
                NN_outputs.y_test)
                NN_outputs.test_accuracy = maxAccuracy - NN_outputs.test_mean_squared_error
                if NN_outputs.test_accuracy < recommendedAccuracy:
                    NN_outputs.flag = warning
                    NN_outputs.message  = wAccuracy
                else:
                    NN_outputs.flag = success
                  
    except:
            NN_outputs.flag = error
            NN_outputs.message  = eUnexpected
            
    finally:
             return NN_outputs
# END of Neural Network function definition------------------------------------------------------------------

# # Function call
# NN_outputs1 = NeuralNet(NN_inputs1)

# # Output result
# if NN_outputs1.flag==error:
#     print(NN_outputs1.message)
# else:
#     #Printing outputs
#     print('flag:                   ', NN_outputs1.flag)
#     print('Predicted Output:       ', NN_outputs1.y_test)
#     print('test input:             ', NN_outputs1.X_test)
#     print('expected output:        ', NN_outputs1.y_actual)
#     print('length of output array: ', NN_outputs1.length)
#     print('Mean Square error:      ', NN_outputs1.test_mean_squared_error)
#     print('Accuracy:               ', NN_outputs1.test_accuracy)
#     if NN_outputs1.flag == warning:
#         print(NN_outputs1.message)

    