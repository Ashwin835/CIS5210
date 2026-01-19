import numpy as np
import nltk
from string import punctuation

############################################################
# CIS 521: Homework 1
############################################################

student_name = "Ashwin Verma"

# This is where your grade report will be sent.
student_email = "vashwin@seas.upenn.edu"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Python is strongly typed because it enforces type constraints at
runtime. Operations between incompatible types will raise errors, for
example: "5" + 5  # Raises TypeError.

Python is also dynamically typed: variable types are determined at
runtime rather than at compile time. For example, `x = 10` then
`x = "10"` changes `x` from an int to a str at runtime.
"""

python_concepts_question_2 = """
Lists are mutable and therefore not hashable; they cannot be used as
dictionary keys. Convert lists to tuples to use them as keys.
"""

python_concepts_question_3 = """
Using `result += s` inside a loop is inefficient because it creates a
new string on each concatenation. Using `"".join(...)` is O(n) and
more efficient than repeated concatenation, which can be O(n^2).
"""

############################################################
# Section 2: Working with Lists
############################################################


def extract_and_apply(lst, p, f):
    return [f(x) for x in lst if p(x)]


def concatenate(seqs):
    return [x for seq in seqs for x in seq]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

############################################################
# Section 3: Sequence Slicing
############################################################


def copy(seq):
    return seq[:]


def all_but_last(seq):
    if seq == []:
        return []
    if seq == "":
        return ""
    return seq[:-1]


def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################


def prefixes(seq):
    yield [] if isinstance(seq, list) else ""

    for i in range(len(seq)):
        yield seq[:i + 1]


def suffixes(seq):
    for i in range(len(seq)+1):
        yield seq[i:]


def slices(seq):
    for i in range(len(seq)):
        for j in range(i + 1, len(seq) + 1):
            yield seq[i:j]

############################################################
# Section 5: Text Processing
############################################################


def normalize(text):
    words = text.split()

    text = " ".join([word.lower() for word in words])
    return text


def no_vowels(text):
    new_text = ""
    vowels = [
        'a', 'e', 'i', 'o', 'u',
        'A', 'E', 'I', 'O', 'U',
    ]

    [new_text := new_text + char for char in text if char not in vowels]
    return new_text


def digits_to_words(text):
    digit_map = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
    }

    words = [digit_map[char] for char in text if char in digit_map]
    if len(words) == 0:
        return ""

    return " ".join(words)


def to_mixed_case(name):
    words = name.split('_')
    if words == []:
        return ""

    first_word = True
    for word in words:
        if word == "":
            continue
        if first_word:
            first_word = False
            words[words.index(word)] = word.lower()
        else:
            words[words.index(word)] = word.capitalize()

    return "".join(words)

############################################################
# Section 6: Polynomials
############################################################


class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        return Polynomial([
            (-coeff, power)
            for (coeff, power) in self.polynomial
        ])

    def __add__(self, other):
        return Polynomial(self.polynomial + other.polynomial)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Polynomial([
            (c1 * c2, p1 + p2)
            for (c1, p1) in self.get_polynomial()
            for (c2, p2) in other.get_polynomial()
        ])

    def __call__(self, x):
        return sum(c * (x ** p) for c, p in self.get_polynomial())

    def simplify(self):
        combined = {}

        for c, p in self.get_polynomial():
            combined[p] = combined.get(p, 0) + c

        coefficients = [(c, p) for p, c in combined.items() if c != 0]
        if not coefficients:
            self.polynomial = ((0, 0),)
        else:
            self.polynomial = tuple(
                sorted(coefficients, key=lambda coefficient: -coefficient[1])
            )

    def __str__(self):
        s = ""

        for i, (c, p) in enumerate(self.get_polynomial()):
            if c < 0:
                sign = "-"
            else:
                sign = "+"
            if c == 0:
                sign = "+"

            c = abs(c)

            if p == 0:
                term = str(c)
            else:
                if c == 1:
                    term = "x"
                else:
                    term = str(c) + "x"
                if p != 1:
                    term += "^" + str(p)

            if i == 0:
                if sign == "-":
                    s += "-" + term
                else:
                    s += term
            else:
                s += " " + sign + " " + term

        return s


############################################################
# Section 7: Python Packages
############################################################


def sort_array(list_of_matrices):
    all_values = np.concatenate([
        m.flatten() for m in list_of_matrices
    ])

    return np.sort(all_values.astype(int))[::-1]


def POS_tag(sentence):
    sentence = sentence.lower()
    tokens = nltk.word_tokenize(sentence)

    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_tokens = [
        word for word in tokens
        if word not in stop_words and word not in punctuation
    ]

    pos_tags = nltk.pos_tag(filtered_tokens)
    return pos_tags
############################################################
# Section 8: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
I spend approximately 3 hours on this assignment
"""

feedback_question_2 = """
Coding was quite easy as I have prior experience with Python.
The text processing and polynomial sections however took some
time to understand the requirements and implement correctly.
"""

feedback_question_3 = """
Overall liked the assignment, good review of python concepts.
Wouldn't change anything majorly.
"""
