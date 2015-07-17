#coding=utf8

class MovieLen:
    def __init__(self, movielenPath='/home/bright/github/music-recom/movielen/ml-100k/ua.base'):
        fin = open(movielenPath)
        self.data = {}
        while True:
            line = fin.readline()
            if not line:
                break
            items = line.split()

        fin.close()

