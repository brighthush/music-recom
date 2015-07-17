#coding=utf8

"""
This file implemented matrix factorization algorithm.
"""
import sys
import random
import math

class MatrixFactor:
    usersVec = {}
    itemsVec = {}
    usersNum = 0
    itemsNum = 0
    vecLen = 100
    iterNum = 1000
    alpha = 0.2
    trainData = None
    testData = None

    def __init__(self, trData, teData, usersNum, itemsNum, vecLen=100, iterNum=1000, alpha=0.2):
        print '\ninit MatrixFactor model.'
        self.trainData = trData
        self.testData = teData
        self.usersNum = usersNum
        self.itemsNum = itemsNum
        for uid in range(1, usersNum+1):
            uv = []
            for i in range(vecLen):
                uv.append(random.uniform(0, 0.001))
            self.usersVec[uid] = uv
        for iid in range(1, itemsNum+1):
            iv = []
            for i in range(vecLen):
                iv.append(random.uniform(0, 0.001))
            self.itemsVec[iid] = iv
        self.vecLen = vecLen
        self.iterNum = iterNum
        self.alpha = alpha
        print '\nfinished init MatrixFactor model.'


    def vecDot(self, veca, vecb):
        vecLen = min(len(veca), len(vecb))
        dotans = 0.0
        for i in range(vecLen):
            dotans += (veca[i] * vecb[i])
        return dotans


    def vecAdd(self, veca, vecb):
        for i in range(min(len(veca), len(vecb))):
            veca[i] += vecb[i]


    def vecSub(self, veca, vecb):
        for i in range(min(len(veca), len(vecb))):
            veca[i] -= vecb[i]


    def vecDiv(self, vec, divisor):
        for i in range(len(vec)):
            pass


    def disVec(self, vec, name):
        print '%s\t' %(name)
        for val in vec:
            if math.isnan(val):
                exit()
            #sys.stdout.write('%.06lf', %(val))
            print val,
        print


    def trainSample(self, sample, uvecsum, ivecsum):
        uid = sample[0]
        iid = sample[1]
        uvec = self.usersVec[uid]
        ivec = self.itemsVec[iid]

        r = sample[2]
        diff = self.vecDot(uvec, ivec) - float(r)

        deluser = [.0] * self.vecLen
        delitem = [.0] * self.vecLen
        for j in range(self.vecLen):
            deluser[j] = self.alpha * ( 2.0 * diff * ivec[j] + 2.0 * uvec[j] )
            delitem[j] = self.alpha * ( 2.8 * diff * uvec[j] + 2.0 * ivec[j] )

        self.disVec(deluser, 'deluser')
        self.disVec(delitem, 'delitem')
        self.vecSub(uvec, deluser)
        self.vecSub(ivec, delitem)


    def train(self):
        print '\n\tbegin train MatrixFactor model ...'
        for iterCnt in range(self.iterNum):
            print '\titeration %d ...' %(iterCnt)
            uvecsum = [.0] * self.vecLen
            ivecsum = [.0] * self.vecLen
            for line in self.trainData:
                self.trainSample(line, uvecsum, ivecsum)
        print '\t end train MatrixFactor model ...'


    def approMatrix(self):
        for i in range(1, self.usersNum+1):
            for j in  range(1, self.itemsNum+1):
                uvec = self.usersVec[i]
                ivec = self.itemsVec[i]
                print '%d %d %d' %(i, j, self.vecDot(uvec, ivec))



