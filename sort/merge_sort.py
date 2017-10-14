def merge(a,b):
    c = []
    i = j = 0
    a += ['inf']
    b += ['inf']
    for _k in range(len(a)+len(b)):
        if not (a[i] == 'inf' and b[j] == 'inf'):
            if a[i] <= b[j]:
                c.append(a[i])
                i += 1
            else:
                c.append(b[j])
                j += 1
        else:
            break
    return c


def MERGE_SORT(unsorted_list):
    if len(unsorted_list) <= 1:
        print unsorted_list
        return unsorted_list
    middle = len(unsorted_list)/2
    left = MERGE_SORT(unsorted_list[:middle])
    right = MERGE_SORT(unsorted_list[middle:])
    return merge(left,right)

test = [2,4,5,7,1,2,3]
print MERGE_SORT(test)
