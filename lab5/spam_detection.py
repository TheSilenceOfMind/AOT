import os
import string
from collections import Counter

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


if __name__ == '__main__':
    print(create_dictionary_dir('mails/train'))
    pass
