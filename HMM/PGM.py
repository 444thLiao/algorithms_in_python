"""
Probabilistic Graphical Models

Bayesian Network

also called 'Belief Network' or 'Probability Network'

Hidden Markov Model also is a kind of PGM
"""
from pandas import DataFrame as df

class Node(object):

    def __init__(self,text):
        self.text = text
        self.parent = []
        self.pro_table = []
        self.son = []
    def __repr__(self):
        return self.text

    def __eq__(self, other):
        if 'text' in dir(other):
            return other.text == self.text
        elif type(other) == str:
            return other == self.text
        else:
            raise SyntaxError,'Wrong comparement.'

# class PGM(object):
#     def __init__(self,nodes):
#
class BayesianModel(object):

    def __init__(self,edges,nodes = []):
        self.nodes = nodes
        self.edges = []
        for edge in edges:
            #print edge
            edge_s = edge[0]
            edge_e = edge[1]
            node_s = self.add_node(edge_s)
            node_e = self.add_node(edge_e)
            self.add_edge(node_s,node_e)

    def add_node(self,text):
        if text not in self.nodes:
            if type(text) == str:
                node = Node(text)
                self.nodes.append(node)
            else:
                node = text
                self.nodes.append(text)
            return node
        else:
            return [node for node in self.nodes if node == text][0]

    def add_edge(self,s_node,e_node):
        if (s_node,e_node) not in self.edges:
            self.edges.append((s_node,e_node))
            s_node.son.append(e_node)
            e_node.parent.append(s_node)

    def fit_data(self,Joint_dis):
        for node in self.nodes:
            tmp = []
            if not node.parent:
                r1 = []
                r2 = []
                for v_c_node in set(Joint_dis.loc[:,node.text]):
                    header = '%s = %s' % (node.text,v_c_node)
                    r1.append(header)
                    r2.append(sum(list(Joint_dis[Joint_dis.loc[:,node.text] == v_c_node].loc[:,'prob'])))
                tmp.append(r1);tmp.append(r2)
                node.pro_table = df(tmp[1:],columns=tmp[0])
            else:
                subset = Joint_dis.loc[:,[p_node.text for p_node in node.parent]]
                subset_cal = Joint_dis.loc[:,[p_node.text for p_node in node.parent] + [node.text,'prob']]
                derep_subset = subset.drop_duplicates()
                feas = list(subset.columns)
                new_index = []
                cmdline = '%s = %s;' * len(node.parent)
                all_rows = derep_subset.values.tolist()
                for row in all_rows:
                    _temp = row[::]
                    for r_idx,_idx in enumerate(range(0,len(node.parent)*2-1,2)):
                        _temp.insert(_idx,feas[r_idx])
                    new_index.append(cmdline % tuple(_temp))
                cols = []
                cols_v = []
                for each_col in set(subset_cal.loc[:,node.text]):
                    cols.append('%s = %s' % (node.text,each_col))
                    cols_v.append(each_col)

                for row in all_rows:
                    r = []
                    for each_node_v in cols_v:
                        spec_ob = get_JD_pro(subset_cal,row+[each_node_v])
                        all_ob = get_JD_pro(subset_cal.loc[:,list(subset_cal.columns)[:-2]+['prob']], row)
                        r.append(spec_ob/all_ob)
                    tmp.append(r)
                node.pro_table = df(tmp,index = new_index,columns=cols)

    def add_cpds(self,*arg):
        for each in arg:
            node_name = each[0]
            node_table = each[1]

            node_query = [node for node in self.nodes if node == node_name]
            if not node_query:
                print 'error'
                exit()
            else:
                node_query[0].pro_table = node_table

def get_JD_pro(JD,vals):
    sum_for = []
    for val in JD.values.tolist():
        if val[:-1] == vals:
            sum_for.append(val[-1])
    return sum(sum_for)

def format_table(node_name,node_pro_list,node_cols = []):
    result = []
    result.append(node_name)
    cols_name = '%s = %s'
    cols = []
    if not node_cols:
        for x in range(len(node_pro_list[0])):
            cols.append(cols_name % (node_name,x))
        table = df(node_pro_list,columns=cols)
    else:
        table = df(node_pro_list, columns=node_cols)
    result.append(table)
    return result

def count_for(data,vals):
    big = data.values.tolist()
    count = big.count(vals)
    return count

def fit_data_for(data):
    class_feature = {}
    total_comb = 1
    for fea in list(data.columns):
        class_feature[fea] = list(set(data.loc[:,fea]))
        total_comb *= len(class_feature[fea])
    each_rows = []
    current_comb = total_comb
    for fea in list(data.columns):
        current_comb = current_comb/len(class_feature[fea])
        temp = []
        for _i in class_feature[fea]:
            for _ in range(current_comb):
                temp.append(_i)
        temp_new = temp[::] * (total_comb/len(temp))
        each_rows.append(temp_new)
    whole_joint_table = df(each_rows).T
    whole_joint_table.columns = data.columns
    whole_joint_table.loc[:,'prob'] = 0
    for idx in list(whole_joint_table.index):
        vals = whole_joint_table.loc[idx,:].values.tolist()
        vals = vals[:-1]
        v_count = count_for(data,vals)
        whole_joint_table.loc[idx,'prob'] = v_count/float(len(data))
    return whole_joint_table


    # for fea in list(data.columns):
    #     for sub_fea in class_feature[fea]:
    #         whole_joint_table.loc[idx,[]]
# def preprocess_input(input):
#     #TODO
#
# def construct_PGM(input):
#     #TODO


if __name__=='__main__':
    import numpy as np
    import pandas as pd
    raw_data = np.random.randint(low=0, high=2, size=(1000, 5))
    data = pd.DataFrame(raw_data, columns=['D', 'I', 'G', 'L', 'S'])


    JD = fit_data_for(data)
    model = BayesianModel([('D', 'G'), ('I', 'G'), ('I', 'S'), ('G', 'L')])
    model.fit_data(JD)
    print model.nodes[4].pro_table
