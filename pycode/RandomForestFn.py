import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

X = [   [4.5,6.7],
        [8.9,3.8],
        [9,6.8],
        [12.3,8.8] ]

# output dataset            
y = [8.55055,5.53195,9.1547,11.91745]

# Fitting Random Forest Regression to the dataset 
# import the regressor 

def RFreg(est,tst_siz):
    from sklearn.ensemble import RandomForestRegressor 
    #regressor = RandomForestRegressor(n_estimators = 100, random_state = 0) 
    regressor = RandomForestRegressor(n_estimators = est, random_state = 42) 
    #Train the model with training data and test it with test data  (80% train and 20% test)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= tst_siz, random_state=40)
    # fit the regressor with x and y data 
    regressor.fit(X_train, y_train)   
    # test the output by changing values 
    y_pred = regressor.predict(X_test)  
    return y_pred, X_test

y_new, x_new = RFreg(1000,0.2)
print(x_new)
print(y_new)