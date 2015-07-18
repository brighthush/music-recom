#coding=utf8

"""
This file implemented matrix factorization algorithm.
"""
import sys
import random
import math
from Heap import Heap

class MatrixFactor:
    usersVec = {}
    itemsVec = {}
    usersNum = 0
    itemsNum = 0
    vecLen = 100
    iterNum = 1000
    alpha = 0.2
    lam = 0.02
    trainData = None
    testData = None
    visitedItems = {}

    def __init__(self, trData, teData, usersNum, itemsNum, vecLen=100, iterNum=1000, alpha=0.2):
        print '\ninit MatrixFactor model.'
        self.trainData = trData
        self.testData = teData
        self.usersNum = usersNum
        self.itemsNum = itemsNum
        for uid in range(1, usersNum+1):
            uv = []
            for i in range(vecLen):
                uv.append(random.uniform(0, 0.5))
            self.usersVec[uid] = uv
        for iid in range(1, itemsNum+1):
            iv = []
            for i in range(vecLen):
                iv.append(random.uniform(0, 0.5))
            self.itemsVec[iid] = iv
        self.vecLen = vecLen
        self.iterNum = iterNum
        self.alpha = alpha
        for line in self.trainData:
            uid = line[0]
            iid = line[1]
            if uid not in self.visitedItems:
                self.visitedItems[uid] = set()
            self.visitedItems[uid].add(iid)
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


    def vecSquare(self, vec):
        squ = .0
        for dim in vec:
            squ += (dim * dim)
        return squ


    def disVec(self, vec, name):
        print '\t%s\t' %(name),
        for val in vec:
            if math.isnan(val):
                exit()
            #sys.stdout.write('%.06lf', %(val))
            print val,
        print


    def trainSample(self, sample, uvecsum, ivecsum):
        uid = sample[0]
        iid = sample[1]
        #print 'user %d, item %d, r %f' %(uid, iid, sample[2])
        uvec = self.usersVec[uid]
        ivec = self.itemsVec[iid]

        r = sample[2]
        diff = self.vecDot(uvec, ivec) - float(r)

        deluser = [.0] * self.vecLen
        delitem = [.0] * self.vecLen
        for j in range(self.vecLen):
            deluser[j] = self.alpha * ( 2.0 * diff * ivec[j] + 2.0 * self.lam * uvec[j] )
            delitem[j] = self.alpha * ( 2.8 * diff * uvec[j] + 2.0 * self.lam * ivec[j] )

        #self.disVec(deluser, 'deluser')
        #self.disVec(delitem, 'delitem')
        self.vecSub(uvec, deluser)
        self.vecSub(ivec, delitem)
        #self.disVec(uvec, 'uvec %d' %(uid))
        #self.disVec(ivec, 'ivec %d' %(iid))


    def train(self):
        print '\n\tbegin train MatrixFactor model ...'
        for iterCnt in range(self.iterNum):
            print '\titeration %d ...' %(iterCnt)
            uvecsum = [.0] * self.vecLen
            ivecsum = [.0] * self.vecLen
            for line in self.trainData:
                self.trainSample(line, uvecsum, ivecsum)
            regularizedError, rmseVal = self.rmse()
            print 'regularizedError %f, rmse %f' %(regularizedError, rmseVal)
            print 'test rmse %f' %(self.testError())
            #self.approMatrix()
        print '\t end train MatrixFactor model ...'


    def approMatrix(self):
        for i in range(1, self.usersNum+1):
            for j in  range(1, self.itemsNum+1):
                uvec = self.usersVec[i]
                ivec = self.itemsVec[j]
                print '%d %d %f' %(i, j, self.vecDot(uvec, ivec))


    def rmse(self):
        regularizedError = 0.0
        rmse = .0
        for line in self.trainData:
            uid = line[0]
            iid = line[1]
            r = line[2]
            uvec = self.usersVec[uid]
            ivec = self.itemsVec[iid]
            rest = self.vecDot(uvec, ivec)
            regularizedError += ((rest - r) * (rest - r) + self.lam * (self.vecSquare(uvec) + self.vecSquare(ivec)))
            rmse += ((rest-float(r))*(rest-float(r)))
        rmse /= float(len(self.trainData))
        rmse = math.sqrt(rmse)
        return regularizedError, rmse
        #return math.sqrt(rmseSum)


    def recommend(self, topk=10):
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        print '\tbegin to recommend top %d items for each user ...' %(topk)
        recDict = {}
        for uid in  range(1, self.usersNum+1):
            uvec = self.usersVec[uid]
            heap = Heap(topk)
            for iid in  range(1, self.itemsNum+1):
                if iid in self.visitedItems[uid]:
                    continue
                else:
                    ivec = self.itemsVec(iid)
                    score = self.vecDot(uvec, ivec)
                    heap.push((score, iid))
            recList = []
            while heap.size() > 0:
                recList.append(heap.pop())
            recList.reverse()
            recDict[udi] = recList
        print '\tfinished recommendation.'
        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        return recDict

    def testError(self):
        esum = 0.0
        for line in self.testData:
            uid = line[0]
            iid = line[1]
            r = line[2]
            uvec = self.usersVec[uid]
            ivec = self.itemsVec[iid]
            pr = self.vecDot(uvec, ivec)
            esum += (pr - float(r)) * (pr - float(r))
        esum /= float(len(self.testData))
        esum = math.sqrt(esum)
        return esum

