#coding=utf8

class MovieLen:
    users = {}
    itemsSet = set()
    def __init__(self, movielenPath='/home/bright/github/music-recom/movielen/ml-100k/u.data'):
        fin = open(movielenPath)
        self.data = {}
        while True:
            line = fin.readline()
            if not line:
                break
            items = line.split()
            if len(items) != 4:
                continue
            uid = int(items[0])
            iid = int(items[1])
            self.itemsSet.add(iid)
            r = int(items[2])
            ts = int(items[3])
            if uid not in self.users:
                self.users[uid] = []
            self.users[uid].append((iid, r, ts))

        usersNum = len(self.users)
        itemsNum = len(self.itemsSet)
        minItems = -1
        maxItems = -1
        itemsSum = 0
        for uid in self.users:
            itemsList = self.users[uid]
            itemsList.sort(key=lambda x : x[2])
            listLen = len(itemsList)

            if minItems == -1:
                minItems = listLen
            else:
                minItems = min(minItems, listLen)

            if maxItems == -1:
                maxItems = listLen
            else:
                maxItems = max(maxItems, listLen)
            itemsSum += listLen
        print '=============================================='
        print 'finished read movielen data'
        print 'total %d users' %(usersNum)
        print 'total %d items' %(itemsNum)
        print 'each user rated items range [%d, %d]' %(minItems, maxItems)
        print 'each user rated avg %.6lf items' %(float(itemsSum) / float(usersNum))
        print '=============================================='
        fin.close()

    def buildData():
        trainData = []
        testData = []
        for uid in self.users:
            ilist = self.users[uid]
            for i in range(len(ilist)):
                item = ilist[i]
                iid = item[0]
                r = item[1]
                ts = item[2]
                if i == len(ilist) - 1:
                    testData.append((uid, iid, r, ts))
                else:
                    trainData.append((uid, iid, r, ts))
        return trainData, testData

    def getUsersNum():
        return len(self.users)

    def getItemsNum():
        return len(self.itemsSet)


def main():
    ml = MovieLen()

if __name__ == '__main__':
    main()

