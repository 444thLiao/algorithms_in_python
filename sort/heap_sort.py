
# basic definition
"""
A is a num array, using 1-coordinate.
For Node i, its value = A[i]
    PARENT Node is i/2
    LEFT CHILD Node is 2i
    RIGHT CHILD Node is 2i+1
"""

def max_heapify(A,i):
    l_i = (i+1)*2 - 1
    r_i = (i+1)*2 +1 -1

    l = A[l_i]
    ori = A[i]
    try:
        r = A[r_i]
    except:
        r = min(ori,l) - 1
    # in case we choose the node which only have one left child node.
    largest = ori
    largest_i = i

    if l > ori:
        largest_i = l_i
        largest = l
    if r > largest:
        largest_i = r_i
        largest = r
    if largest_i != i:
        A[i] = largest
        A[largest_i] = ori
        if largest_i not in range(len(A)/2,len(A)+1):
            # if largest_i not in the leaves nodes.
            return max_heapify(A,largest_i)
    return A

def build_max_heap(A):
    for i in range(len(A)/2-1, -1, -1):
        A = max_heapify(A,i)
    return A

def heapsort(A):
    A = build_max_heap(A)
    #print 'max heap A: ',A
    for i in range(len(A)-1,1,-1):
        cache = A[i]
        A[i] = A[0]
        A[0] = cache
        try:
            A = max_heapify(A[:i],0) + A[i:]
        except:
            # when sorting single node array, it will raise error.
            # if we not iterate the single node array, it will put the smallest two reverse because of the max_heapify process.
            pass
    return A
test = [4,1,3,2,16,9,10,14,8,7]

#print max_heapify(test,1)
#print heapsort(test)
