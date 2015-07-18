#coding=utf8
"""
This file implemented the top minimum heap.
"""

import heapq

class Heap:
    heap = []
    def __init__(self, k=10):
        self.k = k;

    def push(self, val):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        else:
            heapq.heappushpop(self.heap, val)

    def top(self):
        if len(self.heap) > 0:
            return self.heap[0]
        else:
            return None

    def pop(self):
        if len(self.heap) > 0:
            val = heapq.heappop(self.heap)
            return val
        else:
            return None

    def size(self):
        return len(self.heap)


def main():
    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    print '\tUsage of Heap.'
    print '\t\t1 value, add a value to heap'
    print '\t\t0, get the top value in the heap'
    print '\t\t-1, pop a value in the heap'
    print '+++++++++++++++++++++++++++++++++++++++++++++++'
    h = Heap(5)
    while True:
        op = input('operation:')
        if int(op) == 1:
            val = input('value:')
            val = int(val)
            h.push(val)
        elif int(op) == 0:
            print 'top value is %d' %(h.top())
        elif int(op) == -1:
            print 'pop value is %d' %(h.pop())
        else:
            print 'heap size if %d' %(h.size())

if __name__ == '__main__':
    main()


