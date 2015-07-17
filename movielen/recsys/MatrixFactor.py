#coding=utf8

"""
This file implemented matrix factorization algorithm.
"""

import random

class MatrixFactor:
    usersVec = {}
    itemsVec = {}
    vecLen = 100
    iterNum = 1000
    alpha = 0.2
    trainData = None
    testData = None

    def __init__(self, trData, teData, usersNum, itemsNum, vecLen=100, itersNum=1000, alpha=0.2):
        self.trainData = trData
        self.testData = teData
        for uid in range(1, usersNum+1):
            uv = []
            for i in range(vecLen):
                uv.append(random.random())
            usersVec[uid] = uv
        for iid in range(1, itemsNum+1):
            iv = []
            for i in range(vecLen):
                iv.append(random.random())
            itemsVec[iid] = iv
        self.vecLen = vecLen
        self.iterNum = iterNum
        self.alpha = alpha




