# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:16:16 2022

@author: NidhiGoyal
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

plt.rcParams['figure.dpi'] = 300
df=pd.read_csv('outliers_removed+knn.csv')
df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1','mx_km', 'junkflag','registrationnumber','mileage','inspection_year'],inplace=True)
numerical_cols=df.select_dtypes(include=np.number).columns.tolist()
del numerical_cols[0],numerical_cols[1],numerical_cols[2],numerical_cols[4],numerical_cols[7]

df.type.replace({'luxury':'Luxury','Suv':'SUV','Luxury\t':'Luxury'},inplace=True)
df.transmission.replace({'Manual/auto':'Manual/Auto','manual':'Manual','mANUAL/Auto':'Manual/Auto','auto':'Auto','aUTO':'Auto'},inplace=True)
#live plots
from plotly.offline import plot
fig=px.histogram(df,x='mx_target_price',marginal='box',nbins=50,title='Distribution of Target Price')
fig.update_layout(bargap=0.1)
plot(fig)

plot(px.bar(df,x='insurancetype',y='mx_target_price'))



corr=df.corr()
sns.heatmap(corr)
#mx_target_price is negatively correlated with age,km,numberofowners and damagessummary
#mx_target_price is positively correlated with bodyexteriordesign,bodyinteriordesign and cubic capacity

#checking age and target price
sns.scatterplot(x='age',y='mx_target_price',data=df.reset_index(),hue='make')

#checking km and target price for different make of cars
sns.scatterplot(x='km',y='mx_target_price',data=df.reset_index(),hue='make')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

#checking age and target price for different type of cars
sns.scatterplot(x='age',y='mx_target_price',data=df.reset_index(),hue='type',s=9)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

#checking age and target price for different transmission of cars
sns.scatterplot(x='age',y='mx_target_price',data=df.reset_index(),hue='transmission')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

#checking age and target price for different number of owners
sns.scatterplot(x='age',y='mx_target_price',data=df.reset_index(),hue='numberofowners')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

sns.scatterplot(x='age',y='mx_target_price',data=df.reset_index(),hue='chassiscolor',s=15)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)


sns.swarmplot(x=df['make'],y=df['mx_target_price'])
sns.catplot(x='make',y='mx_target_price',data=df,s=2)
plt.xticks(rotation=90,fontsize=5)

sns.catplot(x='type',y='mx_target_price',data=df)
plt.xticks(rotation=90)

sns.catplot(x='transmission',y='mx_target_price',data=df)
sns.catplot(x='insurancetype',y='mx_target_price',data=df)
sns.catplot(x='caronhypothecation',y='mx_target_price',data=df)
sns.swarmplot(x='chassiscolor',y='mx_target_price',data=df)

sns.countplot(x='type',data=df)
plt.xticks(rotation=90)

sns.countplot(x='registeredcity',data=df)
plt.xticks(rotation=90,fontsize=5)

sns.countplot(x='make',data=df)
plt.xticks(rotation=90,fontsize=3)


plt.boxplot(['mx_target_price','mx_km','mileage','cubiccapacity','age','damagessummary'],notch=True,labels=['mx_target_price','mx_km','mileage','cubiccapacity','age','damagessummary'])
df[['mx_target_price']].plot(kind='box')
plt.show()




