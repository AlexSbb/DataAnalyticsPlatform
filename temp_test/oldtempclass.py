class OneDataSeries:
    name = 'name'
    dataSeries = []
    minValue =  0.0
    maxValue =  0.0
    tempValue = 0
    boolValue = True
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


@app.route('/getClass', methods=['GET'] )
def getClass():
    firstDataSeries = OneDataSeries()
    firstDataSeries.name = 'Series 1'
    firstDataSeries.maxValue = 10
    firstDataSeries.tempValue = 100
    firstDataSeries.dataSeries = list(np.random.rand(20))
    return firstDataSeries.toJSON()
