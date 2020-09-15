# Sam Gass
# scg0040
# Computational Biology
# Project 5
# python3 coded in Microsoft Visual Studio Code on Windows 10
# Last Modified: April 15, 2020
#
# This python code takes two pssm files from the command line and predicts TM score

from sys import argv
from sys import exit
from pickle import load
from PredictSS import openModel as openSSmodel
from PredictRSA import openModel as openSAmodel
from TrainingTM import Pair
from PredictRSA import Node


def openTMModel(modelname):
    try:
        with open(modelname, 'rb') as f:
            return load(f), load(f)
    except:
        print("Error opening model. Model must be a pkl file for TM prediction.")
        exit()


def validateArgs():
    if (len(argv) < 3):
        print("Error. Insufficent arguments. Requires two pssm files.")
        exit()


def predict(w0, w1, SSmodel, SAmodel, name1, name2):
    d = Pair(name1, name2, SSmodel, SAmodel, False)
    prediction = w0
    for x in d.features:
        prediction += (w1 * x)
    print("Predicted TM-score:", prediction)


if __name__ == "__main__":
    validateArgs()
    w0, w1 = openTMModel('TMmodel.pkl')
    SSmodel = openSSmodel('SSmodel.pkl')
    SAmodel = openSAmodel('SAmodel.pkl')

    filename1 = argv[1]
    filename2 = argv[2]
    predict(w0, w1, SSmodel, SAmodel, filename1, filename2)
