import numpy as np 
import pandas as pd
import NeuralNetworkFn as NN
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

actv1 = ("identity", "logistic", "tanh", "relu")
slvr1 = ("lbfgs", "sgd", "adam")
hid_lyrs1=(8,4,5)
hid_lyrs2=(8,4,5,1001,10,1,1,1,1,1)
hid_lyrs3=(8,4,5,100,10,1,1,1,1,1,1)

NN_inputs1 = NN.NN_inputs(X1,y1,0.2,actv1[3],hid_lyrs1,slvr1[1],200,True)
NN_inputs2 = NN.NN_inputs(X2,y2,0.2,actv1[3],hid_lyrs1,slvr1[1],200,False)

NN_inputs3 = NN.NN_inputs(X2,y1,0.2,actv1[3],hid_lyrs1,slvr1[1],200,True)
NN_inputs4 = NN.NN_inputs(X1,y2,0.2,actv1[3],hid_lyrs1,slvr1[1],200,True)
#neuron count
NN_inputs5 = NN.NN_inputs(X1,y1,0.2,actv1[3],hid_lyrs2,slvr1[1],200,True)
#test size
NN_inputs6 = NN.NN_inputs(X1,y1,0.95,actv1[3],hid_lyrs1,slvr1[1],200,True)
#no of iterations
NN_inputs7 = NN.NN_inputs(X1,y1,0.2,actv1[3],hid_lyrs1,slvr1[1],2001,True)
#no of hidden layers
NN_inputs8 = NN.NN_inputs(X1,y1,0.2,actv1[3],hid_lyrs3,slvr1[1],200,True)

#Positive cases----------------------------------------------------------

#Normal inputs should not produce error
# Function call
print('\nNormal inputs should not produce error')
NN_outputs1 = NN.NeuralNet(NN_inputs1)
if NN_outputs1.flag == NN.success:
    print('Case1 Run1: Pass')
else:
    print('Case1 Run1: Fail')

NN_outputs1 = NN.NeuralNet(NN_inputs2)
if NN_outputs1.flag == NN.success:
    print('Case1 Run2: Pass \n')
else:
    print('Case1 Run2: Fail \n')
    
#Negative cases----------------------------------------------------------

#Test input and output sizes
print('Test input and output sizes')
NN_outputs1 = NN.NeuralNet(NN_inputs3)
if NN_outputs1.flag == NN.error and NN_outputs1.msg == NN.eIoSize:
    print('Case2 Run1: Pass')
else:
    print('Case2 Run1: Fail')

NN_outputs1 = NN.NeuralNet(NN_inputs4)
if NN_outputs1.flag == NN.error and NN_outputs1.msg == NN.eIoSize:
    print('Case2 Run2: Pass \n')
else:
    print('Case2 Run2: Fail \n')

#Test illegal no of neuron count error
print('Test illegal no of neuron count error')
NN_outputs1 = NN.NeuralNet(NN_inputs5)
if NN_outputs1.flag == NN.error and NN_outputs1.msg == NN.eNeuronCount:
    print('Case6 Run1: Pass \n')
else:
    print('Case6 Run1: Fail \n')

#Test testsize error
print('Test testsize error')
NN_outputs1 = NN.NeuralNet(NN_inputs6)
if NN_outputs1.flag == NN.error and NN_outputs1.msg == NN.eTestSize:
    print('Case3 Run1: Pass \n')
else:
    print('Case3 Run1: Fail \n')

#Test illegal no of iterations error
print('Test illegal no of iterations error')
NN_outputs1 = NN.NeuralNet(NN_inputs7)
if NN_outputs1.flag == NN.error and NN_outputs1.msg == NN.eIterCount:
    print('Case4 Run1: Pass \n')
else:
    print('Case4 Run1: Fail \n')

#Test illegal no of hidden layers error
print('Test illegal no of hidden layers error')
NN_outputs1 = NN.NeuralNet(NN_inputs8)
if NN_outputs1.flag == NN.error and NN_outputs1.msg == NN.eNoOfHiddLyr:
    print('Case5 Run1: Pass \n')
else:
    print('Case5 Run1: Fail \n')




