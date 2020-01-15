import numpy as np
from scipy import interpolate

def MaxMin(OriginalMatrix, MaxValue, MinValue):
    ReplaceMatrixIndex = []
    for index in range(len(OriginalMatrix)):
        if OriginalMatrix[index] > MaxValue or OriginalMatrix[index] < MinValue :
            ReplaceMatrixIndex.append(index)

    return ReplaceMatrixIndex


def StdDev(OriginalMatrix, StdDevFactor):
    ReplaceMatrixIndex = []
    StdDevNum = np.std(OriginalMatrix, axis=0)
    StdMeanNum = np.mean(OriginalMatrix, axis=0)
    ReplaceMatrixIndex = MaxMin(OriginalMatrix, StdMeanNum+(StdDevNum*StdDevFactor), StdMeanNum-(StdDevNum*StdDevFactor))
    return ReplaceMatrixIndex


def Interpolation(OriginalMatrix,ReplaceMatrixIndex):
    InterpolatedMatrixIndex = np.zeros([len(ReplaceMatrixIndex), 3])
    InterpolatedMatrix = OriginalMatrix
    for index in range(len(ReplaceMatrixIndex)):
        InterpolatedMatrixIndex [index][0] =  OriginalMatrix[ReplaceMatrixIndex[index]-1]
        InterpolatedMatrixIndex [index][1] = OriginalMatrix[ReplaceMatrixIndex[index]]
        InterpolatedMatrixIndex [index][2] = OriginalMatrix[ReplaceMatrixIndex[index] + 1]
        f = interpolate.interp1d([ReplaceMatrixIndex[index]-1, ReplaceMatrixIndex[index]+1], [InterpolatedMatrixIndex [index][0], InterpolatedMatrixIndex[index][2]],  kind = 'linear')
        InterpolatedMatrix [ReplaceMatrixIndex[index]] = f(ReplaceMatrixIndex[index])

    return InterpolatedMatrix
