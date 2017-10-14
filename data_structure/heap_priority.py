from heap_sort import build_max_heap,max_heapify

"""
A Priority Queue is a data structure for maintaining a set S of elements, each with an associated value called a key.
A max-priority queue supports the following operations:
    INSERT(S,x)
    MAXIMUM(S)
    EXTRACT-MAX(S): pop the maximum elements.
    INCREASE-KEY(S,x,k) : increase the value of elements x's key to the new value k,
                          which is assumed to be at least as large as x's current key value.
"""
test = [4,1,3,2,16,9,10,14,8,7]
test = build_max_heap(test)
# A must be a max heap.
def maximum(A):
    return A[0]

def extract_max(A):
    if len(A) < 1:
        return []
    max = A[0]
    A[1] = A[-1]
    A = A[:-1]
    A = max_heapify(A,0)
    return max,A

def increase_key(A,x,key):
    if key < A[x]:
        raise SyntaxError,'new key is smalller than current key'
    A[x] = key
    while x > 0 and A[(x+1)/2-1] < A[x]:
        cache = A[x]
        A[x] = A[(x+1)/2-1]
        A[(x+1)/2-1] = cache
        x = (x+1)/2-1
    return A

def insert(A,key):
    A.append(float('-inf'))
    A = increase_key(A,len(A)-1,key)
    return A


print increase_key(test,6,11)
#print test
