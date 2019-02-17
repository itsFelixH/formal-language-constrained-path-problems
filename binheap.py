class BinHeap:

    def __init__(self):
        """Initialize a binary heap."""

        self.heapList = [0]
        self.currentSize = 0
        self.key = {}
        self.pos ={}
        
    def bubbleUp(self, i):
        """Restore heap property by traversing up.
        Parameters:
        i : int (index of element to bubble up)"""

        while i // 2 > 0:
            if self.key[self.heapList[i]] < self.key[self.heapList[i//2]]:
                
                tmp = self.heapList[i//2]
                tmppos = self.pos[self.heapList[i//2]]
                self.pos[self.heapList[i//2]] = self.pos[self.heapList[i]]
                self.heapList[i//2] = self.heapList[i]
                self.pos[self.heapList[i]] = tmppos
                self.heapList[i] = tmp
                
                
            i = i//2
    
    def insert(self, element, key):
        """Insert element into the heap
        Parameters:
        element : (element to insert into heap)
        key : int (key value of element)"""

        self.heapList.append(element)
        self.currentSize = self.currentSize + 1
        self.key[element] = key
        self.pos[element] = self.currentSize
        self.bubbleUp(self.currentSize)
    
    def bubbleDown(self, i):
        """Restore heap property by traversing down
        Parameters:
        i : int (index of element to bubble down)"""

        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.key[self.heapList[i]] > self.key[self.heapList[mc]]:
                
                tmp = self.heapList[i]
                tmppos = self.pos[self.heapList[i]]
                self.pos[self.heapList[i]] = self.pos[self.heapList[mc]]
                self.heapList[i] = self.heapList[mc]
                self.pos[self.heapList[mc]]= tmppos
                self.heapList[mc]= tmp
                
            i = mc
            
    def minChild(self, i):
        """Computes child of element i with minimum key value
        Parameters:
        i : int (index of element)

        Returns:
        : int (index of minimum child)"""

        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.key[self.heapList[i * 2]] < self.key[self.heapList[i * 2 + 1]]:
                return i * 2
            else:
                return i * 2 + 1
    
    def extractMin(self):
        """Computes element i with minimum key value
        Returns:
        min : (element with min key value)"""

        min = self.heapList[1]
        self.pos.pop(self.heapList[1])
        self.pos[self.heapList[self.currentSize]] = 1
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.bubbleDown(1)
        return min
    
    def decreaseKey(self, element, key):
        """Decreases key of element in the heap
        Parameters:
        element : (element to decrease key from)
        key : int (new key value)"""

        self.key[element] = key
        self.bubbleUp(self.pos[element])