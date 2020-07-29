import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pybiblio import bibliometrics

data = pd.read_csv("./data.csv")

analysis = bibliometrics.Bibliometrics()

ABINITtest = analysis.cit_num(ABINIT, by='TI', subset=['density','theory'], n=15, norm = False, sort = False)
print(ABINITtest)


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

