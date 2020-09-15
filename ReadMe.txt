------------------
Usage Instructions
------------------
This program was create on Windows.

Before execution, ensure that PredictTM.py, TrainingTM.py, PredictRSA.py, PredictSS.py, and the three pickle files,
SAmodel.pkl, SSmodel.pkl, and TMmodel.pkl are all in the same directory.
In this directory, place two subdirectories named "pssm" and "fasta"
In these subdirectories place the pssm files and the fasta files that will be used in prediction.

From the command line, PredictTM.py takes two command line arguements.
The arguments are the names of two proteins without a file extension i.e. "1a3a"
In the pssm and fasta subdirectories there should be files with these two names and the cooresponding extension.

To run the program, from the command line type:		python PredictTM.py [name of protein 1] [name of protein 2]

The program will output to the terminal "Predicted TM-Score:" and then the model's predicted TM-score.

TrainingTM.py is the program that creates the TMmodel.pkl file.
There is no need to run it as I have already run it on my machine and its output, TMmodel.pkl, is given.
The average square error of the model given is 0.0022

The other .py files and .pkl files present are used by TrainingTM.py and PredictTM.py to 
extract the features from the pssm and fasta files