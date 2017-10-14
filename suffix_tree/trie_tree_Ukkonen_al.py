from generate_suffix import generate_prefix
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
            #print 'accept: active_point to locate:',active_point,check_nodes
            return check_nodes

        def check_exist(active_point, checked_letter):
            # get former node.
            check_nodes = active_point_return_node(active_point,checked_letter)
            if not check_nodes.get_son():
                poss_check_nodes = [check_nodes.text]
            else:
                poss_check_nodes = [check_nodes.text + son.text for son in check_nodes.get_son()]
            for poss in poss_check_nodes:
                if checked_letter in generate_prefix(poss):
                    return True

        for idx, letter in enumerate(word):

            #print letter,active_point
            remainder += 1
            if not self.root.get_son():
                self.root.add_son(Node(letter))  # init the first node.
                remainder -= 1
            else:
                all_last_node = [_node for _node in self.get_all_nodes() if not _node.get_son()]  # find all leaf nodes
                for node in all_last_node:
                    node.change_text(node.text + letter)  # expand each line.
                checked_letter = active_point[1] + letter

                if not check_exist(active_point,checked_letter):  # check current 'active_edge + letter' is a existed prefix or not?
                    splited_node = []
                    while remainder > 1:
                        print 'implictly', remainder, active_point, letter
                        # node = self.prefix_to_locate(active_point[1])
                        added_node = active_point_return_node(active_point,checked_letter)
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
                    print 'find existed word'
                    node = self.get_node_lineage(checked_letter)[-1]  # find nodes which have these word.
                    ac_p = node
                    active_point[0] = ac_p.get_parent()
                    active_point[1] = checked_letter
                    active_point[2] = ac_p.text.index(letter) + 1

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

if __name__ == '__main__':
    root = Node('')
    trie = dict_tree(root)
    trie.construct_suffixtree_ukkonen('abcabxabcd')


