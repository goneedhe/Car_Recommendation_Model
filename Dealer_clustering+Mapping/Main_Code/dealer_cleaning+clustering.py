# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:48:51 2022

@author: NidhiGoyal
"""
#importing libraries
import psycopg2
import pandas as pd
import numpy as np
#establishing connection with database
connection_string = "host='doppler.c4nfnb3d0ywp.eu-west-1.redshift.amazonaws.com' dbname='panameraods' user='nidhi_goyal' password='cUNXrIhMNc6GsMg#1' port='5439'"
conn_pg = psycopg2.connect(connection_string)

#saving dealer data to csv
pd.read_sql('select* from southasia_cmc_sandbox.dealerprofile;',conn_pg).to_csv('dealer_data.csv')
#448129 rows
#reading csv file saved
df1=pd.read_csv(r'C:\Users\NidhiGoyal\.spyder-py3\dealer_data.csv', parse_dates=['createdon'])
#reading cleaned data of assets that the dealers have bought
df2=pd.read_csv(r'C:\Users\NidhiGoyal\.spyder-py3\outliers_removed+knn.csv')

#convert into uppercase and removing spaces
df1.mx_reg_no=df1.mx_reg_no.str.upper()
df1.mx_reg_no=df1.mx_reg_no.str.replace(' ','')
df2.registrationnumber=df2.registrationnumber.str.upper()
df2.registrationnumber=df2.registrationnumber.str.replace(' ','') 

#taking intersection on cars and dealer data
df3=pd.merge(df1,df2,left_on='mx_reg_no',right_on='registrationnumber')
#checking for unique dealers
df3.mx_highest_bid_dealer_id.str.upper().nunique()
#6202

#dropping additional columns
df3.drop(columns=['Unnamed: 0_x','Unnamed: 0_y','Unnamed: 0.1', 'Unnamed: 0.1.1','mx_km_y','junkflag','mileage'],inplace=True)
df5=df3.head(50)

#dropping additional columns
df6=df3.drop(columns=['mx_reg_no','mx_make','mx_model','mx_km_x', 'mx_target_price_x', 'city', 'mx_city','mx_state', 'mx_fuel_type', 'createdon'])
#defining new column for car that consists of both make and model
df6['car']=df6['make']+' '+df6['model']
df6.drop(columns=['make','model','inspection_year','registrationnumber','year_y'],inplace=True)
df6.drop(columns=['Unnamed: 0'],inplace=True)
#combining duplicate categories
df6.type.replace({'luxury':'Luxury','Suv':'SUV','Luxury\t':'Luxury'},inplace=True)
df6.transmission.replace({'Manual/auto':'Manual/Auto','manual':'Manual','mANUAL/Auto':'Manual/Auto','auto':'Auto','aUTO':'Auto'},inplace=True)
df6.type=df6.type.str.replace(' ','') 

#grouping according to dealer
df6.to_csv('cleaned_dealer_data.csv')
df6=pd.read_csv('cleaned_dealer_data.csv')
groups=df6.groupby(by=['mx_highest_bid_dealer_id'])

#analysing a dealer
x=groups.get_group('14efc7a2-bd80-4dee-8e98-aa28a0797480')
describe=x.describe()


#################### Approach 2 #######################################

##preparing new data as requested
#this data includes the proportion of cars bought and target price for each type of cars

#getting numerical attricutes
numerical=df6.groupby(by=['mx_highest_bid_dealer_id']).agg({'car':['count'],'mx_target_price_y':[np.median],'km':[np.median],'age':[np.median],'cubiccapacity':[np.median],'damagessummary':[np.median]})
numerical.columns = numerical.columns.map('|'.join).str.strip('|')

categorical=df6.select_dtypes(include=object)
categorical.drop(columns=['mx_highest_bid_dealer_id','transmission','registeredcity','fuel'],inplace=True)
categorical=pd.get_dummies(categorical)
categorical=categorical.join(df6['mx_highest_bid_dealer_id'])
categorical_agg=categorical.groupby(by='mx_highest_bid_dealer_id').agg('sum')

#treating outliers in target price
df6.loc[df6['mx_target_price_y']>df6['mx_target_price_y'].quantile(0.95),['mx_target_price_y']]=df6['mx_target_price_y'].quantile(0.95)


#treating outliers in age
df6.loc[df6['age']>df6['age'].quantile(0.97),['age']]=df6['age'].quantile(0.95)


#proportion of cars
type_count=pd.get_dummies(df6['type'])
type_count=type_count.join(df6['mx_highest_bid_dealer_id'])
type_count_sum=type_count.groupby(by=['mx_highest_bid_dealer_id']).agg('sum')
type_count_proportion=type_count_sum.copy()
for i in type_count_sum.columns:
    type_count_proportion.loc[:,i]=type_count_sum.loc[:,i]/numerical['car|count']
    print (i)

#target price for each car
#TP sum
tp_sum=df6[['mx_highest_bid_dealer_id','mx_target_price_y','type']]
tp_sum=pd.pivot_table(tp_sum,columns=['type'],index=['mx_highest_bid_dealer_id'],aggfunc=['sum'])
tp_sum=tp_sum.fillna(0)  
#TP Median
tp_median=df6[['mx_highest_bid_dealer_id','mx_target_price_y','type']]
tp_median=pd.pivot_table(tp_median,columns=['type'],index=['mx_highest_bid_dealer_id'],aggfunc=['median'])
tp_median=tp_median.fillna(0)  

#joining data
data1=numerical.join(type_count_proportion)
data1=data1.join(tp_median)

car=pd.get_dummies(df6['car'])
car=car.join(df6['mx_highest_bid_dealer_id'])
car=car.groupby(by=['mx_highest_bid_dealer_id']).agg('sum')

#type_count, tp_median, km, age, cc, damagessummary taken into account
#adding cars
data1=data1.join(car)
data1=data1[data1['car|count']>24]
data1=data1.drop(columns=['car|count', 'mx_target_price_y|median'])

#standardising data
from sklearn.preprocessing import StandardScaler
std=StandardScaler()
data_std1=std.fit_transform(data1)


#performing PCA
from sklearn.decomposition import PCA
pca=PCA(0.95)
principal_components_dealers1=pca.fit_transform(data_std1)


#clustering on new data using cosine similarity

import matplotlib.pyplot as plt
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.elbow import elbow
from pyclustering.utils.metric import distance_metric, type_metric


def cosine_distance(a, b):
     a_norm = np.linalg.norm(a)
     b_norm = np.linalg.norm(b)
     similiarity = np.dot(a, b.T)/(a_norm * b_norm)
     dist = 1. - similiarity
     return dist
metric = distance_metric(type_metric.USER_DEFINED, func=cosine_distance)

kmin, kmax = 2, 15
elbow_instance = elbow(principal_components_dealers1, kmin, kmax)
elbow_instance.process()
amount_clusters = elbow_instance.get_amount()   # most probable amount of clusters
wce = elbow_instance.get_wce()

centers = kmeans_plusplus_initializer(principal_components_dealers1, amount_clusters).initialize()
kmeans_instance = kmeans(principal_components_dealers1, centers,metric=metric)
kmeans_instance.process()

clusters = kmeans_instance.get_clusters()
centers = kmeans_instance.get_centers()
label=kmeans_instance.predict(principal_components_dealers1)
plt.plot(np.arange(2,16),wce,marker='X')

final2=data1.copy()
final2['label']=label
grouped2=final2.groupby(by=['label'])
statistics_km=final2.groupby(by=['label']).agg('median')



# 1253, 394, 237, 229, 228, 179 : number of dealers in each cluster

#4 clusters
centers = kmeans_plusplus_initializer(principal_components_dealers1, 4).initialize()
kmeans_instance = kmeans(principal_components_dealers1, centers,metric=metric)
kmeans_instance.process()

clusters = kmeans_instance.get_clusters()
centers = kmeans_instance.get_centers()
label5=kmeans_instance.predict(principal_components_dealers1)
#1125,682,388,325
final3=data1.copy()
final3['label']=label5
statistics_km4=final3.groupby(by=['label']).agg('median')

#exporting clusters to csv file
cluster4_0=final3.groupby(by=['label']).get_group(0).to_csv('cluster4_0_n1.csv')
cluster4_1=final3.groupby(by=['label']).get_group(1).to_csv('cluster4_1_n1.csv')
cluster4_2=final3.groupby(by=['label']).get_group(2).to_csv("cluster4_2_n1.csv")
cluster4_3=final3.groupby(by=['label']).get_group(3).to_csv("cluster4_3_n1.csv")

#1485,474,335,262 with those 9 dealers
#1296,590,342,292

