import pickle
import sys
from copy import copy

#   Node class to create binary tree that will be the model. The
#   true branch is the right branch, and false branch the left.
#   attribute is the data it holds. If it is a leaf node, leaf
#   will be true. If it is a leaf node label will be set to E or
#   B for wheter or not it is exposed or buried.


class Node:
    def __init__(self, attribute=None, label=None, leaf=False):
        self.trueBranch = None
        self.falseBranch = None
        self.attribute = attribute
        self.label = label
        self.leaf = leaf


#   Dictionary for the table for each amino acid and their attributes. Order of attributes:
#   Hydrophobic / Polar / Positive / Negative / Charged / Small / Tiny / Aromatic / Aliphatic / Proline
table = {
    'A': [True, False, False, False, False, True, True, False, False, False],
    'C': [True, False, False, False, False, True, False, False, False, False],
    'D': [False, True, False, True, True, True, False, False, False, False],
    'E': [False, True, False, True, True, False, False, False, False, False],
    'F': [True, False, False, False, False, False, False, True, False, False],
    'G': [True, False, False, False, False, True, True, False, False, False],
    'H': [False, True, True, False, True, False, False, True, False, False],
    'I': [True, False, False, False, False, False, False, False, True, False],
    'K': [False, True, True, False, True, False, False, False, False, False],
    'L': [True, False, False, False, False, False, False, False, True, False],
    'M': [True, False, False, False, False, False, False, False, False, False],
    'N': [False, True, False, False, False, True, False, False, False, False],
    'P': [True, False, False, False, False, True, False, False, False, True],
    'Q': [False, True, False, False, False, False, False, False, False, False],
    'R': [False, True, True, False, True, False, False, False, False, False],
    'S': [False, True, False, False, False, True, True, False, False, False],
    'T': [True, True, False, False, False, True, False, False, False, False],
    'V': [True, False, False, False, False, True, False, False, True, False],
    'W': [True, False, False, False, False, False, False, True, False, False],
    'Y': [True, True, False, False, False, False, False, True, False, False]
}

#   takes the path to a pickle file and returns the root node to the binary tree inside.


def openModel(modelname):
    with open(modelname, 'rb') as f:
        return pickle.load(f)

#   converts fasta file to a list of tuples.


def fileToList(filename):
    seqList = []
    try:
        with open(filename, 'r') as fastaFile:
            for line in fastaFile:
                for c in line:
                    if c == '>':
                        break
                    if c == '\n':
                        continue
                    seqList.append(c)
    except FileNotFoundError:
        return "file not found"

    attrList = []
    for amino in seqList:
        a = tuple(table[amino])
        attrList.append(a)

    return attrList

#   creates an sa file, filename_prediction.sa, with
#   the decision trees prediction for buried/exposed


def predict(model, seq):
    e = 0
    b = 0
    for amino in seq:
        m = copy(model)
        while not m.leaf:
            if amino[m.attribute]:
                m = m.trueBranch
            else:
                m = m.falseBranch
        if (m.label == 'E'):
            e += 1
        else:
            b += 1

    length = len(seq)
    e /= length
    b /= length
    return e, b
