 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:44:52 2020

@author: mcd0029
"""

import pandas as pd
from pybiblio import bibliometrics

ABINIT = pd.read_csv("/home/mcd0029/Dropbox/WorkMachineLearning/dataframes/ABINIT.csv")
ADF = pd.read_csv("/home/mcd0029/Dropbox/WorkMachineLearning/dataframes/ADF.csv")
OCTOPUS = pd.read_csv("/home/mcd0029/Dropbox/WorkMachineLearning/dataframes/OCTOPUS.csv")
QE = pd.read_csv("/home/mcd0029/Dropbox/WorkMachineLearning/dataframes/QuantumExpresso.csv")
SIESTA = pd.read_csv("/home/mcd0029/Dropbox/WorkMachineLearning/dataframes/Siesta.csv")
VASP = pd.read_csv("/home/mcd0029/Dropbox/WorkMachineLearning/dataframes/VASP.csv")
OTHERS = pd.read_csv("/home/mcd0029/Dropbox/WorkMachineLearning/dataframes/Others.csv")
ALL = pd.read_csv("/home/mcd0029/Dropbox/WorkMachineLearning/dataframes/ALL.csv")

analysis = bibliometrics.Bibliometrics()

ABINITtest = analysis.cit_num(ABINIT, by='TI', subset=['density','theory'], n=15, norm = False, sort = False)
print(ABINITtest)

import numpy as np
import matplotlib.pyplot as plt
r1 = np.arange(len(ABINITtest))
fig = plt.figure(figsize=(6,4))
plt.bar(r1, ABINITtest.freq)
plt.xticks([r + 0.05 for r in range(len(ABINITtest))], ABINITtest.PY)
plt.xlabel("Year", fontsize = 15)
plt.ylabel("Normalized number of citations", fontsize = 13)
for x,y in zip(r1, ABINITtest.freq):
    label = "{:.2f}".format(y)
    plt.annotate(label, (x,y+0.0015), ha='center')
    


plt.plot(ABINITtest.numTI, ABINITtest.freq)
plt.xlabel("Number of words in title", fontsize=14)
plt.ylabel("Number of citations", fontsize=14)
plt.xticks(ABINITtest.numTI)



ADFtest = analysis.pub_by(ADF, by='FU', dpc=['DI'], n=10, norm = False, sort=False)
OCTOPUStest = analysis.pub_by(OCTOPUS, by='FU', n=10, norm = True, sort=False)
QEtest = analysis.pub_by(QE, by='FU', n=10, norm = True, sort=False)
SIESTAtest = analysis.pub_by(SIESTA, by='FU', n=10, norm = True, sort=False)
VASPtest = analysis.pub_by(VASP, by='FU', n=10, norm = True, sort=False)
OTHERStest = analysis.pub_by(OTHERS, by='FU', norm=True, n=10, sort=False)

ALLtest = analysis.pub_by(ALL, by='FU', n=10, norm=True, sort=False)
