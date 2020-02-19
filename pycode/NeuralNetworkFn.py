import pandas as pd
import numpy as np

from typing import NamedTuple

#Error codes
eIoSize         = "Input and output array size does not match"
eNoOfHiddLyr    = "Number of hidden layers should be within 1 and 10"
eNeuronCount    = "Number of Neurons should is in range 1 to 1000"
eIterCount      = "Number of Iteration should be in range 1 to 2000"
eTestSize       = "Test size should be in range 0.1 to 0.9"
eNoOfTrees      = "Number of trees should be within 1000"


# Neural Net paramenters selected by user should remain in the following range:
actv1 = ("identity", "logistic", "tanh", "relu")
slvr1 = ("lbfgs", "sgd", "adam")

#Tuple of hidden layers in Neural Networks
hid_lyrs1 = (8,4,4)

# Input structure for Neural Network
class NN_inputs(NamedTuple):
    X:          float
    y:          float
    tst_siz:    float
    actv:       tuple
    hid_lyrs:   tuple
    slvr:       tuple
    itr:        int
    sclng:      bool #scaling

# Output structure for Neural Network
class NN_outputs(NamedTuple):
    y_test:     float # resulting output
    X_test:     float # test input
    y_actual:   float # expected output
    length:     int   # length of y_test
    tst_mse:    float # mean square error
    tst_accrc:  float # accuracy

# Input array (In final implementation there should be a choice to select between processed input and raw input)
X1 = [   [4.5,6.7],
         [8.9,3.8],
         [9,6.8],
         [12.3,8.8] ]

# output dataset (raw or processed selection)           
y1 = [8.55055,5.53195,9.1547,11.91745]

# Input initialization
NN_inputs1 = NN_inputs(X1,y1,0.2,actv1[3],hid_lyrs1,slvr1[1],200,False)     # Activation=relu, solver=sgd

# Neural Network function definition:
def NeuralNet(NN_inputs):
    from sklearn.preprocessing import StandardScaler
    from sklearn.neural_network import MLPRegressor
    if NN_inputs.sclng == True:
        sc = StandardScaler()
        NN_inputs.X = sc.fit_transform(NN_inputs.X)
    else:
        pass
    print(NN_inputs.X)
    print(NN_inputs.y)
    #Train the model with training data and test it with test data  (80% train and 20% test)
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    X_train, NN_outputs.X_test, y_train, NN_outputs.y_actual = train_test_split(NN_inputs.X, NN_inputs.y, test_size= NN_inputs.tst_siz, random_state=40)
    #Neural network model
    reg = MLPRegressor(hidden_layer_sizes = NN_inputs.hid_lyrs, activation = NN_inputs.actv, solver = NN_inputs.slvr, learning_rate = 'adaptive', max_iter = NN_inputs.itr, random_state = 1)
    reg.fit(X_train,y_train)
    #Prediction of the unseen test data
    NN_outputs.y_test = reg.predict(NN_outputs.X_test)
    # return pred, X_test
    #pred = reg.predict([[1.30789956, 1.27638396]])
    NN_outputs.length = len(NN_outputs.X_test)
    NN_outputs.tst_mse = mean_squared_error(NN_outputs.y_actual, NN_outputs.y_test)
    NN_outputs.tst_accrc = 100 - NN_outputs.tst_mse
    return NN_outputs


# Function call
NN_outputs1 = NeuralNet(NN_inputs1)

#Printing outputs
print('Predicted Output:       ', NN_outputs1.y_test)
print('test input:             ', NN_outputs1.X_test)
print('expected output:        ', NN_outputs1.y_actual)
print('length of output array: ', NN_outputs1.length)
print('Mean Square error:      ', NN_outputs1.tst_mse)
print('Accuracy:               ', NN_outputs1.tst_accrc)