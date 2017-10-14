"""
Quick sort applies divide-and-conquer paradigm.

Divide: split the array into two part with a middle element, middle element is larger than each elements in left part,
    also smaller than each elements in right part.

"""
import random

def partition(A,p,r):
    """
    For in place construct a array which has middle element to split two part.
     each part is completely bigger or lower than the middle element.
    :param A:
    :param p: Normally is 1, or index you want to start but plus 1
    :param r: Normally is the length(A)-1
    :return: Index of the pivot placed.
    """
    #print A,p,r
    x = A[r] # choose a pivot
    i = p-1
    for j in range(p,r):
        #print j,A[j],A[i]
        if A[j] <= x:
            i = i+1
            A[i],A[j] = A[j],A[i]
        #print A
    if i != p-1:
        A[i+1],A[r] = A[r],A[i+1]
    else:
        A[i],A[r] = A[r],A[i]
    #print A,i+1
    return i+1

test = [2,8,7,1,3,5,6,4]
# index_of_pivot = partition(test,1,7)
# assert test == [2,1,3,4,7,5,6,8]
# print 'partition successfully'


def QUICK_SORT(A,p,r):
    if p<r:
        q = partition(A,p,r)
        QUICK_SORT(A,p,q)
        QUICK_SORT(A,q+1,r)
    else:
        return None

QUICK_SORT(test,1,7)
print test
# test2 = [2, 1, 3, 4, 7, 5, 6, 8]
# a=partition(test2,1,1)
# print test2,a

# count = 0
# while count < 10:
#     test_1 = [random.randint(0,100) for _i in range(10)]
#     print test_1
#     QUICK_SORT(test_1,1,9)
#     print test_1
#     count +=1