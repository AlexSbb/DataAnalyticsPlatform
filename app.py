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
        print(fileName)
        print(dataArray)  
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
    elif action == "performInterpolationHardLimits":
        globalDataObject(request.get_json()['seriesName']).interpolation(request.get_json()['Intrp_Max'], request.get_json()['Intrp_Min'])
    elif action == "performInterpolationStdDev":
        globalDataObject(request.get_json()['seriesName']).standardDeviation(request.get_json()['Std_factor'])
    elif action == "performNNCalculations":
        print()
     #   NN.NeuralNet(NN.NN_inputs(changeDataSeriesForm([inputSeries1.originalData, inputSeries2.originalData]), outputSeries.originalData, 0.5, actv1[3], hid_lyrs1, slvr1[1], 200, False))
       # globalDataObject(request.get_json()['seriesName']).standardDeviation(request.get_json()['Std_factor'])
       # globalDataObject(request.get_json()['seriesName']).standardDeviation(request.get_json()['Std_factor'])
    elif action == "performRFCalculations":
        print()
      #  globalDataObject(request.get_json()['seriesName']).standardDeviation(request.get_json()['Std_factor'])
    
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
