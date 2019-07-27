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
            raise IOError('Wrong compare.')

    def link_suffix(self, other_node):
        '''suffix link'''
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
        # init a two parameters
        self.active_point = [self.root, '', 0]
        self.remainder = 0
        # self.nodes = []
    def get_current_pnode(self):
        return self.active_point[0]
    def get_active_edge(self):
        return self.active_point[1]
    def get_last_pos(self):
        return self.active_point[2]

    def get_all_nodes(self, pnode=''):
        # recursive get all nodes
        nodes = []
        if not pnode:
            pnode = self.root
        for snode in pnode.get_son():
            nodes.append((pnode, snode))
        if pnode.get_son():
            # if exist son, it is not a leaf
            for snode in pnode.get_son():
                nodes += self.get_all_nodes(snode)
        return nodes

    ## ukkonen part
    def split_branch(self, node, letter):
        # split a given node with activate point and add a new node with letter
        last_pos = self.get_last_pos()
        pnode = node.get_parent()
        new_son_text = node.text[last_pos:]
        print("original relation:")
        print('%s--%s ====>' % (pnode.text, node.text))
        node.change_text(node.text[:last_pos])
        node.add_son(Node(new_son_text))
        node.add_son(Node(letter))
        print("split into")
        print('==> %s--[%s--[%s,%s]]' % (pnode.text, node.text, new_son_text, letter))
        return node

    def active_point_return_node(self, checked_letter):
        current_parent_node = self.get_current_pnode()
        existed_string = self.get_active_edge()
        last_pos = self.get_last_pos()
        if existed_string:
            removed_short_nodes = [son
                                   for son in current_parent_node.get_son()
                                   if len(son.text) > last_pos]
            if not removed_short_nodes:
                check_nodes = current_parent_node
            else:
                if not current_parent_node.text:
                    # current_parent_node is root
                    check_nodes = [son
                                   for son in removed_short_nodes
                                   if checked_letter[:-1] == son.text[:last_pos]]
                    if check_nodes:
                        check_nodes = check_nodes[0]
                    else:
                        check_nodes = current_parent_node
                else:
                    parent_nodes_pos = checked_letter.rindex(current_parent_node.text)
                    parent_nodes_pos_right = parent_nodes_pos + len(current_parent_node.text)
                    # check if is a node which contains checked_letter
                    check_nodes = [son
                                   for son in removed_short_nodes
                                   if checked_letter[parent_nodes_pos_right:-1] == son.text[:last_pos]]
                    if check_nodes:
                        check_nodes = check_nodes[0]
                    else:
                        check_nodes = current_parent_node
        else:
            check_nodes = active_point[0]
        # print 'accept: active_point to locate:',active_point,check_nodes
        return check_nodes

    def check_exist(active_point, checked_letter):
        # get former node.
        check_nodes = active_point_return_node(active_point, checked_letter)
        if not check_nodes.get_son():
            poss_check_nodes = [check_nodes.text]
        else:
            poss_check_nodes = [check_nodes.text + son.text for son in check_nodes.get_son()]
        for poss in poss_check_nodes:
            if checked_letter in generate_prefix(poss):
                return True

    def construct_suffixtree_ukkonen(self, word):


        for idx, letter in enumerate(word):

            # print letter,active_point
            remainder += 1
            if not self.root.get_son():
                self.root.add_son(Node(letter))  # init the first node.
                remainder -= 1
            else:
                all_last_node = [_node for _node in self.get_all_nodes() if not _node.get_son()]  # find all leaf nodes
                for node in all_last_node:
                    node.change_text(node.text + letter)  # expand each line.
                checked_letter = active_point[1] + letter

                if not check_exist(active_point, checked_letter):  # check current 'active_edge + letter' is a existed prefix or not?
                    splited_node = []
                    while remainder > 1:
                        print('implictly', remainder, active_point, letter)
                        # node = self.prefix_to_locate(active_point[1])
                        added_node = active_point_return_node(active_point, checked_letter)
                        node_sp = split_merge(active_point, added_node, letter)
                        remainder -= 1
                        if active_point[0] == self.root and not active_point[0].suffix_link:
                            active_point[0] = self.root
                            active_point[2] -= 1
                        elif active_point[0] != self.root and not active_point[0].suffix_link:
                            active_point[0] = self.root
                        else:
                            active_point[0] = active_point[0].suffix_link

                        active_point[1] = checked_letter[1:]
                        checked_letter = checked_letter[1:]
                        # new_idx_for_node = active_point_return_node(active_point)

                        if splited_node:
                            splited_node[-1].link_suffix(node_sp)
                        splited_node.append(node_sp)

                    active_point[0].add_son(Node(letter))  # add new branch in root
                    # active_point[2] -= 1
                    if remainder == 1:
                        active_point = [self.root, '', 0]
                        remainder -= 1

                else:
                    print('find existed word')
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
