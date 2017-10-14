
def generate_suffix(text,sign=''):
    suffixs = []
    for _i in range(len(text)):
        if _i == 0:
            suffixs.append(text)
        else:
            suffixs.append(text[_i:])
    if not sign:
        return suffixs
    else:
        return suffixs+[sign]

def generate_prefix(text,sign=''):
    prefixs = []
    for _i in range(len(text)):
        if _i == len(text)-1:
            prefixs.append(text[:_i])
            prefixs.append(text)
        else:
            prefixs.append(text[:_i])
    if not sign:
        return prefixs
    else:
        return prefixs+[sign]

if __name__ == '__main__':
    assert generate_suffix('banana') == ['banana', 'anana', 'nana', 'ana', 'na', 'a']
    assert generate_prefix('banana') == ['', 'b', 'ba', 'ban', 'bana', 'banan','banana']