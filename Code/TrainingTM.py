# Sam Gass
# scg0040
# Computational Biology
# Project 5
# python3 coded in Microsoft Visual Studio Code on Windows 10
# Last Modified: April 15, 2020
#
# This python code creates a model for TM prediction and stores it in the TMmodel.pkl file

from os import listdir
from random import shuffle
from random import choice
from pickle import Pickler
from pickle import load
from PredictSS import fileToMatrix
from PredictSS import predict as predictSS
from PredictSS import openModel as openSSmodel
from PredictRSA import fileToList
from PredictRSA import predict as predictSA
from PredictRSA import openModel as openSAmodel
from PredictRSA import Node

# ------------------------------------------------------------------------


class Pair:
    def __init__(self, name1, name2, SSmodel, SAmodel, isTraining):
        pssm1 = self.getPSSM(name1)
        pssm2 = self.getPSSM(name2)

        matrix1 = fileToMatrix(".\\pssm\\" + name1 + ".pssm")
        matrix2 = fileToMatrix(".\\pssm\\" + name2 + ".pssm")

        ss1 = self.getSS(matrix1, SSmodel)
        ss2 = self.getSS(matrix2, SSmodel)

        attributes1 = fileToList(".\\fasta\\" + name1 + ".fasta")
        attributes2 = fileToList(".\\fasta\\" + name2 + ".fasta")

        sa1 = self.getSA(attributes1, SAmodel)
        sa2 = self.getSA(attributes2, SAmodel)

        self.features = self.getFeatures(pssm1, pssm2, ss1, ss2, sa1, sa2)

        if (isTraining):
            tm = self.getTM(name1, name2)
            self.label = tm
        else:
            self.label = None

    def getPSSM(self, filename):
        path = '.\\pssm\\' + filename + '.pssm'
        with open(path, 'r') as pssmFile:
            lines = pssmFile.readlines()
        for i in range(3):
            lines.pop(0)
        for i in range(6):
            lines.pop(-1)
        for i in range(len(lines)):
            lines[i] = lines[i].split()

        avgFeatures = [0] * 20
        for line in lines:
            for i in range(22, 42):
                avgFeatures[i - 22] += int(line[i])

        length = len(lines)
        for i in range(len(avgFeatures)):
            avgFeatures[i] /= (length * 100)

        return tuple(avgFeatures)

    def getSS(self, matrix, model):
        h, e, c = predictSS(model['y'], model['m'], model['s'], matrix)
        return (h, e, c)

    def getSA(self, attributes, model):
        e, b = predictSA(model, attributes)
        return (e, b)

    def getTM(self, name1, name2):
        with open(".\\tmalign\\" + name1 + '_' + name2 + '_tmalign') as tmFile:
            lines = tmFile.readlines()
        line1 = lines[17].split()
        line2 = lines[18].split()

        tm1 = float(line1[1])
        tm2 = float(line2[1])

        return ((tm1 + tm2) / 2)

    def getFeatures(self, pssm1, pssm2, ss1, ss2, sa1, sa2):
        return pssm1 + pssm2 + ss1 + ss2 + sa1 + sa2

# ------------------------------------------------------------------------


def getData():
    path = ".\\tmalign"
    filenames = listdir(path)

    SSmodel = openSSmodel('SSmodel.pkl')
    SAmodel = openSAmodel('SAmodel.pkl')

    pairs = []
    duplicates = []
    for name in filenames:
        pair = name.split('_')
        if ((pair[1], pair[0])) not in duplicates:
            pairs.append(Pair(pair[0], pair[1], SSmodel, SAmodel, True))
            duplicates.append((pair[0], pair[1]))

    return pairs


def splitData(data, percent):
    shuffle(data)
    data1 = list(data)
    data2 = []
    length = percent * len(data1)
    while length > 0:
        data2.append(data1.pop())
        length -= 1
    return data1, data2

# ------------------------------------------------------------------------


def gradientDescent(data, step, maxIterations):
    change0 = float('inf')
    change1 = float('inf')
    w0 = 0
    w1 = 0
    iterations = 0
    while iterations < maxIterations:
        d = choice(data)
        prediction = w0
        for x in d.features:
            prediction += (w1 * x)
        linear = d.label - prediction

        change0 = 2 * step * linear

        change1 = 0
        for x in d.features:
            change1 += (x * linear)
        change1 = 2 * step * change1

        w0 = w0 + change0
        w1 = w1 + change1
        iterations += 1

    print("iterations:", iterations)
    return w0, w1

# ------------------------------------------------------------------------


def pickleModel(modelname, w0, w1):
    with open(modelname, "wb") as f:
        p = Pickler(f)
        p.dump(w0)
        p.dump(w1)


# ------------------------------------------------------------------------

def testModel(data, w0, w1):
    avgSquareError = 0
    for d in data:
        prediction = w0
        for x in d.features:
            prediction += (w1 * x)

        avgSquareError += (d.label - prediction)**2

    avgSquareError /= len(data)

    print("Average Square Error of Model:", avgSquareError)

# ------------------------------------------------------------------------


if __name__ == "__main__":
    dataSet = getData()
    percent = 0.25
    trainingData, testingData = splitData(dataSet, percent)

    step = 0.001
    maxIterations = 8192
    w0, w1 = gradientDescent(trainingData, step, maxIterations)

    modelname = "TMmodel.pkl"
    pickleModel(modelname, w0, w1)

    testModel(testingData, w0, w1)
