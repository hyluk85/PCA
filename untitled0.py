#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 11:46:17 2023

@author: hluk
"""

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing

fp='/Users/hluk/Desktop/'
file='mw24.xlsx'

mw=pd.DataFrame(pd.read_excel(fp+file))
first_column=mw.pop('T: Protein IDs')
mw.insert(0, 'T: Protein IDs', first_column)

alldata=mw.drop(mw.columns[[25,26,27,28,29]], axis=1)

alldata_T=alldata.T

#### set first row as header
header=alldata_T.iloc[0].reset_index
alldata_T=alldata_T[1:]
#######

#scaled the data
scaled_data=StandardScaler().fit_transform(alldata_T)


###PCA fitting
pca=PCA()
pca.fit(scaled_data)
pca_data=pca.transform(scaled_data)
per_var=np.round(pca.explained_variance_ratio_*100,decimals=1)
######

###create lables for however many PC
labels=['PC'+str(x) for x in range (1,len(per_var)+1)]
plt.xlabel('Principle Component')
plt.ylabel('Percent of Explained Variance')
plt.title('Scree Plot')
plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label=labels)
plt.show()


ID=['ME-24a','ME-24b','ME-24c',
    'ME-Pa','ME-Pb','ME-Pc',
    'MR-24a','MR-24b','MR-24c',
    'MR-Pa','MR-Pb','MR-Pc',
    'FE-24a','FE-24b','FE-24c',
    'FE-Prea','FE-Preb','FE-Prec',
    'FR-24a','FR-24b','FR-24c',
    'FR-Pa','FR-Pb','FR-Pc']

pca_df=pd.DataFrame(pca_data, index=[ID], columns=labels)

fig=plt.figure(figsize=(14,10))
#ax=fig.add_subplot(11)
plt.scatter(pca_df['PC1'],pca_df['PC2'],cmap='Ser2_r',s=400)

for x,y, label in zip(pca_df['PC1'],pca_df['PC2'],ID):
    plt.text(x,y,label, fontsize=10)
