import math
import textwrap

import numpy as np
import pandas
import pymorphy2
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from scipy.cluster.hierarchy import dendrogram, linkage

from lab2.tokenizer.tokenizer import tokenize


# retrieving of vectors
def get_vector(words, word_matrix, word):
    for y, x in enumerate(words):
        if x == word:
            return word_matrix[y]
    return 0


# functions-metrics
def div_kl(p, q):
    ans = 0
    for i in range(len(p)):
        if p[i] != 0 and q[i] != 0:
            ans += p[i] * math.log(p[i] / q[i])
    return ans


def div_gs(p, q):
    c = []
    for i in range(len(p)):
        c.append((p[i] + q[i]) / 2)
    return div_kl(p, c) + div_kl(q, c)


def jacard(v1, v2):
    x, y = 0, 0
    for i in range(len(v1)):
        x += min(v1[i], v2[i])
        y += max(v1[i], v2[i])
    return x / y


def cosine_similarity(v1, v2):
    sxx, sxy, syy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sxx += x * x
        syy += y * y
        sxy += x * y
    return sxy / math.sqrt(sxx * syy)


morph_analyzer = pymorphy2.MorphAnalyzer()

stop_words = stopwords.words('english')
n = 10  # number of docs
ws = 7  # word span (aka width of context)

d_matrix = []
words_set = []
words_frequencies_dictionary = {}

# building of word-context matrix
for ind in range(1, n + 1):
    sum_w = 0
    print("processing document text_{id}.txt ...".format(id=ind))
    with open("documents/text_{id}.txt".format(id=ind), encoding='utf-8') as f:
        for line in f:
            tokens_from_line = tokenize(line.strip())
            tokens_from_line = [i for i in tokens_from_line if i not in stop_words]
            sum_w += len(tokens_from_line)
            words = [morph_analyzer.parse(word)[0].normal_form for word in tokens_from_line]

            for token in set(words):
                if token not in words_set:
                    words_set.append(token)
                    words_frequencies_dictionary[token] = 0
                    d_matrix.append([0] * len(d_matrix))
                    for i in range(len(d_matrix)):
                        d_matrix[i].append(0)

            for word in words:
                words_frequencies_dictionary[word] += 1

            for i in range(len(words_set)):
                for token_number in [y for y, x in enumerate(words) if x == words_set[i]]:
                    for j in range(len(words_set)):
                        for k in range(token_number - ws, token_number + ws + 1):
                            if k < 0:
                                continue
                            if k > len(words) - 1:
                                continue
                            if words[k] == words_set[j]:
                                d_matrix[j][i] += 1

for word in words_set:
    words_frequencies_dictionary[word] /= sum_w

# building PPMI model
d2_ppmi = [[0] * len(words_set) for _ in range(len(words_set))]

for i in range(len(words_set)):
    for j in range(len(words_set)):
        if d_matrix[i][j] == 0:
            d2_ppmi[i][j] = 0
        else:
            d2_ppmi[i][j] = math.log(
                (d_matrix[i][j] / sum(d_matrix[i])) / (words_frequencies_dictionary[words_set[i]] *
                                                       words_frequencies_dictionary[words_set[j]]))
        if d2_ppmi[i][j] < 0:
            d2_ppmi[i][j] = 0

# define test set; these words are from wordsim353
test_list = ['planet', 'sun', 'opera', 'industry', 'money', 'cash', 'bank',
             'credit', 'card', 'information', 'computer',
             'internet', 'software', 'professor', 'cucumber', 'doctor']


# get words as vectors for testing and definition value-matrix for clusterization
def get_d(coord, word):
    i, j = coord
    v1 = get_vector(words_set, d2_ppmi, word[i])
    v2 = get_vector(words_set, d2_ppmi, word[j])
    return jacard(v1, v2)


tri = np.triu_indices(len(test_list), 1)
weights = np.apply_along_axis(get_d, 0, tri, test_list)

# Hierarchical clusterization
linkage_result = linkage(weights, 'ward')
dend = dendrogram(linkage_result, labels=np.array(test_list), leaf_rotation=90, leaf_font_size=10)
fig = plt.figure(figsize=(10, 5))

# Test sets for wordsim and experiment are different which causes
# some deviation (along with almost positive correlation).
# We chose 5 different texts with different tematics.
#
# Results are represented in file "main.out"
# Clusterization result are represented in "dendogram.png"
filename = "documents/wordsim353crowd.csv"
wordsim353 = pandas.read_csv(filename)

dict_test_word = {}
for word in test_list:
    dict_test_word[word] = get_vector(words_set, d_matrix, word)


def pretty_print(prefix_msg: str, message: str):
    prefix = prefix_msg + ": "
    prefix_width = 80
    wrapper = textwrap.TextWrapper(initial_indent=prefix, width=prefix_width,
                                   subsequent_indent=' ' * (prefix_width // 4))
    print(wrapper.fill(message))


def process(num: int, w1: str, w2: str, w_order: str):
    print('=' * 80)
    pretty_print(prefix_msg='pair {i}'.format(i=num),
                 message='{w1} , {w2}'.format(i=num, w1=w1, w2=w2))
    pretty_print(prefix_msg="KL div",
                 message=str(div_kl(dict_test_word[w1], dict_test_word[w2])))
    pretty_print(prefix_msg="GS div",
                 message=str(div_gs(dict_test_word[w1], dict_test_word[w2])))
    pretty_print(prefix_msg="Jacard",
                 message=str(jacard(dict_test_word[w1], dict_test_word[w2])))
    pretty_print(prefix_msg="Cosine",
                 message=str(cosine_similarity(dict_test_word[w1], dict_test_word[w2])))
    print()
    if w_order == 'Word 1':
        print(wordsim353[wordsim353[w_order] == w1], '\n')
    elif w_order == 'Word 2':
        print(wordsim353[wordsim353[w_order] == w2], '\n')


process(0, 'opera', 'industry', 'Word 2')
process(1, 'bank', 'money', 'Word 1')
process(2, 'computer', 'internet', 'Word 1')
process(3, 'computer', 'software', 'Word 2')
process(4, 'professor', 'doctor', 'Word 1')

plt.show()
