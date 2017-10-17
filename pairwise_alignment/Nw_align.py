import numpy as np
"""
Needleman-Wunsch algorithm
For align two whole string.
"""
def score_system(a=1,b=-1,c=-1):
    global match
    global mismatch
    global indel
    match = a
    mismatch = b
    indel = c

def visu_table(table):
    for row in table:
        print ' '.join(['{:>4}'.format(str(i)) for i in row])

def construct_table(a_str,b_str):

    cols = [0] * (len(a_str) + 1)
    table = []
    for i in range(len(b_str)+1):
        table.append(cols[::])
    # table = [cols] * (len(b_str) + 1)

    # init the table
    table[0] = [i*indel for i in range(len(table[0]))]
    for _i in range(len(table)):
        table[_i][0] = _i*indel
    for row in range(1,len(table)):
        for col in range(1,len(table[0])):
            c_left = table[row][col-1] + indel # indel
            c_top = table[row-1][col] + indel # indel
            left_top = table[row-1][col-1]
            if a_str[col-1] == b_str[row-1]:
                c_left_top = left_top + match
            else:
                c_left_top = left_top + mismatch
            table[row][col] = max(c_left,c_top,c_left_top)
    return table

def get_v(table,loc):
    try:

        return table[loc[0]][loc[1]]
    except:
        return -np.inf

def next_loc(loc):
    return [loc[0],loc[1]+1],[loc[0]+1,loc[1]],[loc[0]+1,loc[1]+1]

def track_back(a_str,b_str,table):
    # right = [0,1]
    # down = [1,0]
    # right_down = [1,1]
    ali1 = ''
    ali2 = ''
    value = 0
    loc = [0,0]
    storge = [[value,ali1,ali2,loc]]
    result = []
    while 1:
        #print storge
        if not storge:
            break
        for each in storge:
            if len(each[1]) - each[1].count('_') == len(a_str) or len(each[2]) - each[2].count('_') == len(b_str):
                result.append([each[0],each[1],each[2]])
                storge.remove(each)
                continue
            right, down, right_down = next_loc(each[3])
            right_v = get_v(table,right)
            down_v = get_v(table, down)
            right_down_v = get_v(table, right_down)
            max_v = max(right_v,down_v,right_down_v)

            poss = []
            if right_v == get_v(table,each[3]) + indel:
                poss.append(right)
            if down_v == get_v(table,each[3]) + indel:
                poss.append(down)
            if a_str[right_down[1]-1] == b_str[right_down[0]-1]:
                if right_down_v == get_v(table,each[3]) + match:
                    poss.append(right_down)
            else:
                if right_down_v == get_v(table,each[3]) + mismatch:
                    poss.append(right_down)

            each[0] = max_v
            poss_v = [(loc,get_v(table,loc)) for loc in poss]

            if [v for loc,v in poss_v].count(max_v) == 1:
                loc = [loc for loc,v in poss_v if max_v == v][0]
                if loc == down:
                    each[1] += '_'
                    each[2] += b_str[down[0]-1]
                    each[3] = down
                elif loc == right:
                    each[1] += a_str[right[1]-1]
                    each[2] += '_'
                    each[3] = right
                elif loc == right_down:
                    each[1] += a_str[right_down[1]-1]
                    each[2] += b_str[right_down[0]-1]
                    each[3] = right_down
            elif [v for loc,v in poss_v].count(max_v) >1:
                storge.remove(each)
                for loc,v in [(loc,v) for loc,v in poss_v if v == max_v]:
                    if loc == down:
                        _ali1 = each[1] + '_'
                        _ali2 = each[2] + b_str[down[0]-1]
                        _loc = down
                        _value = v
                    elif loc == right:
                        _ali1 = each[1]+ a_str[right[1]-1]
                        _ali2 = each[2] + '_'
                        _loc = right
                        _value = v
                    elif loc == right_down:
                        _ali1 = each[1] + a_str[right_down[1]-1]
                        _ali2 = each[2] + b_str[right_down[0]-1]
                        _loc = right_down
                        _value = v
                    new_storged = [_value,_ali1,_ali2,_loc]
                    storge.append(new_storged)
            else:
                storge.remove(each)
                continue

    return result

if __name__ == '__main__':
    score_system(1,-1,-1)
    table = construct_table('GCATGCU','GATTACA')
    visu_table(table)
    print max(track_back('GCATGCU','GATTACA',table))