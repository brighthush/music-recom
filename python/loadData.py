#coding=utf8

import json

DATA_DIR = '../data/'

def loadFile(filePath):
    fin = open(filePath, 'r')
    jsonFile = fin.read()
    data = json.loads(jsonFile)
    fin.close()
    return data

def cleanLoaded():
    songs = loadFile(DATA_DIR + 'songs.txt')
    arts  = loadFile(DATA_DIR + 'arts.txt')
    colls = loadFile(DATA_DIR + 'colls.txt')
    cleaned = {}
    for coll in colls:
        collId = coll
        if collId.isdigit():
            cleaned[collId] = []
        else:
            continue
        songs = colls[coll]
        print collId
        for song_art in songs:
            if song_art[0].isdigit() and song_art[1].isdigit():
                #print '\t', song_art[0], song_art[1]
                cleaned[collId].append((song_art[0], song_art[1]))
            else:
                #print '\t remove ', song_art[0], song_art[1]
                songs.remove(song_art)
    colls = cleaned
    for coll in colls:
        collId = coll
        songs = colls[collId]
        print collId
        for song_art in songs:
            print '\t', song_art[0], song_art[1]
    return colls, songs, arts


def statData(colls, songs, arts):
    collsLen = len(colls)
    songsLen = len(songs)
    artsLen = len(arts)
    songSet = set()
    artSet = set()
    print ('collsLen %d, songsLen %d, artsLen %d\n' %(collsLen, songsLen, artsLen))
    sumLen = 0
    for collId in colls:
        songs = colls[collId]
        sumLen += len(songs)
        for song_art in songs:
            songSet.add(song_art[0])
            artSet.add(song_art[1])
    print 'every collection has %.6lf songs' %( float(sumLen) / float(collsLen))
    print 'colls have %d songs, %d arts' %(len(songSet), len(artSet))



def main():
    colls, songs, arts = cleanLoaded()
    statData(colls, songs, arts)

if __name__ == '__main__':
    main()

