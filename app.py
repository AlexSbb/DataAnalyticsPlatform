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


if __name__ == '__main__':
    app.run(debug=True)
