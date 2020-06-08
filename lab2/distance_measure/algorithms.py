import math


def hamming_distance(s1, s2) -> int:
    """Return the Hamming distance between equal-length sequences."""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length.")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


def levenshtein_distance(s, t):
    """Tremendously ineffective: computation complexity is 2^(|s|+|t|)"""
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1

    res = min([levenshtein_distance(s[:-1], t) + 1,
               levenshtein_distance(s, t[:-1]) + 1,
               levenshtein_distance(s[:-1], t[:-1]) + cost])

    return res


def levenshtein_distance_efficient(s, t):
    s_len = len(s)
    t_len = len(t)
    D = [[0] * (t_len + 1) for i in range(s_len + 1)]
    for i in range(s_len + 1):
        D[i][0] = i
    for j in range(t_len + 1):
        D[0][j] = j
    for i in range(1, s_len + 1):
        for j in range(1, t_len + 1):
            c = 0 if s[i - 1] == t[j - 1] else 1
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + c)
    return D[s_len][t_len]


def jaro_winkler_distance(first, second, winkler=True, winkler_ajustment=True, scaling=0.1):
    jaro = _score(first, second)
    cl = min(len(_get_prefix(first, second)), 4)

    if all([winkler, winkler_ajustment]):  # 0.1 as scaling factor
        return round((jaro + (scaling * cl * (1.0 - jaro))) * 100.0) / 100.0

    return jaro


def _score(first, second):
    shorter, longer = first.lower(), second.lower()

    if len(first) > len(second):
        longer, shorter = shorter, longer

    m1 = _get_matching_characters(shorter, longer)
    m2 = _get_matching_characters(longer, shorter)

    if len(m1) == 0 or len(m2) == 0:
        return 0.0

    return (float(len(m1)) / len(shorter) +
            float(len(m2)) / len(longer) +
            float(len(m1) - _transpositions(m1, m2)) / len(m1)) / 3.0


def _get_diff_index(first, second):
    if first == second:
        return -1
    if not first or not second:
        return 0
    max_len = min(len(first), len(second))
    for i in range(0, max_len):
        if not first[i] == second[i]:
            return i
    return max_len


def _get_prefix(first, second):
    if not first or not second:
        return ""
    index = _get_diff_index(first, second)
    if index == -1:
        return first
    elif index == 0:
        return ""
    else:
        return first[0:index]


def _get_matching_characters(first, second):
    common = []
    limit = math.floor(min(len(first), len(second)) / 2)
    for i, l in enumerate(first):
        left, right = int(max(0, i - limit)), int(min(i + limit + 1, len(second)))
        if l in second[left:right]:
            common.append(l)
            second = second[0:second.index(l)] + '*' + second[second.index(l) + 1:]
    return ''.join(common)


def _transpositions(first, second):
    return math.floor(len([(f, s) for f, s in zip(first, second) if not f == s]) / 2.0)
