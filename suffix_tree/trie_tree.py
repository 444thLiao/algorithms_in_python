# from generate_suffix import generate_prefix,generate_suffix
from collections import Counter
class Node(object):
    def __init__(self,text):
        self.text = text
        self.son = []
        self.parent = ''
        #self.count = 0
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
            raise IOError,'Wrong compare.'
    def add_son(self,node):
        self.son.append(node)
        node.add_parent(self)
    def add_parent(self,node):
        self.parent = node
    def drop_son(self,node):
        if node in self.son:
            self.son.remove(node)
    def get_son(self):
        return self.son
    def get_parent(self):
        return self.parent
    def change_text(self,new_text):
        self.text = new_text


class dict_tree(object):
    def __init__(self,root):
        self.root = root
        self.compressed = False
        #self.nodes = []
    def get_all_nodes(self,pnode=''):
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
    def construct_from_words(self,words):
        for word in words:
            for idx,letter in enumerate(word):
                if idx == 0:
                    parent_node_text = ''
                    current_node = Node(letter)
                else:
                    parent_node_text = word[:idx]
                    current_node = Node(letter)
                #print 'add s.%s into p.%s' % (letter,word[idx-1])
                self.add_son(current_node,parent_node_text)

    def add_son(self,s_node,p_node_text = ''):
        if not p_node_text:
            if s_node not in self.root.get_son():
                #self.nodes.append(s_node)
                p_node = self.root
                p_node.add_son(s_node)
        else:
            p_node = self.get_last_node(p_node_text)

            if s_node not in p_node.get_son():
                p_node.add_son(s_node)

    def get_last_node(self,lineage_text):
        current_parent = self.root
        if lineage_text == '':
            return current_parent
        while len(lineage_text) > 1:
            sons = current_parent.get_son()
            current_parent = None
            all_prefix_letters = generate_prefix(lineage_text,' ')[1:]
            for letter in all_prefix_letters:
                if letter in sons:
                    current_parent = [son for son in sons if son == letter][0]
                    lineage_text = lineage_text[len(letter):]
                    break
            if not current_parent:
                import pdb;pdb.set_trace()
                raise IOError,'Wrong lineage.'

        #import pdb;pdb.set_trace()
        if current_parent.get_son() and len(lineage_text) != 0:
            if Node(lineage_text) not in current_parent.get_son():
                raise IOError, 'Wrong lineage.'
            current_node = [son for son in current_parent.get_son() if son == Node(lineage_text)][0]
            return current_node
        elif len(lineage_text) == 0:
            return current_parent

    def get_all_aft_words(self,lineage_text):
        try:
            last_node = self.get_last_node(lineage_text)
            all_sons = []

            if last_node.get_son():
                all_new_lineage_text = [lineage_text+node.text for node in last_node.get_son()]
                for lineage in all_new_lineage_text:
                    all_sons+=self.get_all_aft_words(lineage)
                    #print all_sons,lineage
            else:
                return [lineage_text]
            return all_sons
        except:
            import pdb;pdb.set_trace()

    def get_node_lineage(self,lineage_text):
        if lineage_text == '':
            return '<Root>'
        else:
            if not self.compressed :
                prefixs = generate_prefix(lineage_text)
                # try:
                return [self.get_last_node(node) for node in prefixs[:]]
                # except:
                #     import pdb;pdb.set_trace()
            else:
                parent_node = self.root
                lineage = []
                lineage.append('<Root>')
                while 1:
                    next_node = None
                    all_prefixs = generate_prefix(lineage_text)[1:]
                    for poss_pre in all_prefixs:
                        if poss_pre in parent_node.get_son():
                            next_node = [son for son in parent_node.get_son() if son == poss_pre][0]
                            lineage.append(next_node)
                            break
                    if not next_node:
                        raise IOError, "The lineage doesn't exist in sons of root."
                    lineage_text = lineage_text[len(poss_pre):]
                    if not lineage_text:
                        break
                    else:
                        parent_node = lineage[-1]
            return lineage
    def compressed_one(self,node):
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




if __name__=='__main__':
    # root = Node('')
    # trie = dict_tree(root)
    #
    #
    # trie.construct_from_words(['bear','bell','knowledges','bid','buy','bus','bug','busy','because'])
    # trie.compressed_self()
    # trie.get_all_nodes()
    #
    #
    #
    # test_word = 'banana#'
    # test_word_suffixs = generate_suffix(test_word)
    # trie.construct_from_words(test_word_suffixs)
    # trie.compressed_self()
    # #trie.get_all_nodes()
    # #trie.get_node_lineage('nana#')
    # for word in trie.get_all_aft_words(''):
    #     trie.get_node_lineage(word)

    root = Node('')
    trie = dict_tree(root)
    test_word = 'xabxa$'
    test_word_suffixs = generate_suffix(test_word)
    trie.construct_from_words(test_word_suffixs)
    trie.compressed_self()
    #trie.get_all_nodes()
    for word in trie.get_all_aft_words(''):
        print trie.get_node_lineage(word)