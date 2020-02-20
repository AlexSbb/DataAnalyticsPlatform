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

@app.route('/getGlobalDataObject', methods=['GET'] )
def getGlobalDataObject():
    if (globalDataObject is None):
        return jsonify(message = "Empty") 
    else:
        return jsonify(globalDataObject.toJSON()) 

@app.route('/dataManipulation', methods=['POST'] )
def resetGlobalDataObject():
    action = request.get_json()['action']
    if (globalDataObject is None):
        return jsonify(message = "Empty") 
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
    elif action == "performInterpolation_Limit":
        # Interpolation with hard limits, done!
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
    elif action == "performInterpolation_StandardDev":
        # Interpolation with standart deviation
        print("not working")
        globalDataObject(request.get_json()['seriesName']).standardDeviation(request.get_json()['Std_factor'])
    elif action == "performNNCalculations":
        # Neural Network     
        print("Neural Network")  
        try:      
            inputSeriesNameArray = request.get_json()['inputSeries']
            seriesName          = request.get_json()['outputSeries']
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

        inputSeriesName = inputSeriesNameArray[0]
        inputSeriesData = globalDataObject.dataSeriesDict[inputSeriesName].currentData
        globalDataObject.dataSeriesDict[seriesName].neuralNetwork(inputSeriesData,testSize,activeFunction,hiddenLayers,solverFunction,iterations,scalingOnOff)

    elif action == "performRFCalculations":
        # Random Forest      
        print("performRFCalculations")
        seriesName              = request.get_json()['outputSeries'] 
        inputSeriesNameArray    = request.get_json()['inputSeries']
        trees                   = int(request.get_json()['trees'])
        testSize                = float(request.get_json()['testSize'])
        historyOnOff            = bool(request.get_json()['historyOnOff'])
        
        inputSeriesName = inputSeriesNameArray[0]
        inputSeries = globalDataObject.dataSeriesDict[inputSeriesName].currentData
        globalDataObject.dataSeriesDict[seriesName].randonForest(inputSeries,trees,testSize,historyOnOff)


    
    if (globalDataObject.dataSeriesDict[seriesName].error == ''):
        return  jsonify(globalDataObject.toJSON()) 
    else:
        errorMsg=globalDataObject.dataSeriesDict[seriesName].error
        globalDataObject.dataSeriesDict[seriesName].resetError()
        return jsonify(message = errorMsg) 

@app.route('/interpolation', methods=['POST'] )
def interpolation():
    seriesName= request.get_json()['seriesName']      
    limit_or_dev=bool(request.get_json()['limit_or_dev'])
    selectedMin=float(request.get_json()['selectedMin'])
    selectedMax=float(request.get_json()['selectedMax'])
    stdDevFactor=int(request.get_json()['stdDevFactor'])
    interpolationType=bool(request.get_json()['interpolationType'])
    if  limit_or_dev:
        # Calculate hard limit
        globalDataObject.dataSeriesDict[seriesName].maxMin(selectedMax,selectedMin)
        print ('replaceArray=',  globalDataObject.dataSeriesDict[seriesName].replaceArray)
    else:
        # Calculate standart deviation
        globalDataObject.dataSeriesDict[seriesName].stdDev(stdDevFactor)
        print ('replaceArray=',  globalDataObject.dataSeriesDict[seriesName].replaceArray)
    
    if (globalDataObject.dataSeriesDict[seriesName].error == ''):
        return  jsonify(globalDataObject.dataSeriesDict[seriesName].toJSON())
    else:
        errorMsg=globalDataObject.dataSeriesDict[seriesName].error
        globalDataObject.dataSeriesDict[seriesName].resetError()
        return jsonify(message = errorMsg ) 


if __name__ == '__main__':
    app.run(debug=True)
