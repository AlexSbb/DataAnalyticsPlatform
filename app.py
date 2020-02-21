from flask import Flask, jsonify, request
from flask import render_template
import numpy as np
import pandas as pd
from flask_cors import CORS
import temp_test.read_csv_data as rcd
import json
import pycode.Team2Functions as T2F
from CustomClasses import DataObject, DataSeries

app = Flask(__name__)
CORS(app, resources=r'/*')

globalDataObject = None

@app.route('/')
def hello_world():  
    return render_template('index.html')

# Importing the data from the front end (receiving a json message 
# and reading it into a globalDataObject of type DataObject)
@app.route('/importDataFromFile', methods=['POST', 'GET'] )
def importDataFromFile():
    if request.method == 'GET':
        print ('GET')
        return jsonify(message = "GET") 
    else:
        # print(request.get_json())
        fileName = request.get_json()['fileName']
        dataArray = list(request.get_json()['dataArray']) 
        global globalDataObject
        if (globalDataObject is None):
            globalDataObject = DataObject(dataArray, fileName)
        else: 
            globalDataObject.addSeries(dataArray, fileName)       
        return jsonify(globalDataObject.toJSON()) 

# Sending the data object from the backend to the frontend
# Check if there is no data uploaded yet and returning a notification based on it
@app.route('/getGlobalDataObject', methods=['GET'] )
def getGlobalDataObject():
    if (globalDataObject is None):
        return jsonify(message = "Please upload a file with data series to start.") 
    else:
        return jsonify(globalDataObject.toJSON()) 

# Receiving input from the frontend to perform a specific function
# Depending on the action specified in the json, we can for example delete all data or
# send the parameters to perform the desired procedures as specified by the user in the GUI
# The return value is either an error message, which is then to be displayed to the user
# in the GUI, or the data object itself when the procedure was successful.
@app.route('/dataManipulation', methods=['POST'] )
def resetGlobalDataObject():
    action = request.get_json()['action']
    if (globalDataObject is None):
        return jsonify(message = "Please upload a file with data series to start.") 
    elif action == "deleteAll":
        globalDataObject.clearSeries()
    elif action == "deleteSeries":
        globalDataObject.deleteSeries(request.get_json()['seriesName'])
    elif action == "resetToOriginalData":
        globalDataObject.resetToOriginalData()
    elif action == "performSmoothing":
        window=int(request.get_json()['window'])
        seriesName= request.get_json()['seriesName']
        smoothingType = request.get_json()['smoothingType']
        globalDataObject.dataSeriesDict[seriesName].smoothing(smoothingType,window)    
    elif action == "performInterpolationHardLimits":
        # Interpolation with hard limits
        seriesName=request.get_json()['seriesName']
        selectedMin=float(request.get_json()['selectedMin'])
        selectedMax=float(request.get_json()['selectedMax'])
        interpolationType=int(request.get_json()['interpolationType']) 
        # 0 - Linear Interpolation
        # 1 - Quadratic Interpolation
        globalDataObject.dataSeriesDict[seriesName].selectedMax=selectedMax
        globalDataObject.dataSeriesDict[seriesName].selectedMin=selectedMin
        globalDataObject.dataSeriesDict[seriesName].interpolationType=interpolationType

        globalDataObject.dataSeriesDict[seriesName].maxMin()
        if (globalDataObject.dataSeriesDict[seriesName].error == ''):
            # if maxMin is OK, than calculate interpolation
            globalDataObject.dataSeriesDict[seriesName].interpolation()
        else:
            errorMsg=globalDataObject.dataSeriesDict[seriesName].error
            globalDataObject.dataSeriesDict[seriesName].resetError()
            return jsonify(message = errorMsg ) 
    elif action == "performInterpolationStdDev":
        # Interpolation with standart deviation
        seriesName = request.get_json()['seriesName']
        Std_factor = int(request.get_json()['Std_factor'])
        interpolationType=int(request.get_json()['interpolationType']) 
        # 0 - Linear Interpolation
        # 1 - Quadratic Interpolation      
        globalDataObject.dataSeriesDict[seriesName].stdDevFactor=Std_factor
        globalDataObject.dataSeriesDict[seriesName].interpolationType=interpolationType
        globalDataObject.dataSeriesDict[seriesName].standardDeviation()
        
        if (globalDataObject.dataSeriesDict[seriesName].error == ''):
            # if StDev is OK, than calculate interpolation
            globalDataObject.dataSeriesDict[seriesName].interpolation()
        else:
            errorMsg=globalDataObject.dataSeriesDict[seriesName].error
            globalDataObject.dataSeriesDict[seriesName].resetError()
            return jsonify(message = errorMsg ) 

    elif action == "performNNCalculations":
        # Neural Network     
        print("Neural Network")  
        try:      
            inputSeriesNameArray = list(request.get_json()['inputSeries'])
            seriesName          = request.get_json()['seriesName']
            testSize            = float(request.get_json()['testSize'])
            activeFunction      = request.get_json()['activeFunction']
            solverFunction      = request.get_json()['solverFunction']
            hiddenLayers        = list(request.get_json()['hiddenLayers'])
            hiddenLayers        = list(map(int, hiddenLayers))
            print(hiddenLayers)
            iterations          = int(request.get_json()['iterations'])
            scalingOnOff        = bool(request.get_json()['scalingOnOff'])
        except: 
            return jsonify(message = 'Wrong input' ) 

        inputSeriesData =[]
        for name in inputSeriesNameArray:
            inputSeriesData.append(globalDataObject.dataSeriesDict[name].currentData)
        globalDataObject.dataSeriesDict[seriesName].neuralNetwork(inputSeriesData,testSize,activeFunction,hiddenLayers,solverFunction,iterations,scalingOnOff)

    elif action == "performRFCalculations":
        # Random Forest      
        print("performRFCalculations")
        try:
            seriesName              = request.get_json()['seriesName'] 
            inputSeriesNameArray    = list(request.get_json()['inputSeries'])
            trees                   = int(request.get_json()['trees'])
            testSize                = float(request.get_json()['testSize'])
            historyOnOff            = bool(request.get_json()['historyOnOff'])
        except:
            return jsonify(message = 'Wrong input' ) 
        inputSeriesData =[]
        for name in inputSeriesNameArray:
            inputSeriesData.append(globalDataObject.dataSeriesDict[name].currentData)
        globalDataObject.dataSeriesDict[seriesName].randonForest(inputSeriesData,trees,testSize,historyOnOff)  
    
    if 'seriesName' in locals():
        if (globalDataObject.dataSeriesDict[seriesName].error == ''):
            return  jsonify(globalDataObject.toJSON()) 
        else:
            errorMsg=globalDataObject.dataSeriesDict[seriesName].error
            globalDataObject.dataSeriesDict[seriesName].resetError()
            return jsonify(message = errorMsg)  
    else:
        return  jsonify(globalDataObject.toJSON())



if __name__ == '__main__':
    app.run(debug=True)
