"""
Probabilistic Graphical Models

Bayesian Network

also called 'Belief Network' or 'Probability Network'

Hidden Markov Model also is a kind of PGM
"""
from pandas import DataFrame as df
import itertools
class Node(object):

    def __init__(self,text):
        self.text = text
        self.parent = []
        self.pro_table = []
        self.son = []
    def __repr__(self):
        return self.text
    def __ne__(self, other):
        if 'text' in dir(other):
            return other.text != self.text
        elif type(other) == str:
            return other != self.text
        else:
            raise SyntaxError,'Wrong comparement.'

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

    def add_cpds(self,text,table):
        '''
        cpd mean 'local conditional distributions'
        :param text:
        :param table:
        :return:
        '''
        node = [node for node in self.nodes if node == text][0]
        node.pro_table = table

    def print_cal_reference(self):
        L_equation= 'P('+', '.join([n.text for n in self.nodes])+')'
        each_p = []
        for n in self.nodes:
            if not n.parent:
                each_p.append('P(%s)' % n.text)
            else:
                each_p.append('P(%s|%s)' % (n.text,','.join([pn.text for pn in n.parent])))
        final_eq = '%s = %s' % (L_equation,' * '.join(each_p))
        print final_eq
    def cal_ref(self,ob_t,values):
        """
        inference means calculating the conditional distribution.
        like P(H|V) = P(H,V)/SIGMA(P(H,V),all_H)
        :param ob_t:
        :param values:
        :return:
        """
        if type(ob_t) == str:
            all_other_nodes = [list(n.pro_table.columns) for n in self.nodes if n != ob_t] + [['%s = %s' % (ob_t,values)]]

        else:
            all_other_nodes = [list(n.pro_table.columns) for n in self.nodes if n not in ob_t] + [['%s = %s' % (ob,v)] for ob,v in zip(ob_t,values)]
        vals = 0
        for comb in itertools.product(*all_other_nodes):
            each_comb = 1
            for node in self.nodes:
                data = node.pro_table
                if not node.parent:
                    each_comb *= [data.loc[0, col] for col in list(data.columns) if col in comb][0]
                else:
                    for col in list(data.columns):
                        for index in list(data.index):
                            if col in comb and len(set(index.split(';')).intersection(set(comb))) == len(node.parent):
                                each_comb *= data.loc[index, col]
            vals += each_comb
        return vals

    def cal_condi_prob(self,left,left_v,right,right_v):
        """
        all must be list. I'm tired to write if else.
        :param left:
        :param left_v:
        :param right:
        :param right_v:
        :return:
        """

        upper = self.cal_ref(left+right,left_v+right_v)
        down = self.cal_ref(right,right_v)
        return upper/down
    def diagonistic(self):
        #TODO
        pass



def formatted_cpds(node_self,n_c_self,table,rows=[],n_c_rows=[]):
    '''

    :param node_self:
    :param n_c_self: num of class in 'node' feature or list of values you specify.
    :param table:
    :param rows:
    :param n_c_rows: list of num of class in 'rows' feature. or list of list values you specify
    :return:
    '''
    cols = []
    if type(n_c_self) == int:
        for i in range(n_c_self):
            cols.append('%s = %s' % (node_self,i))
        if len(table[0]) != n_c_self:
            table = df(table).T.values.tolist()
    else:
        for v in n_c_self:
            cols.append('%s = %s' % (node_self,v))
        if len(table[0]) != len(n_c_self):
            table = df(table).T.values.tolist()

    if not rows:
        final_table = df(table,columns=cols)
    else:
        indexs = []
        v_class = []
        base_index = '%s = %s;' * len(rows)
        for n_c in n_c_rows:
            if type(n_c) == int:
                v_class.append(range(n_c))
            else:
                v_class.append(n_c)

        for row in itertools.product(*v_class):
            _temp = list(row[::])
            for r_idx, _idx in enumerate(range(0, len(rows) * 2 - 1, 2)):
                _temp.insert(_idx, rows[r_idx])
            indexs.append(base_index % tuple(_temp))

        final_table = df(table,columns=cols,index=indexs)
    return final_table

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


if __name__=='__main__':
    import numpy as np
    import pandas as pd
    # raw_data = np.random.randint(low=0, high=2, size=(1000, 5))
    # data = pd.DataFrame(raw_data, columns=['D', 'I', 'G', 'L', 'S'])
    #
    #
    # JD = fit_data_for(data)

    # model = BayesianModel([('C', 'S'), ('C', 'R'), ('S', 'W'), ('R', 'W')])
    # c_cpds = formatted_cpds('C',2,[[0.5,0.5]])
    # sc_cpds = formatted_cpds('S',2,[[0.5,0.5],[0.9,0.1]],rows=['C'],n_c_rows=[2])
    # rc_cpds = formatted_cpds('R', 2, [[0.8, 0.2], [0.2, 0.8]], rows=['C'], n_c_rows=[2])
    # wsr_cpds = formatted_cpds('W', 2, [[1.0, 0], [0.1, 0.9],[0.1,0.9],[0.01,0.99]], rows=['S','R'], n_c_rows=[2,2])
    # #model.fit_data(JD)
    # model.add_cpds('C',c_cpds)
    # model.add_cpds('S', sc_cpds)
    # model.add_cpds('R', rc_cpds)
    # model.add_cpds('W', wsr_cpds)
    # print [n.pro_table for n in model.nodes]
    # model.print_cal_reference()
    # print model.cal_ref('W',1)
    # print model.cal_ref(['R','W'], [1,1])
    # print model.cal_ref(['R','W','S'],[1,1,1])

    model = BayesianModel([('D', 'G'), ('I', 'G'), ('I', 'S'), ('G', 'L')])
    d_cpds = formatted_cpds('D',2,[[0.6,0.4]])
    i_cpds = formatted_cpds('I', 2, [[0.7, 0.3]])
    gid_cpds = formatted_cpds('G', [1,2,3], [[0.3, 0.4,0.3], [0.05, 0.25,0.7],[0.9,0.08,0.02],[0.5,0.3,0.2]], rows=['I','D'], n_c_rows=[2,2])
    si_cpds = formatted_cpds('S',2,[[0.95,0.05],[0.2,0.8]],rows=['I'],n_c_rows=[2])
    lg_cpds = formatted_cpds('L',2,[[0.1,0.9],[0.4,0.6],[0.99,0.01]],rows=['G'],n_c_rows=[[1,2,3]])
    #model.fit_data(JD)
    model.add_cpds('D',d_cpds)
    model.add_cpds('I', i_cpds)
    model.add_cpds('G', gid_cpds)
    model.add_cpds('S', si_cpds)
    model.add_cpds('L', lg_cpds)
    #print [n.pro_table for n in model.nodes]
    # model.print_cal_reference()
    # print model.cal_ref('W',1)
    # print model.cal_ref(['R','W'], [1,1])
    # print model.cal_ref(['R','W','S'],[1,1,1])
    print model.cal_ref(['I','D','G','S','L'], [1,0,2,1,0])
    print model.cal_ref(['L'],['1'])
    print model.cal_condi_prob(['L'],[1],['I'],[0])
    print model.cal_condi_prob(['L'], [1], ['I','D'], [0,0])
    #print model.cal_ref(['L', 'I'], [1, 0])