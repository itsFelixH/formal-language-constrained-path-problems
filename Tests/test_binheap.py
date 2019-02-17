import unittest
from binheap import BinHeap


class TestBinHeap(unittest.TestCase):

    def test_init(self):
        heap = BinHeap()

        self.assertEqual(heap.heapList, [0])
        self.assertEqual(heap.currentSize, 0)
        self.assertEqual(heap.key, {})
        self.assertEqual(heap.pos, {})

    def test_insert(self):
        heap = BinHeap()

        heap.insert(1, 10)
        self.assertEqual(heap.heapList, [0, 1])
        self.assertEqual(heap.currentSize, 1)
        self.assertEqual(heap.key, {1: 10})
        self.assertEqual(heap.pos, {1: 1})

    def test_insert__tuple(self):
        heap = BinHeap()

        heap.insert((1, 2), 10)
        self.assertEqual(heap.heapList, [0, (1, 2)])
        self.assertEqual(heap.currentSize, 1)
        self.assertEqual(heap.key, {(1, 2): 10})
        self.assertEqual(heap.pos, {(1, 2): 1})

    def test_buildHeap(self):
        heap = BinHeap()

        alist = [11, 90, 72, 45, 3]
        i = 1
        for key in alist:
            heap.insert(i, key)
            i = i + 1

        self.assertEqual(heap.currentSize, 5)
        self.assertEqual(heap.key, {1: 11, 2: 90, 3: 72, 4: 45, 5: 3})
        self.assertEqual(heap.pos, {1: 2, 2: 4, 3: 3, 4: 5, 5: 1})
        self.assertEqual(heap.heapList, [0, 5, 1, 3, 2, 4])

    def test_bubbleUp(self):
        heap = BinHeap()

        heap.heapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        heap.pos = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13}
        heap.key = {1: 2, 2: 5, 3: 8, 4: 3, 5: 6, 6: 10, 7: 8, 8: 9, 9: 11, 10: 13, 11: 4, 12: 7, 13: 11}
        heap.currentSize = 13
        self.assertEqual(heap.currentSize, 13)
        self.assertEqual(heap.key,
                         {1: 2, 2: 5, 3: 8, 4: 3, 5: 6, 6: 10, 7: 8, 8: 9, 9: 11, 10: 13, 11: 4, 12: 7, 13: 11})
        self.assertEqual(heap.pos,
                         {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13})
        self.assertEqual(heap.heapList, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])

        heap.insert(14, 1)  # benutzt bubbleUp
        self.assertEqual(heap.currentSize, 14)
        self.assertEqual(heap.key,
                         {1: 2, 2: 5, 3: 8, 4: 3, 5: 6, 6: 10, 7: 8, 8: 9, 9: 11, 10: 13, 11: 4, 12: 7, 13: 11, 14: 1})
        self.assertEqual(heap.pos,
                         {1: 3, 2: 2, 3: 7, 4: 4, 5: 5, 6: 6, 7: 14, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 1})
        self.assertEqual(heap.heapList, [0, 14, 2, 1, 4, 5, 6, 3, 8, 9, 10, 11, 12, 13, 7])

    def test_extractMin(self):
        heap = BinHeap()
        heap.insert(1, 10)

        min = heap.extractMin()
        self.assertEqual(heap.currentSize, 0)
        self.assertEqual(heap.key, {1: 10})
        self.assertEqual(heap.pos, {1: 1})
        self.assertEqual(heap.heapList, [0])
        self.assertEqual(min, 1)

    def test_decreaseKey(self):
        heap = BinHeap()
        heap.insert(1, 10)

        heap.decreaseKey(1, 5)
        self.assertEqual(heap.currentSize, 1)
        self.assertEqual(heap.key, {1: 5})
        self.assertEqual(heap.pos, {1: 1})
        self.assertEqual(heap.heapList, [0, 1])

    def test_minChild(self):
        heap = BinHeap()

        heap.heapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        heap.pos = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13}
        heap.key = {1: 2, 2: 5, 3: 8, 4: 3, 5: 6, 6: 10, 7: 8, 8: 9, 9: 11, 10: 13, 11: 4, 12: 7, 13: 11}
        heap.currentSize = 13

        self.assertEqual(heap.minChild(1), 2)
        self.assertEqual(heap.minChild(2), 4)
        self.assertEqual(heap.minChild(3), 7)
        self.assertEqual(heap.minChild(4), 8)
        self.assertEqual(heap.minChild(5), 11)
        self.assertEqual(heap.minChild(6), 12)

    def test_bubbleDown(self):
        heap = BinHeap()

        heap.heapList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        heap.pos = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13}
        heap.key = {1: 2, 2: 5, 3: 8, 4: 3, 5: 6, 6: 10, 7: 8, 8: 9, 9: 11, 10: 13, 11: 4, 12: 7, 13: 11}
        heap.currentSize = 13

        min = heap.extractMin()  # benutzt bubbleDown
        self.assertEqual(heap.currentSize, 12)
        self.assertEqual(heap.key,
                         {1: 2, 2: 5, 3: 8, 4: 3, 5: 6, 6: 10, 7: 8, 8: 9, 9: 11, 10: 13, 11: 4, 12: 7, 13: 11})
        self.assertEqual(heap.pos, {2: 1, 3: 3, 4: 2, 5: 5, 6: 6, 7: 7, 8: 4, 9: 9, 10: 10, 11: 11, 12: 12, 13: 8})
        self.assertEqual(heap.heapList, [0, 2, 4, 3, 8, 5, 6, 7, 13, 9, 10, 11, 12])