from lab2.distance_measure.algorithms import jaro_winkler_distance
from lab2.distance_measure.algorithms import hamming_distance
from lab2.distance_measure.algorithms import levenshtein_distance

if __name__ == '__main__':
    s1 = "hello"
    s2 = "haloa"

    print(hamming_distance(s1, s2))
    print(levenshtein_distance(s1, s2))
    print(jaro_winkler_distance(s1, s2))
