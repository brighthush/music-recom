#coding=utf8
"""
This file is the Main file, which calls all the other modules.
"""

import MovieLen as ml
import MatrixFactor as mf

def main():
    #movielen = ml.MovieLen('debug.txt')
    movielen = ml.MovieLen()
    trainData, testData = movielen.buildData()
    usersNum = movielen.getUsersNum()
    itemsNum = movielen.getItemsNum()

    matrixfa = mf.MatrixFactor(trainData, testData, usersNum, itemsNum, alpha=.002, vecLen=100, iterNum=300)
    matrixfa.train()
    #matrixfa.approMatrix()
    #matrixfa.testError()


if __name__ == '__main__':
    main()

