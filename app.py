from flask import Flask, jsonify, request
from flask import render_template
import numpy as np
import pandas as pd
from flask_cors import CORS
import temp_test.read_csv_data as rcd
import json
import pycode.Team2Functions as T2F
app = Flask(__name__)
CORS(app, resources=r'/*')



def randomData():
    d = {'index': np.arange(20), 'value': np.random.rand(20)}
    return d

RandomDataArr= {}
for x in range(2):
    RandomDataArr['data_'+ str(x)]=pd.DataFrame(randomData()).to_json(orient='records')



@app.route('/')
def hello_world():  
    return render_template('index.html')




@app.route('/data', methods=['POST', 'GET'] )
def data():
    if request.method == 'GET':
        
        
        #  df1 = pd.DataFrame(np.random.randn(6, 2)*10, columns=list('xy'))
        #  df2 = pd.DataFrame(np.random.randn(6, 2), columns=list('xy'))
        df3 = pd.DataFrame(randomData())
        jf3=df3.to_json(orient='records')
        
        RandomDataArr= {}
        for x in range(2):
            RandomDataArr['data_'+ str(x)]=pd.DataFrame(randomData()).to_json(orient='records')


        return jsonify(RandomDataArr)
        # return jsonify( data1=df3.to_json(orient='records'), data2=rcd.ImportData().to_json(orient='records'))



    else:
        print(request.get_json())
        print(request.get_json()['username'])
        return jsonify(response_value_1=1,response_value_2="value")



@app.route('/interpolation', methods=['POST', 'GET'] )
def interpolation():
    if request.method == 'GET':
        print ('GET')
        return jsonify(message = "GET") 
    else:
        print(request.get_json())
        varmin = float(request.get_json()['MIN'])
        varmax = float(request.get_json()['MAX'])
        print(varmin,varmax)
        return jsonify(message = "OK") 



if __name__ == '__main__':
    app.run(debug=True)
