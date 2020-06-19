import os
import string
from collections import Counter

import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def get_accurate_words(text: string):
    """
    Clear the text by:
    1) splitting text in tokens by spaces
    2) removal of punctuation
    3) making all chars lowercase
    4) removal of non-alphabetic tokens
    5) removal of stop-words
    :param text: text with lemmatized words
    :return: list of normalized words
    """
    tokens = word_tokenize(text)  # split into words
    tokens = [w.lower() for w in tokens]  # convert to lower case
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [w for w in tokens if w.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]
    return words


def create_dictionary(filename: string):
    """
    Create dictionary with counts of each lemma (suppose that document is already lemmatized)
    :param filename: document filename in relative or absolute path notation
    :return: Counter obj
    """
    with open(filename, 'rt') as doc:
        for line_num, text in enumerate(doc):
            if line_num == 2:
                words = get_accurate_words(text)
                return Counter(words)


def create_dictionary_dir(dir_name: string, words_limit: int = 5000):
    """
    Create dictionary from docs in specified directory name
    :param dir_name: where is all docs are located (not recursive)
    :param words_limit: max amount of words in dictionary
    :return: Counter obj
    """
    filenames = [os.path.join(dir_name, f) for f in os.listdir(dir_name)]
    res = Counter()
    for f in filenames:
        res += create_dictionary(f)
    return res.most_common(words_limit)


def create_dictionary_indexes(dictionary):
    """
    Util method to retrieve consistent wordId by word
    :param dictionary: dictionary of words
    :return: dictionary of word:wordId entries
    """
    indexes_d = {}
    word_id = 0
    for w, _ in dictionary:
        if w not in indexes_d:
            indexes_d[w] = word_id
            word_id += 1
    return indexes_d


def extract_feature(dir_name: string):
    """
    :param dir_name: directory where all docs are located
    :return: Create feature matrix, where row is a doc and a column is a word. Value is occurrences
    counter in the specified doc.
    """
    filenames = [os.path.join(dir_name, f) for f in os.listdir(dir_name)]
    dictionary = create_dictionary_dir(dir_name)
    dictionary_indexes = create_dictionary_indexes(dictionary)
    features_matrix = np.zeros((len(filenames), len(dictionary)))

    doc_id = 0  # for indexing in np.array
    for f in filenames:
        doc_dictionary = create_dictionary(f)
        for w, c in doc_dictionary.items():
            if w in dictionary:
                features_matrix[doc_id, dictionary_indexes[w]] = c
        doc_id += 1
    return features_matrix


if __name__ == '__main__':
    print(extract_feature('mails/test'))
    pass
