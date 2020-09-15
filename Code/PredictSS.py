from pickle import load
from sys import argv
from sys import exit
from math import exp
from math import sqrt
from math import pi


def openModel(modelname):
    try:
        with open(modelname, 'rb') as f:
            y = load(f)
            m = load(f)
            s = load(f)
    except:
        print("Error opening model. Model must be a pkl file for SS classification.")
        exit()

    return {'y': y, 'm': m, 's': s}


def fileToMatrix(filename):
    features = []
    try:
        with open(filename, 'r') as pssmFile:
            lines = pssmFile.readlines()
            for i in range(3):
                lines.pop(0)
            for i in range(6):
                lines.pop(-1)
            for i in range(len(lines)):
                lines[i] = lines[i].split()
    except:
        print("Error reading file. File must be a pssm for SS classification.")
        exit()

    empty = [-1] * 20
    for i in range(len(lines)):
        row = []
        if i - 2 < 0:
            row += empty
        else:
            for j in range(2, 22):
                row.append(int(lines[i-2][j]))
        if i - 1 < 0:
            row += empty
        else:
            for j in range(2, 22):
                row.append(int(lines[i-1][j]))
        for j in range(2, 22):
            row.append(int(lines[i][j]))
        if i + 1 >= len(lines):
            row += empty
        else:
            for j in range(2, 22):
                row.append(int(lines[i+1][j]))
        if i + 2 >= len(lines):
            row += empty
        else:
            for j in range(2, 22):
                row.append(int(lines[i+2][j]))
        features.append(tuple(row))
    return tuple(features)


def gaussian(x, u, s):
    c = sqrt(2 * pi * s)
    c = 1/c
    e = exp(-((x - u)**2 / (2 * s)))
    return (c * e)


def predict(y, m, s, seq):
    h = 0
    e = 0
    c = 0
    for x in seq:
        argMax = [0, 0, 0]
        pick = 0
        for k in range(0, 3):
            product = 1
            for i in range(0, 100):
                product *= gaussian(x[i], m[k][i], s[k][i])
            argMax[k] = (y[k] * product)
        pick = argMax.index(max(argMax))
        if pick == 0:
            h += 1
        elif pick == 1:
            e += 1
        elif pick == 2:
            c += 1

    length = len(seq)
    h /= length
    e /= length
    c /= length

    return h, e, c
