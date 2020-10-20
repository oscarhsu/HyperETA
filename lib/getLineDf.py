import numpy
from pandas import DataFrame

def getLineDf(trajTrain):
  trajNoArr = numpy.unique(trajTrain[5])
  trajTrain2 = []
  for aTrajNo in trajNoArr:
      OneTrajTrain = trajTrain.loc[trajTrain[5]==aTrajNo,]
      if OneTrajTrain.size <= 0 or OneTrajTrain.shape[0] <= 1:
          continue
      nCubes = OneTrajTrain.shape[0]
      j=0
      for indCube in range(nCubes-1):
          oneCube = OneTrajTrain.iloc[indCube,]
          secondCube = OneTrajTrain.iloc[indCube+1,]
          listNewLine = [
              None,
              j,
              None,
              None,
              None,
              oneCube[5],
              oneCube[0],
              secondCube[0],
              getDegree(oneCube,secondCube),
              oneCube[2],
              secondCube[2],
              oneCube[3],
              oneCube[4],
              secondCube[3],
              secondCube[4] ]
          trajTrain2.append(listNewLine)
          j += 1
  trajTrain2 = DataFrame(trajTrain2,columns=list(range(15)))
  return trajTrain2
