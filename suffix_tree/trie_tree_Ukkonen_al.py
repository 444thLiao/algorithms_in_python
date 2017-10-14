from generate_suffix import generate_prefix, generate_suffix
from collections import Counter


class Node(object):
    def __init__(self, text):
        self.text = text
        self.son = []
        self.parent = ''
        self.suffix_link = None
        # self.count = 0

    def __repr__(self):
        return self.text

    def __eq__(self, other):
        if 'text' in dir(other):
            if self.text == other.text:
                return True
            else:
                return False
        elif type(other) == str:
            if self.text == other:
                return True
            else:
                return False
        else:
            raise IOError, 'Wrong compare.'

    def link_suffix(self, other_node):
        '''directional '''
        if other_node != self:
            self.suffix_link = other_node

    def add_son(self, node):
        self.son.append(node)
        node.add_parent(self)

    def add_parent(self, node):
        self.parent = node

    def drop_son(self, node):
        if node in self.son:
            self.son.remove(node)

    def get_son(self):
        return self.son

    def get_parent(self):
        return self.parent

    def change_text(self, new_text):
        self.text = new_text


class dict_tree(object):
    def __init__(self, root):
        self.root = root
        self.compressed = False
        # self.nodes = []

    def get_all_nodes(self, pnode=''):
        nodes = []
        if not pnode:
            pnode = self.root
        if pnode.get_son():
            nodes.append(pnode)
            for snode in pnode.get_son():
                nodes += self.get_all_nodes(snode)
        else:
            nodes.append(pnode)
            return nodes
        return nodes

    def prefix_to_locate(self, prefix):
        check = {word: generate_prefix(word) for word in trie.get_all_words()}
        finded_word = ''
        for word, prefixs in check.items():
            if prefix in prefixs:
                finded_word = word
        if not finded_word:
            return None
        # prefix inside one node
        for node in self.get_node_lineage(finded_word):
            if prefix in generate_prefix(node.text):
                return node
        # prefix in two series of nodes.
        for be, af in zip(self.get_node_lineage(finded_word)[:-1], self.get_node_lineage(finded_word)[1:]):
            if prefix in be.text + af.text:
                return [be, af]
    def construct_suffixtree_ukkonen(self, word):
        active_point = [self.root, '', 0]
        remainder = 0
        def split_merge(active_point, node, letter):
            pnode = node.get_parent()
            suffix_text = node.text[active_point[2]:]
            print '%s--%s ====>' % (pnode.text, node.text)
            node.change_text(node.text[:active_point[2]])
            node.add_son(Node(suffix_text))
            node.add_son(Node(letter))
            print '%s--[%s--[%s,%s]]' % (pnode.text, node.text, suffix_text, letter)
            return node
            # if type(node) == list:
            #     nodep,nodes = node
            #     nodep.drop_son(nodes)
            #
            #     new_node = Node(active_point[1][len(nodep.text):])
            #
            #     nodep.add_son(new_node)
            #     print '%s--%s ====>' % (nodep.text, nodes.text)
            #     nodes.change_text(nodes.text[len(new_node.text):])
            #     new_node.add_son(nodes)
            #     new_node.add_son(Node(letter))
            #     print '%s--[%s--[%s,%s]]' % (nodep.text, new_node.text, letter,nodes.text)
            #     return new_node
            # else:
            #     aft = node.text[:active_point[2]]
            #     son_aft = node.text[active_point[2]:]
            #     print '%s ====> ' % (node.text)
            #     node.change_text(aft)  # split ori node into small one.
            #     node.add_son(Node(son_aft))  # add splited as son to node.
            #     node.add_son(Node(letter))  # just add one new branch, so remainder minux 1.
            #     print '%s--[%s,%s]' % (node.text, son_aft, letter)
            #     return node
        def active_point_return_node(active_point,checked_letter):
            if active_point[1]:
                if not active_point[0].text:
                    check_nodes = \
                        [son for son in active_point[0].get_son() if
                         checked_letter[:-1] == son.text[:active_point[2]]][
                            0]
                else:
                    check_nodes = [son for son in active_point[0].get_son() if
                                   checked_letter[checked_letter.rindex(active_point[0].text)+len(active_point[0].text):-1] == son.text[
                                                                                                     :active_point[2]]][0]
            else:
                check_nodes = active_point[0]
            print 'accept: active_point to locate:',active_point,check_nodes
            return check_nodes

        def check_exist(active_point, checked_letter):
            # get former node.
            try:
                check_nodes = active_point_return_node(active_point,checked_letter)
            except:
                import pdb;pdb.set_trace()
            if not check_nodes.get_son():
                poss_check_nodes = [check_nodes.text]
            else:
                poss_check_nodes = [check_nodes.text + son.text for son in check_nodes.get_son()]
            for poss in poss_check_nodes:
                if checked_letter in generate_prefix(poss):
                    return True

        for idx, letter in enumerate(word):
            # loop in this word.
            # if letter == 'b':
            #     import pdb;pdb.set_trace()
            print letter,active_point
            remainder += 1
            if not self.root.get_son():
                self.root.add_son(Node(letter))  # init the first node.
                remainder -= 1
            else:
                all_last_node = [_node for _node in self.get_all_nodes() if not _node.get_son()]  # find all leaf nodes
                for node in all_last_node:
                    node.change_text(node.text + letter)  # expand each line.
                checked_letter = active_point[1] + letter

                if not check_exist(active_point,
                                   checked_letter):  # check current 'active_edge + letter' is a existed prefix or not?
                    splited_node = []
                    # import pdb;pdb.set_trace()
                    while remainder > 1:
                        print 'implictly', remainder, active_point, letter
                        # node = self.prefix_to_locate(active_point[1])
                        try:
                            added_node = active_point_return_node(active_point,checked_letter)
                        except:
                            import pdb;pdb.set_trace()
                        node_sp = split_merge(active_point, added_node, letter)
                        remainder -= 1
                        if active_point[0]==self.root and not active_point[0].suffix_link:
                            active_point[0] = self.root
                            active_point[2] -= 1
                        elif active_point[0]!=self.root and not active_point[0].suffix_link:
                            active_point[0] = self.root
                        else:
                            active_point[0] = active_point[0].suffix_link

                        active_point[1] = checked_letter[1:]
                        checked_letter = checked_letter[1:]
                        #new_idx_for_node = active_point_return_node(active_point)

                        if splited_node:
                            splited_node[-1].link_suffix(node_sp)
                        splited_node.append(node_sp)

                    active_point[0].add_son(Node(letter)) # add new branch in root
                    #active_point[2] -= 1
                    if remainder == 1:
                        active_point = [self.root, '', 0]
                        remainder -= 1

                else:
                    print 'accept existed node'
                    node = self.get_node_lineage(checked_letter)[-1]  # find nodes which have these word.
                    ac_p = node
                    # if node.text == checked_letter:
                    #     active_point[0] = node.get_parent()
                    # elif len(node.text) < len(checked_letter):
                    #
                    #
                    # if node.text == checked_letter[-len(node.text):]:  # check whether the node cover whole word.
                    #     active_point[0] = node.get_parent()  # if is, assert this node.parent as active_point
                    # else:
                    #     find_prefix = checked_letter[len(node.text):]  # if not, fetch remain word.
                    #     for son in node.get_son():
                    #         if find_prefix == son.text[:len(find_prefix)]:  # find next node.
                    #             active_point[0] = node
                    #             ac_p = son
                    #     if ac_p == node: # if next node == ori node. it have some problems.
                    #         import pdb;pdb.set_trace()
                    #         raise SyntaxError, 'Bad code.'
                    active_point[0] = ac_p.get_parent()
                    active_point[1] = checked_letter
                    active_point[2] = ac_p.text.index(letter) + 1

    def add_son(self, s_node, p_node_text=''):
        if not p_node_text:
            if s_node not in self.root.get_son():
                # self.nodes.append(s_node)
                p_node = self.root
                p_node.add_son(s_node)
        else:
            p_node = self.get_last_node(p_node_text)

            if s_node not in p_node.get_son():
                p_node.add_son(s_node)

    def get_last_node(self, lineage_text):
        print lineage_text
        current_parent = self.root
        if lineage_text == '':
            return current_parent
        while 1:
            # print lineage_text
            sons = current_parent.get_son()
            if not sons or not lineage_text:
                break
            prefixs = generate_prefix(lineage_text)
            for prefix in prefixs:
                if prefix in sons:
                    current_parent = [son for son in sons if son == prefix][0]
            lineage_text = lineage_text[len(current_parent.text):]
        return current_parent

    def get_all_words(self, node=None):
        all_last_node = [_node for _node in self.get_all_nodes() if not _node.get_son()]  # find all leaf node
        words = []
        for lnode in all_last_node:
            temp = lnode.text
            while 1:
                lnode = lnode.get_parent()
                if not lnode:
                    break
                temp = lnode.text + temp

            words.append(temp)
        return words

    def get_node_lineage(self, lineage_text):
        lineages = []
        current_parent = self.root
        if lineage_text == '':
            return current_parent

        while 1:
            sons = current_parent.get_son()
            if not sons or not lineage_text:
                break
            for son in sons:
                if lineage_text == son.text[:len(lineage_text)]:
                    current_parent = son
                    if current_parent not in lineages:
                        lineages.append(current_parent)
            if not lineages:
                for son in sons:
                    if son.text == lineage_text[:len(son.text)]:
                        current_parent = son
                        lineages.append(current_parent)
            lineage_text = lineage_text[len(current_parent.text):]
        return lineages

    def compressed_one(self, node):
        '''
        if will compress the parents recursively till it can't compress
        :param node:
        :return:
        '''
        if node == '':
            pass
        else:
            parent_node = node.get_parent()
            if len(parent_node.get_son()) == 1:
                parent_node.change_text(parent_node.text + node.text)
                if node.get_son():
                    for ssnode in node.get_son():
                        parent_node.add_son(ssnode)
                parent_node.drop_son(node)
                return 'succeed'
            else:
                return 'failed'

    def compressed_self(self):
        while 1:
            all_nodes = self.get_all_nodes()
            status = []
            for node in all_nodes:
                status.append(self.compressed_one(node))
            if 'succeed' not in status:
                break
        self.compressed = True
        print 'Tree has been compressed.'


if __name__ == '__main__':
    root = Node('')
    trie = dict_tree(root)
    trie.construct_suffixtree_ukkonen('abcabxabcd')

    # trie.get_all_nodes()
