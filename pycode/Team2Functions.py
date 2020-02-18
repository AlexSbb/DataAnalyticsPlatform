import numpy as np
import csv
# dataSeries = []
#
# with open('y_data_test.csv', 'wb') as csvDataFile:
#     csvReader = csv.reader(csvDataFile)
#     for row in csvReader:
#         dataSeries.append(float(row[0]))
#
#
# print(dataSeries)
#
# # dataSeries = [98.6281, 98.6456, 98.6379, 98.6207, 98.6141, 98.6202, 98.5742, 98.5871, 98.5823, 98.5917, 98.5853, 98.6433, 98.6381, 98.6689, 98.6948, 98.7285, 98.7569, 98.7972, 98.8188, 98.7958, 98.7706, 98.7184, 98.6851, 98.7166, 98.714]
# # print(len(dataSeries))



def MaxMin(OriginalMatrix, MaxValue, MinValue):
    ReplaceMatrixIndex = []
    for index in range(len(OriginalMatrix)):
        if OriginalMatrix[index] > MaxValue or OriginalMatrix[index] < MinValue:
            ReplaceMatrixIndex.append(index)

    return len(ReplaceMatrixIndex) * 100 / len(OriginalMatrix), ReplaceMatrixIndex

#
# ResMaxMin = MaxMin (dataSeries, 98.818, 98.58)
# print(ResMaxMin)


def StdDev(OriginalMatrix, StdDevFactor):
    StdDevNum = np.std(OriginalMatrix, axis=0)
    print(StdDevNum)
    StdMeanNum = np.mean(OriginalMatrix, axis=0)
    print(StdMeanNum)
    ReplaceMatrixIndex = MaxMin(OriginalMatrix, StdMeanNum+(StdDevNum*StdDevFactor), StdMeanNum-(StdDevNum*StdDevFactor))
    return ReplaceMatrixIndex

#
# print(StdDev(dataSeries, 1.35))
