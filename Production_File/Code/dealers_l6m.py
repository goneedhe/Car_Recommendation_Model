# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 13:00:08 2022

@author: NidhiGoyal
"""

import pandas as pd

df1=pd.read_csv('dealer_l6m.csv',parse_dates=['activity_sold_date_ist'])
df2=df1.drop_duplicates(subset=['mx_lead_no'],keep='last')
x=df2[df2.year==0]


df2.make.fillna(df2.mx_make,inplace=True)
df2.model.fillna(df2.mx_model,inplace=True)
df2.mileage.fillna(df2.mx_km,inplace=True)
df2.numberofowners.fillna(df2.mx_car_owner,inplace=True)
df2.year.fillna(df2.mx_year,inplace=True)
#drop mx_city, mx_make, mx_model, mx_km, mx_car_owner, mx_lead_no, mx_year,mx_inspection_report_id, inspection_id,rank2, rank 1

#damages
df2['damages']=pd.Series([],dtype=int)
i=0
for i in df2.loc[df2.damagessummary.notnull()].index:
    df2['damages'][i]=(len(str(df2['damagessummary'][i]))//10)

df2.damages.fillna(0,inplace=True)

df2['sold_year']=df2['activity_sold_date_ist'].dt.year
df2['age']=df2['sold_year']-df2['year']

df2.make=df2.make.str.upper()
df2.model=df2.model.str.upper()

x=df2.model.value_counts()

df2.model=df2.model.str.replace(' ','')
df2.make=df2.make.str.replace(' ','')
df2.make.replace({'AMBASSADOR':'HINDUSTAN','MERCEDES BENZ':'MERCEDESBENZ','MERCEDES-BENZ':'MERCEDESBENZ','MAHINDRARENAULT':'MAHINDRA','OPEL CORSA':'OPEL','HINDUSTAN MOTORS':'HINDUSTAN','FORCE MOTORS':'FORCE'},inplace=True)
df2.model.replace({'WAGONR1.0':'WAGONR','GLACLASS':'GLA','C-CLASS':'CCLASS','DATSUNREDIGO':'REDIGO','OPELCORSA':'CORSA'},inplace=True)
for i in df2[(df2.make=='NISSAN') & (df2.model=='REDIGO')].index:
    df2.make[i]='DATSUN'

#dealer profile
numerical=df2.groupby(by=['mx_validated_dealer_fcg_id','dealer_number']).agg({'mx_target_price':'median','age':'median','numberofowners':'median','mileage':'median','damages':'median'})

#last 6 months details
gmv=pd.read_excel('gmv.xlsx')
gmv=gmv.iloc[:3358,]


x=gmv[['Dealer ID', 'Dealership Name', 'Locality', 'DRM Name', 'City','Spinny/Wiseary Flag', 'CTx Status','CTx Cars Apr-22','CTx GMV Apr-22','AVG L3M GMV']]
active_flag=pd.merge(numerical,x,left_on='dealer_number',right_on='Dealer ID')
active_flag['l3m_activity_flag']=pd.Series([],dtype=int)

for i in active_flag.index:
    if (active_flag['CTx GMV Apr-22'][i]>0):
        active_flag['l3m_activity_flag'][i]=1
        if (active_flag['AVG L3M GMV'][i]<50000):
            active_flag['l3m_activity_flag'][i]=2
active_flag['l3m_activity_flag'].fillna(0,inplace=True)

# getting type of the car
df2['type']=pd.Series([])
x=pd.read_csv('type_calculated.csv')
i=0
for i in df2[df2.type.isna()].index:
    if x[(x.make==df2.make[i]) & (x.model==df2.model[i])].index.notnull().any(): 
        j=x[(x.make==df2.make[i]) & (x.model==df2.model[i])].index[0]
        df2['type'][i]=x.type[j]
        print(j,'amd',df2['type'][i])
        
#y=df2[df2.type.isna()]
# only hindustan ambassador left
df2.type=df2.type.fillna('Sedan')
df2.type.replace({'luxury':'Luxury','Suv':'SUV','Luxury\t':'Luxury'},inplace=True)
df2.type=df2.type.str.replace(' ','')

df2.drop(columns=['mx_city','mx_make', 'mx_model','mx_highest_bid_dealer_id','activity_sold_date_ist','mx_dealer_at_procurement', 'mx_km','mx_inspection_report_id','mx_car_owner', 'mx_lead_no', 'mx_year','mx_inspection_report_id', 'inspection_id','rank2', 'rank1','sold_year'],inplace=True)
df2.drop(columns=['damagessummary','dealer_id.1','chassiscolor','dealer_id','x6_digit_fcg_id__c','fcg_id__c'],inplace=True)

df2.to_csv('dealer_l6m_final_cleaned.csv')
        

        



