

def bw_t(word):
    word = '$' + word
    words = []
    for i in xrange(len(word),0,-1):
        words.append(word[i:] + word[:i])
    words = sorted(words)
    output_bw = ''.join([bw_word[-1] for bw_word in words])
    return output_bw


def re_bwt(word):
    table = [''] * len(word)
    for _ in word:
        table = sorted([word[m] + table[m] for m in range(len(word))])
        print table
    s = [row for row in table if row.endswith('$')][0]
    return s.rstrip('$')
