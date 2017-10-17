import numpy as np
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

    table[0] = [i*indel if i*indel > 0 else 0 for i in range(len(table[0]))]
    for _i in range(len(table)):
        if _i*indel < 0 :
            table[_i][0] = 0
        else:
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
            if max(c_left,c_top,c_left_top) < 0 :
                table[row][col] = 0
            else:
                table[row][col] = max(c_left,c_top,c_left_top)
    return table

def get_v(table,loc):

    try:
        return table[loc[0]][loc[1]]
    except:
        return np.inf

def next_loc(loc):
    """
    :param loc:
    :return: left,top,left-top
    """
    return [loc[0],loc[1]-1],[loc[0]-1,loc[1]],[loc[0]-1,loc[1]-1]


def sw_align(a_str,b_str,table):
    vals = []
    for row in table:
        vals+=row[::]
    max_v = max(vals)
    max_v_locs = []
    for row in range(1,len(table)):
        for col in range(1,len(table[0])):
            if table[row][col] == max_v:
                max_v_locs.append([row,col])
    max_v_count = len(max_v_locs)

    storge = []
    result = []
    for loc in max_v_locs:
        ali1 = a_str[loc[1]-1]
        ali2 = b_str[loc[0]-1]
        storge+=[[ali1, ali2, loc]]

    while 1:
        #print storge
        if not storge:
            break
        for each in storge:
            if get_v(table,each[2]) in [0,np.inf]:
                #print 'test'
                result.append([each[0],each[1]])
                storge.remove(each)
                continue
            left, top, left_top = next_loc(each[2])

            poss = []
            #if each == ['CA', 'CA', [6, 5]]:
            #    import pdb;pdb.set_trace()
            if get_v(table,left) + indel == get_v(table,each[2]):
                poss.append(left)
            if get_v(table,top) + indel == get_v(table,each[2]) :
                poss.append(top)

            if a_str[left_top[1]] == b_str[left_top[0]]:
                if get_v(table,left_top) + match == get_v(table,each[2]) :
                    poss.append(left_top)
            else:
                if get_v(table,left_top) + mismatch == get_v(table,each[2]):
                    poss.append(left_top)

            #print storge
            storge.remove(each)
            #print storge,poss,left,top,left_top
            for poss_dir in poss:
                #print poss_dir
                loc = poss_dir
                if poss_dir == left:
                    _ali1 = each[0] + a_str[left[1]]
                    _ali2 = each[1] + '_'
                elif poss_dir == top:
                    _ali1 = each[0] + '_'
                    _ali2 = each[1] + b_str[top[0]]
                elif poss_dir == left_top:
                    _ali1 = each[0] + a_str[left_top[1]-1]
                    _ali2 = each[1] + b_str[left_top[0]-1]

                new_storged = [_ali1, _ali2, loc]
                storge.append(new_storged)
    return result

if __name__ == '__main__':
    score_system(3,-3,-2)
    table = construct_table('TGTTACGG','GGTTGACTA')
    visu_table(table)
    print sw_align('TGTTACGG','GGTTGACTA',table)