from typing import List
from scipy.cluster.hierarchy import dendrogram, ward
import matplotlib.pyplot as plt

from lab2.distance_measure.algorithms import levenshtein_distance
from lab2.distance_measure.algorithms import levenshtein_distance_efficient

import nltk


def tokenize(text):
    """
    Convert text in the set of tokens using custom tokenizer
    Explanation: The RegExp is made up of 3 alternatives:
        [A-Z]{2,}(?![a-z]) matches words with all letters capital
        [A-Z][a-z]+(?=[A-Z]) matches words with a first captitel letter. The lookahead (?=[A-Z]) stops the match before the next capital letter
        [\'\w\-]+ matches all the rest, i.e. words which may contain ' and -
    """
    pattern = "[A-ZА-Я]{2,}(?![a-zа-я])|[A-ZА-Я][a-zа-я]+(?=[A-ZА-Я])|[\'\w\-]+"
    return nltk.regexp_tokenize(text, pattern)


def clusterize(tokens: List[str], dist_func, graph_out):
    sim_l = []
    sim_matrix = []
    label_l = tokens[:]
    words_l = tokens[:]
    words_size = len(words_l)
    for i in range(0, words_size):
        pivot = words_l[i]
        for j in range(0, words_size):
            sim = dist_func(pivot, words_l[j])  # calculate similarity(distance)
            print('n{}, n{} : {}'.format(i, j, sim))
            sim_l.append(sim)
            if j == words_size - 1:
                sim_matrix.append(sim_l)
                sim_l = []

    print('-------------------------')
    print('matrix: {}'.format(sim_matrix))
    linkage_matrix = ward(sim_matrix)
    print('--------------------------')
    print(linkage_matrix)
    dendrogram(linkage_matrix, labels=label_l, orientation='right', leaf_font_size=7)
    plt.figure(figsize=(100, 100))
    plt.savefig(graph_out)


if __name__ == '__main__':
    filename_in = "sample_cool.txt"
    dendogram_out = "graph.png"

    with open(filename_in, mode='r') as f:
        text = f.read()
    tokens_l = list(set(tokenize(text)[:]))

    clusterize(tokens_l, levenshtein_distance_efficient, dendogram_out)
