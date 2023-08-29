# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 12:21:50 2022

@author: NidhiGoyal
"""
import pandas as pd
import numpy as np
#reading files
df6=pd.read_csv('cleaned_dealer_data.csv')
cluster4_0=pd.read_csv('cluster4_0_n1.csv')
cluster4_1=pd.read_csv('cluster4_1_n1.csv')
cluster4_2=pd.read_csv('cluster4_2_n1.csv')
cluster4_3=pd.read_csv('cluster4_3_n1.csv')
numerical=pd.read_csv('numerical.csv')

x=pd.concat([cluster4_0,cluster4_1,cluster4_2,cluster4_3])
df6=df6.groupby(by='mx_highest_bid_dealer_id').agg({'car':['count'],'mx_target_price_y':[np.median],'km':[np.median],'age':[np.median],'cubiccapacity':[np.median],'damagessummary':[np.mean]})
df6=df6[df6.iloc[:,0]>24]
x=pd.merge(numerical[['mx_highest_bid_dealer_id','car|count','mx_target_price_y|median']],x,on='mx_highest_bid_dealer_id')

y=x[x['car|count']>24]
y=x[x['car|count']>24].groupby(by='label').median()
y=pd.merge(y,df6.iloc[:,1])

cluster4_0=y.groupby(by=['label']).get_group(0)
cluster4_1=y.groupby(by=['label']).get_group(1)
cluster4_2=y.groupby(by=['label']).get_group(2)
cluster4_3=y.groupby(by=['label']).get_group(3)

############## plotting 3D graphs for cluster visualization #########################

import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 300
ax = plt.axes(projection='3d')
scat_plot1=ax.scatter3D(y['km|median'],y['age|median'],y['mx_target_price_y|median'],c=y['label']);
ax.set_title('Cluster Visualisation')
ax.set_xlabel('km',fontsize=9)
ax.set_ylabel('age',fontsize=9)
ax.set_zlabel('mx_target_price',fontsize=9,labelpad=7)
ax.view_init(30,120)

############ plotting graphs for individual clusters ###########################
import plotly.express as px
from plotly.offline import plot

##########cluster 0 #########
fig=px.histogram(cluster4_0,x='carcount',marginal='box',nbins=50,title='Distribution of car count for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_0,x='mx_target_price_y|median',marginal='box',nbins=50,title='Distribution of Target Price for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_0,x='km|median',marginal='box',nbins=50,title='Distribution of km reading for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_0,x='age|median',marginal='box',nbins=50,title='Distribution of Age for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_0,x='damagessummary|mean',marginal='box',nbins=50,title='Distribution of Damages for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

hatch_tp=cluster4_0.iloc[:,17]
fig=px.histogram(x=hatch_tp,marginal='box',nbins=50,title='Distribution of tp of hatchbacks for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

SUV_tp=cluster4_0.iloc[:,20]
SUV_tp=SUV_tp[SUV_tp!=0]
fig=px.histogram(x=SUV_tp,marginal='box',nbins=50,title='Distribution of tp of SUV\'s for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

Sedan_tp=cluster4_0.iloc[:,21]
Sedan_tp=Sedan_tp[Sedan_tp!=0]
fig=px.histogram(x=Sedan_tp,marginal='box',nbins=50,title='Distribution of tp of Sedan\'s for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

#############cluster 1##############
fig=px.histogram(cluster4_1,x='carcount',marginal='box',nbins=50,title='Distribution of car count for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_1,x='mx_target_price_y|median',marginal='box',nbins=50,title='Distribution of Target Price for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_1,x='km|median',marginal='box',nbins=50,title='Distribution of km reading for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_1,x='age|median',marginal='box',nbins=50,title='Distribution of Age for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_1,x='damagessummary|mean',marginal='box',nbins=50,title='Distribution of Damages for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

hatch_tp=cluster4_1.iloc[:,17]
fig=px.histogram(x=hatch_tp,marginal='box',nbins=50,title='Distribution of tp of hatchbacks for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

SUV_tp=cluster4_1.iloc[:,20]
SUV_tp=SUV_tp[SUV_tp!=0]
fig=px.histogram(x=SUV_tp,marginal='box',nbins=50,title='Distribution of tp of SUV\'s for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

Sedan_tp=cluster4_1.iloc[:,21]
Sedan_tp=Sedan_tp[Sedan_tp!=0]
fig=px.histogram(x=Sedan_tp,marginal='box',nbins=50,title='Distribution of tp of Sedan\'s for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

########cluster 2##########
fig=px.histogram(cluster4_2,x='carcount',marginal='box',nbins=50,title='Distribution of car count for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_2,x='mx_target_price_y|median',marginal='box',nbins=50,title='Distribution of Target Price for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_2,x='km|median',marginal='box',nbins=50,title='Distribution of km reading for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_2,x='age|median',marginal='box',nbins=50,title='Distribution of Age for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_2,x='damagessummary|mean',marginal='box',nbins=50,title='Distribution of Damages for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

hatch_tp=cluster4_2.iloc[:,17]
fig=px.histogram(x=hatch_tp,marginal='box',nbins=50,title='Distribution of tp of hatchbacks for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

SUV_tp=cluster4_2.iloc[:,20]
SUV_tp=SUV_tp[SUV_tp!=0]
fig=px.histogram(x=SUV_tp,marginal='box',nbins=50,title='Distribution of tp of SUV\'s for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

Sedan_tp=cluster4_2.iloc[:,21]
Sedan_tp=Sedan_tp[Sedan_tp!=0]
fig=px.histogram(x=Sedan_tp,marginal='box',nbins=50,title='Distribution of tp of Sedan\'s for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

########cluster 3##########
fig=px.histogram(cluster4_3,x='carcount',marginal='box',nbins=50,title='Distribution of car count for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_3,x='mx_target_price_y|median',marginal='box',nbins=50,title='Distribution of Target Price for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_3,x='km|median',marginal='box',nbins=50,title='Distribution of km reading for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_3,x='age|median',marginal='box',nbins=50,title='Distribution of Age for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster4_3,x='damagessummary|mean',marginal='box',nbins=50,title='Distribution of Damages for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

hatch_tp=cluster4_3.iloc[:,17]
fig=px.histogram(x=hatch_tp,marginal='box',nbins=50,title='Distribution of tp of hatchbacks for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

SUV_tp=cluster4_3.iloc[:,20]
SUV_tp=SUV_tp[SUV_tp!=0]
fig=px.histogram(x=SUV_tp,marginal='box',nbins=50,title='Distribution of tp of SUV\'s for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

Sedan_tp=cluster4_3.iloc[:,21]
Sedan_tp=Sedan_tp[Sedan_tp!=0]
fig=px.histogram(x=Sedan_tp,marginal='box',nbins=50,title='Distribution of tp of Sedan\'s for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)


######################### mapping #################################

car5_0=pd.read_csv('cluster5_0.csv')
car5_1=pd.read_csv('cluster5_1.csv')
car5_2=pd.read_csv('cluster5_2.csv')
car5_3=pd.read_csv('cluster5_3.csv')
car5_4=pd.read_csv('cluster5_4.csv')

dealer4_0=cluster4_0
dealer4_1=cluster4_1
dealer4_2=cluster4_2
dealer4_3=cluster4_3

# car cluster profile for matching
summary_car0=car5_0[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car0=summary_car0[4:7]
proportion_car0=car5_0[['type','car']].groupby(by=['type']).count()/len(car5_0)
proportion_car0=proportion_car0.iloc[[2,6,7],:]


summary_car1=car5_1[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car1=summary_car1[4:7]
proportion_car1=car5_1[['type','car']].groupby(by=['type']).count()/len(car5_1)
proportion_car1=proportion_car1.iloc[[2,6,7],:]

summary_car2=car5_2[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car2=summary_car2[4:7]
proportion_car2=car5_2[['type','car']].groupby(by=['type']).count()/len(car5_2)
proportion_car2=proportion_car2.iloc[[2,6,7],:]

summary_car3=car5_3[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car3=summary_car3[4:7]
proportion_car3=car5_3[['type','car']].groupby(by=['type']).count()/len(car5_3)
proportion_car3=proportion_car3.iloc[[2,6,7],:]

summary_car4=car5_4[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car4=summary_car4[4:7]
proportion_car4=car5_4[['type','car']].groupby(by=['type']).count()/len(car5_4)
proportion_car4=proportion_car4.iloc[[0,4,5],:]

#dealer cluster for matching
summary_dealer0=dealer4_0[['mx_target_price_y|median','km|median', 'age|median','damagessummary|mean']].describe()
summary_dealer0=summary_dealer0[4:7]
proportion0=dealer4_0[['Hatchback','SUV','Sedan']].median()

summary_dealer1=dealer4_1[['mx_target_price_y|median','km|median', 'age|median','damagessummary|mean']].describe()
summary_dealer1=summary_dealer1[4:7]
proportion1=dealer4_1[['Hatchback','SUV','Sedan']].median()

summary_dealer2=dealer4_2[['mx_target_price_y|median','km|median', 'age|median','damagessummary|mean']].describe()
summary_dealer2=summary_dealer2[4:7]
proportion2=dealer4_2[['Hatchback','SUV','Sedan']].median()

summary_dealer3=dealer4_3[['mx_target_price_y|median','km|median', 'age|median','damagessummary|mean']].describe()
summary_dealer3=summary_dealer3[4:7]
proportion3=dealer4_3[['Hatchback','SUV','Sedan']].median()

#for dealer cluster0
tp_variance0,tp_variance1,tp_variance2,tp_variance3=[],[],[],[]
km_variance0,km_variance1,km_variance2,km_variance3=[],[],[],[]
age_variance0,age_variance1,age_variance2,age_variance3=[],[],[],[]
damage_variance0,damage_variance1,damage_variance2,damage_variance3=[],[],[],[]
proportion_variance0,proportion_variance1,proportion_variance2,proportion_variance3=[],[],[],[]
dealer0,dealer1,dealer2,dealer3=np.array([]),np.array([]),np.array([]),np.array([])
score0,score1,score2,score3=np.array([]),np.array([]),np.array([]),np.array([])

summary_car=[summary_car0,summary_car1,summary_car2,summary_car3,summary_car4]
proportion_car=[proportion_car0,proportion_car1,proportion_car2,proportion_car3, proportion_car4]
summary_dealer=[summary_dealer0,summary_dealer1,summary_dealer2,summary_dealer3]
proportion_dealer=[proportion0,proportion1,proportion2,proportion3]
tp=[tp_variance0,tp_variance1,tp_variance2,tp_variance3]
km=[km_variance0,km_variance1,km_variance2,km_variance3]
age=[age_variance0,age_variance1,age_variance2,age_variance3]
damage=[damage_variance0,damage_variance1,damage_variance2,damage_variance3]
proportion=[proportion_variance0,proportion_variance1,proportion_variance2,proportion_variance3]
dealer=[dealer0,dealer1,dealer2,dealer3]
score=[score0,score1,score2,score3]

import numpy as np        
from sklearn.metrics import mean_squared_error
count=0
for k,l,m,n,o,p,q in zip(summary_dealer,proportion_dealer,tp,km,age,damage,proportion):
    print(count)
    for i,j in zip(summary_car,proportion_car):
        m.append(mean_squared_error(i['mx_target_price'],k['mx_target_price_y|median']))
        n.append(mean_squared_error(i['km'],k['km|median']))
        o.append(mean_squared_error(i['age'],k['age|median']))
        p.append(mean_squared_error(i['damagessummary'],k['damagessummary|mean']))
        j['dealer']=l
        q.append(j.cov().iloc[0,1]) 
        
    r=np.matrix([pd.Series(m).rank(),pd.Series(n).rank(),pd.Series(o).rank(),pd.Series(p).rank(),pd.Series(q).rank()]).transpose()
    print(m,n,o,p,q)
    print(r)
    score=r.sum(axis=1)
    print(score)
    print()
    count+=1
    del m,n,o,p,q 


"""
#delaer cluster 0 ranking

# tp km  age damage proportion
[[1.5 1.5 3.5 2.5 9.5]
 [9.5 5.5 9.5 6.5 1.5]
 [7.5 7.5 7.5 6.5 5.5]
 [5.5 9.5 1.5 2.5 3.5]
 [3.5 3.5 5.5 9.5 7.5]]

[[18.5]
 [32.5]
 [34.5]
 [22.5]
 [29.5]]

#dealer cluster 1 ranking

[[2.  2.  2.  1.5 5. ]
 [5.  4.  5.  3.5 1. ]
 [4.  5.  4.  3.5 3. ]
 [3.  3.  1.  1.5 2. ]
 [1.  1.  3.  5.  4. ]]

[[12.5]
 [18.5]
 [19.5]
 [10.5]
 [14. ]]

#dealer cluster 2 ranking
[[4.  3.  4.  3.5 5. ]
 [5.  1.  2.  1.5 1. ]
 [1.  2.  1.  1.5 3. ]
 [2.  5.  3.  3.5 2. ]
 [3.  4.  5.  5.  4. ]]

[[19.5]
 [10.5]
 [ 8.5]
 [15.5]
 [21. ]]

#dealer cluster 3 ranking

[[4.  1.  2.  1.5 5. ]
 [5.  4.  5.  3.5 2. ]
 [2.  5.  3.  3.5 4. ]
 [1.  3.  1.  1.5 1. ]
 [3.  2.  4.  5.  3. ]]
[[13.5]
 [19.5]
 [17.5]
 [ 7.5]
 [17. ]]

"""

