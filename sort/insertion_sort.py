
import cProfile
import random
def insertion_sort(unsorted_list):
    for _i,_v in enumerate(unsorted_list):
        if _i >= 1:
            current_v = _v
            left_v = unsorted_list[_i-1]
            unsorted_list.pop(_i) # remove current value
            while _i >=0 and left_v > current_v:
                _i = _i-1 # continue to seek the before one
                if _i > 0: # if there is one more before
                    left_v = unsorted_list[_i-1] # fetch it as left_v in order to compare with current v
                else:
                    break # if it doesn't, mean current value have been move to the frontest, just stop.
            unsorted_list.insert(_i,current_v)
    return unsorted_list
test = [5,2,4,6,1,3]
test2 = []

for _i in xrange(1000):
    test2.append(random.randint(1,1000))

cProfile.run('insertion_sort(test2)')