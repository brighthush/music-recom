#coding=utf8
"""
This file is the Main file, which calls all the other modules.
"""

import MovieLen as ml
import MatrixFactor as mf

def main():
    movielen = ml.MovieLen('debug.txt')
    trainData, testData = movielen.buildData()
    usersNum = movielen.getUsersNum()
    itemsNum = movielen.getItemsNum()

    matrixfa = mf.MatrixFactor(trainData, testData, usersNum, itemsNum, vecLen=2)
    matrixfa.train()
    matrixfa.approMatrix()


if __name__ == '__main__':
    main()

