import pandas as pd
import numpy as np

import statistics as st
import scipy
from scipy.interpolate import griddata
from scipy import interpolate
from scipy.interpolate import interp1d
np.nan

Matrix = pd.read_csv("Y1.csv")
Matrix2 = Matrix.to_numpy()

def MaxMin(OriginalMatrix, MaxValue, MinValue):
    ReplaceMatrixIndex = []
    for index in range(len(OriginalMatrix)):
        if OriginalMatrix[index] > MaxValue or OriginalMatrix[index] < MinValue :
            ReplaceMatrixIndex.append(index)

    return ReplaceMatrixIndex

#print(Matrix)
#print(Matrix.describe())

ResMaxMin = MaxMin (Matrix2, 1.2353, -1.15)
print(ResMaxMin)


def StdDev(OriginalMatrix, StdDevFactor):
    ReplaceMatrixIndex = []
    StdDevNum = np.std(OriginalMatrix, axis=0)
    StdMeanNum = np.mean(OriginalMatrix, axis=0)
    ReplaceMatrixIndex = MaxMin(OriginalMatrix, StdMeanNum+(StdDevNum*StdDevFactor), StdMeanNum-(StdDevNum*StdDevFactor))
    return ReplaceMatrixIndex

#print(StdDev(Matrix2,1.5))

def Interpolation(OriginalMatrix,ReplaceMatrixIndex):
    InterpolatedMatrixIndex = np.zeros([len(ReplaceMatrixIndex), 3])
    #InterpolatedMatrix = []
    InterpolatedMatrix = OriginalMatrix
    for index in range(len(ReplaceMatrixIndex)):
        InterpolatedMatrixIndex [index][0] =  OriginalMatrix[ReplaceMatrixIndex[index]-1]
        InterpolatedMatrixIndex [index][1] = OriginalMatrix[ReplaceMatrixIndex[index]]
        InterpolatedMatrixIndex [index][2] = OriginalMatrix[ReplaceMatrixIndex[index] + 1]
        f = interpolate.interp1d([ReplaceMatrixIndex[index]-1, ReplaceMatrixIndex[index]+1], [InterpolatedMatrixIndex [index][0], InterpolatedMatrixIndex[index][2]],  kind = 'quadratic')
        #InterpolatedMatrix.append(f(ReplaceMatrixIndex[index]))
        InterpolatedMatrix [ReplaceMatrixIndex[index]] = f(ReplaceMatrixIndex[index])
        #print(InterpolatedMatrix)
    #InterpolatedMatrix = f(2)

    return InterpolatedMatrix

#TimeMatrixIndex = []
#YMatrixIndex = []
#IntMatrix = np.zeros([len(ResMaxMin), 3])
#IntMatrix [0][0] = Matrix2[ResMaxMin[0]-1]
#IntMatrix [0][1] = Matrix2[ResMaxMin[0]]
#IntMatrix [0][2] = Matrix2[ResMaxMin[0]+1]
#print(IntMatrix)

EndMatrix = Interpolation(Matrix2, ResMaxMin)
print(EndMatrix[44])
#print(interpolate.interp1d([1,2,3],IntMatrix))

#    for index in range(len(ResMaxMin)):
#        ResMaxMin[index]            ReplaceMatrixIndex.append(index)

#f = interpolate.interp1d([3, 4],[5, 6])
#print(f(4))

