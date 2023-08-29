# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 16:32:45 2022

@author: NidhiGoyal
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

#reading asset clusters
c0=pd.read_csv('cluster5_0.csv')
c1=pd.read_csv('cluster5_1.csv')
c2=pd.read_csv('cluster5_2.csv')
c3=pd.read_csv('cluster5_3.csv')
c4=pd.read_csv('cluster5_4.csv')

#getting cars in clusters by their count
c0_cars=c0.car.value_counts()
c1_cars=c1.car.value_counts()
c2_cars=c2.car.value_counts()
c3_cars=c3.car.value_counts()
c4_cars=c4.car.value_counts()

#car_cluster_summary
summary_car0=c0[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car0=summary_car0[4:7]
proportion_car0=c0[['type','car']].groupby(by=['type']).count()/len(c0)
proportion_car0=proportion_car0.iloc[[2,6,7],:]


summary_car1=c1[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car1=summary_car1[4:7]
proportion_car1=c1[['type','car']].groupby(by=['type']).count()/len(c1)
proportion_car1=proportion_car1.iloc[[2,6,7],:]

summary_car2=c2[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car2=summary_car2[4:7]
proportion_car2=c2[['type','car']].groupby(by=['type']).count()/len(c2)
proportion_car2=proportion_car2.iloc[[2,6,7],:]

summary_car3=c3[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car3=summary_car3[4:7]
proportion_car3=c3[['type','car']].groupby(by=['type']).count()/len(c3)
proportion_car3=proportion_car3.iloc[[2,6,7],:]

summary_car4=c4[['mx_target_price','km', 'age','damagessummary']].describe()
summary_car4=summary_car4[4:7]
proportion_car4=c4[['type','car']].groupby(by=['type']).count()/len(c4)
proportion_car4=proportion_car4.iloc[[0,4,5],:]

summary_car=[summary_car0,summary_car1,summary_car2,summary_car3,summary_car4]
proportion_car=[proportion_car0,proportion_car1,proportion_car2,proportion_car3,
                proportion_car4]

########################## last 6M dealer summary ############################

df=pd.read_csv('dealer_l6m_final_cleaned.csv')
df['car']=df['make']+' '+df['model']
numerical=df.groupby(by=['mx_validated_dealer_fcg_id']).agg({'car':'count',
                        'mx_target_price':'median','mileage':'median',
                        'age':'median','cubiccapacity':'median',
                        'damages':'median','numberofowners':'median'})

type_count=pd.get_dummies(df['type'])
type_count=type_count.join(df['mx_validated_dealer_fcg_id'])
type_count_sum=type_count.groupby(by=['mx_validated_dealer_fcg_id']).agg('sum')
type_count_proportion=type_count_sum.copy()
for i in type_count_sum.columns:
    type_count_proportion.loc[:,i]=type_count_sum.loc[:,i]/numerical['car']
    print(i)

################# target price for each car ###########################
#TP sum
tp_sum=df[['mx_validated_dealer_fcg_id','mx_target_price','type']]
tp_sum=pd.pivot_table(tp_sum,columns=['type'],index=['mx_validated_dealer_fcg_id'],
                      aggfunc=['sum'])
tp_sum=tp_sum.fillna(0)  
#TP Median
tp_median=df[['mx_validated_dealer_fcg_id','mx_target_price','type']]
tp_median=pd.pivot_table(tp_median,columns=['type'],index=['mx_validated_dealer_fcg_id'],
                         aggfunc=['median'])
tp_median=tp_median.fillna(0)  

#joining data
data1=numerical.join(type_count_proportion)
data1=data1.join(tp_median)
#dealer summary created

############## Alloting new clusters on 6 last 6 months behaviour #############

df['allotment']=pd.Series([],dtype=int)

#matching
count=1
for x,group in df.groupby('mx_validated_dealer_fcg_id'):
    summary_dealer=group[['mx_target_price','mileage', 'age','damages']].describe()
    summary_dealer=summary_dealer[4:7]
    proportion_dealer=data1.loc[x,:][['Hatchback','SUV','Sedan']]
    
    tp_variance0,tp_variance1,tp_variance2,tp_variance3=[],[],[],[]
    km_variance0,km_variance1,km_variance2,km_variance3=[],[],[],[]
    age_variance0,age_variance1,age_variance2,age_variance3=[],[],[],[]
    damage_variance0,damage_variance1,damage_variance2,damage_variance3=[],[],[],[]
    proportion_variance0,proportion_variance1,proportion_variance2,proportion_variance3=[],[],[],[]
    dealer0,dealer1,dealer2,dealer3=np.array([]),np.array([]),np.array([]),np.array([])
    score0,score1,score2,score3=np.array([]),np.array([]),np.array([]),np.array([])

    tp=[tp_variance0,tp_variance1,tp_variance2,tp_variance3]
    km=[km_variance0,km_variance1,km_variance2,km_variance3]
    age=[age_variance0,age_variance1,age_variance2,age_variance3]
    damage=[damage_variance0,damage_variance1,damage_variance2,damage_variance3]
    proportion=[proportion_variance0,proportion_variance1,proportion_variance2,proportion_variance3]
    dealer=[dealer0,dealer1,dealer2,dealer3]
    score=[score0,score1,score2,score3]
    
    for m,n,o,p,q in zip(tp,km,age,damage,proportion):
        for i,j in zip(summary_car,proportion_car):
            m.append(mean_squared_error(i['mx_target_price'],summary_dealer['mx_target_price']))
            n.append(mean_squared_error(i['km'],summary_dealer['mileage']))
            o.append(mean_squared_error(i['age'],summary_dealer['age']))
            p.append(mean_squared_error(i['damagessummary'],summary_dealer['damages']))
            j['dealer']=proportion_dealer
            q.append(j.cov().iloc[0,1])
            
         
        r=np.matrix([[sorted(m).index(x) for x in m],pd.Series(n).rank(),pd.Series(o).
                     rank(),pd.Series(p).rank(),pd.Series(q).rank()]).transpose()
        score=r.sum(axis=1).tolist()
        df.loc[df.mx_validated_dealer_fcg_id==x,'allotment']=score.index(min(score))
        del m,n,o,p,q 
        
        
#new labels defined
allotment=df.groupby('mx_validated_dealer_fcg_id').agg({'allotment':['max']})
x.to_csv('new_cluster_allotment.csv')

###############################################################################

# top 10 cars without count
priority_excel=pd.DataFrame()
for x,group in df.groupby('mx_validated_dealer_fcg_id'):
    y=pd.DataFrame(group.car.value_counts())
    y=y.reset_index()
    priority_excel=pd.concat([priority_excel,y['index']],ignore_index=True,axis=1)
priority_excel.columns=allotment.index
priority_excel=priority_excel.transpose()
priority_excel=priority_excel.iloc[:,0:10]  
#priority_excel.to_csv('priority_excel.csv') 

##############################################################################
gmv=pd.read_excel('gmv.xlsx')
gmv=gmv.iloc[:3358,]


x=gmv[['Dealer ID', 'Dealership Name', 'Locality', 'DRM Name', 'City','Spinny/Wiseary Flag', 'CTx Status','CTx Cars Apr-22','CTx GMV Apr-22','AVG L3M GMV']]
active_flag=pd.DataFrame()
active_flag['l3m_activity_flag']=pd.Series([],dtype=int)

for i in gmv.index:
    if (gmv['CTx GMV Apr-22'][i]>0):
        if (gmv['AVG L3M GMV'][i]<50000):
            active_flag.loc[i,'l3m_activity_flag']=2
        else:
            active_flag.loc[i,'l3m_activity_flag']=0
    if (gmv['CTx GMV Apr-22'][i]<1):
        active_flag.loc[i,'l3m_activity_flag']=1
active_flag['Dealer ID']=gmv['Dealer ID']        

#################### details of dealer ########################################
details=df.groupby('mx_validated_dealer_fcg_id').first()
details=details[['dealer_number','name','dealership_name','dealer_city','drm_name','allotment']]

####################### combining data ########################################
final=pd.concat([priority_excel,numerical,details,],axis=1) 
final=pd.merge(final,active_flag,left_on='dealer_number',right_on='Dealer ID')
final.drop(columns='Dealer ID',inplace=True)

############################ Delhi Dealers ###################################
delhi_final=final[(final.dealer_city=='Delhi NCR')|(final.dealer_city=='chandigarh')
                  |(final.dealer_city=='Chandigarh')|(final.dealer_city=='Ludhiana')
                  |(final.dealer_city=='NCR')|(final.dealer_city=='Delhi')
                  |(final.dealer_city=='Bhatinda')|(final.dealer_city=='Sangrur')
                  |(final.dealer_city=='Jalandhar')|(final.dealer_city=='Patiala')
                  |(final.dealer_city=='Faridabad')|(final.dealer_city=='Gurgaon')
                  |(final.dealer_city=='New Delhi')|(final.dealer_city=='Faridabad')
                  |(final.dealer_city=='Hisar')|(final.dealer_city=='Gurugram')
                  |(final.dealer_city=='West Delhi')|(final.dealer_city=='SONIPAT')
                  |(final.dealer_city=='Delhi_NCR')|(final.dealer_city=='Hissar')
                  |(final.dealer_city=='Amritsar')|(final.dealer_city=='Central Delhi')]

delhi_final.to_csv('delhi_final.csv')

####################### Delhi Dealers Car Count ##############################
y=df[(df.dealer_city=='Delhi NCR')|(df.dealer_city=='chandigarh')
                  |(df.dealer_city=='Chandigarh')|(df.dealer_city=='Ludhiana')
                  |(df.dealer_city=='NCR')|(df.dealer_city=='Delhi')
                  |(df.dealer_city=='Bhatinda')|(df.dealer_city=='Sangrur')
                  |(df.dealer_city=='Jalandhar')|(df.dealer_city=='Patiala')
                  |(df.dealer_city=='Faridabad')|(df.dealer_city=='Gurgaon')
                  |(df.dealer_city=='New Delhi')|(df.dealer_city=='Faridabad')
                  |(df.dealer_city=='Hisar')|(df.dealer_city=='Gurugram')
                  |(df.dealer_city=='West Delhi')|(df.dealer_city=='SONIPAT')
                  |(df.dealer_city=='Delhi_NCR')|(df.dealer_city=='Hissar')
                  |(df.dealer_city=='Amritsar')|(df.dealer_city=='Central Delhi')]

dummies=pd.get_dummies(y.car)
dummies.index=y.dealer_number
dummies=dummies.reset_index()
dummies=dummies.groupby(by='dealer_number').agg('sum')
dummies.to_csv('Delhi_dealers_car_count_l3m_inactivity.csv')




