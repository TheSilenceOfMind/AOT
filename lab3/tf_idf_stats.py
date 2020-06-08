from os import listdir
from os.path import isfile, join

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from lab2.tokenizer.tokenizer import tokenize
from nltk.corpus import stopwords

corpus_stopwords = stopwords.words('english')


def get_occurrence_dict(unique_words, tokens):
    d = dict.fromkeys(unique_words, 0)
    for word in tokens:
        d[word] += 1
    return d


def compute_tf(some_dict, bag_of_words):
    td_dict = {}
    bow_count = len(bag_of_words)
    for word, count in some_dict.items():
        td_dict[word] = count / float(bow_count)
    return td_dict


def compute_idf(num_of_words_d):
    import math
    n = len(num_of_words_d)

    idf_dict = dict.fromkeys(num_of_words_d[0].keys(), 0.)
    for document in num_of_words_d:
        for word, val in document.items():
            if val > 0:
                idf_dict[word] += 1

    for word, val in idf_dict.items():
        idf_dict[word] = math.log(n / float(val))
    return idf_dict


def compute_tf_idf(tf_bow, idfs):
    tf_idf = {}
    for word, val in tf_bow.items():
        tf_idf[word] = val * idfs[word]
    return tf_idf


def get_docs(filename_prefix, dir_path='./samples/'):
    ret_docs = {}
    files = [f for f in listdir(dir_path) if
             isfile(join(dir_path, f))
             and f.startswith(filename_prefix)]
    for f in files:
        with open(join(dir_path, f), 'rt') as fr:
            ret_docs[join(dir_path, f)] = fr.read()
    return ret_docs


def process_docs_manual(filename_prefix):
    docs = get_docs(filename_prefix)
    bows = {}
    tfs = {}
    tf_idf = {}
    num_of_words = {}
    unique_words = set()
    for k, v in docs.items():
        bows[k] = tokenize(v)
        unique_words = unique_words.union(set(bows[k]))

    #  for now we've formed a set of unique_words
    for k, v in docs.items():
        num_of_words[k] = get_occurrence_dict(unique_words, bows[k])
        tfs[k] = compute_tf(num_of_words[k], bows[k])

    idfs = compute_idf(list(num_of_words.values()))
    for k, v in docs.items():
        tf_idf[k] = compute_tf_idf(tfs[k], idfs)
    df = pd.DataFrame(list(tf_idf.values()),
                      index=list(tf_idf.keys()))
    print(df.sort_index())
    pass


def process_docs_using_sklearn(filename_prefix):
    pass


process_docs_manual('doc_')

# documentA = 'the man went out for a walk'
# documentB = 'the children sat around the fire'
#
# bow_a = tokenize(documentA)
# bow_b = tokenize(documentB)
# unique_words = set(bow_a).union(set(bow_b))
#
# num_of_words_a = get_occurrence_dict(unique_words, bow_a)
# num_of_words_b = get_occurrence_dict(unique_words, bow_b)
#
# tf_a = compute_tf(num_of_words_a, bow_a)
# tf_b = compute_tf(num_of_words_b, bow_b)
# print(tf_a)
# print(tf_b)
#
# idfs = compute_idf([num_of_words_a, num_of_words_b])
# print(idfs)
#
# tf_idf_a = compute_tf_idf(tf_a, idfs)
# tf_idf_b = compute_tf_idf(tf_b, idfs)
#
# df = pd.DataFrame([tf_idf_a, tf_idf_b])
