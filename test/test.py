import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pybiblio import bibliometrics

#import data
data = pd.read_csv("data.csv")

#create a bibliometrics object
analysis = bibliometrics.Bibliometrics()

#Number of citations per year
citYear = analysis.cit_by(data, by='PY', n=5, norm = True, sort = False)

#Barplot 
r1 = np.arange(len(citYear))
fig = plt.figure(figsize=(6,4))
plt.bar(r1, citYear.freq)
plt.xticks([r + 0.05 for r in range(len(citYear))], citYear.PY)
plt.xlabel("Year", fontsize = 15)
plt.ylabel("Normalized number of citations", fontsize = 13)
for x,y in zip(r1, citYear.freq):
    label = "{:.2f}".format(y)
    plt.annotate(label, (x,y+0.0015), ha='center')
    
#Number of publications by funding agency
pubFunding = analysis.pub_by(data, by='FU', dpc=['DI'], n=10, norm = False, sort = True)

#Number of citations as function of the number of words in titles
citTitle = analysis.cit_num(data, by='TI', n=15, subset=['density', 'theory'], sep=',', norm = False, sort = False)

#plot the above results
plt.plot(citTitle.numTI, citTitle.freq)
plt.xlabel("Number of words in title", fontsize=14)
plt.ylabel("Number of citations", fontsize=14)
plt.xticks(citTitle.numTI)
