# -*- coding: utf-8 -*-
"""
Created on Mon May 23 19:30:49 2022

@author: NidhiGoyal
"""
import pandas as pd
import numpy as np
 
df=pd.read_csv(r'C:\Users\NidhiGoyal\.spyder-py3\cleaned_data.csv')
#'mx_target_price', 'mx_km', 'junkflag', 'fuel', 'make', 'year_y','model', 'mileage', 'roadtaxpaid', 'cubiccapacity', 'insurancetype','numberofowners', 'registeredcity', 'caronhypothecation','registrationnumber', 'chassiscolor', 'damagessummary','bodyexteriordesign', 'bodyinteriordesign', 'inspection_year', 'age'
#Size : 427508 X 22

#checking for cubic capacity dtype as object
u=df.cubiccapacity.value_counts()
df.cubiccapacity=df.cubiccapacity.replace('DibberDobber1234',np.nan)
df.cubiccapacity=df.cubiccapacity.replace('NA ok',np.nan)
df.cubiccapacity=df.cubiccapacity.replace('Hdj',np.nan)
df.cubiccapacity=pd.to_numeric(df.cubiccapacity)


#defining numerical and categorical columns
numerical_cols=df.select_dtypes(include=np.number).columns.tolist()

#checking to fill null values in categorical columns
#fuel
df.fuel.isna().sum()        #3059
#filling null values for fuel
i=0
for i in df[df.fuel.isna()].index:
    if df[(df.make==df.make[i]) & (df.model==df.model[i])].fuel.mode().notnull().any(): 
        df.fuel[i]=df[(df.make==df.make[i]) & (df.model==df.model[i] )].fuel.mode()[0]
        print(df[(df.make==df.make[i]) & (df.model==df.model[i] )].fuel.mode()[0],'and',df.fuel[i])
#335 null values
i=178604
for i in df[df.fuel.isna()].index:
    if df[(df.make==df.make[i])].fuel.mode().notnull().any():
        df.fuel[i]=df[(df.make==df.make[i])].fuel.mode()[0]
        print(df[(df.make==df.make[i])].fuel.mode()[0],'and', df.fuel[i])
#12 null values
df.fuel=df.fuel.fillna(df.fuel.mode()[0])
#0 null values


#insurance type has a lot of null values
df.insurancetype.value_counts()
z=df.insurancetype.value_counts().index.tolist()
#filling null values in proportion with past data present
w,i=[],''
for i in z:
    w.append((df[df.insurancetype==i].insurancetype.notnull().sum())/df.insurancetype.notnull().sum())
    
x=df.insurancetype.fillna(pd.Series(np.random.choice(z,p=w,size=len(df))))
df.insurancetype=x

#11633 null values in color
i=0
for i in df[df.chassiscolor.isna()].index:
    if df[(df.make==df.make[i]) & (df.model==df.model[i])].chassiscolor.mode().notnull().any(): 
        df.chassiscolor[i]=df[(df.make==df.make[i]) & (df.model==df.model[i] )].chassiscolor.mode()[0]
        print(df[(df.make==df.make[i]) & (df.model==df.model[i] )].chassiscolor.mode()[0],'and',df.chassiscolor[i])

#892 null values
i=0
for i in df[df.fuel.isna()].index:
    if df[(df.make==df.make[i])].chassiscolor.mode().notnull().any():
        df.chassiscolor[i]=df[(df.make==df.make[i])].chassiscolor.mode()[0]
        print(df[(df.make==df.make[i])].chassiscolor.mode()[0],'and', df.chassiscolor[i])

df.chassiscolor=df.chassiscolor.fillna(df.chassiscolor.mode()[0])
#0 null values

#filling null values in caronhypothecation
df.caronhypothecation=df.caronhypothecation.fillna(df.caronhypothecation.mode()[0])

#registrationnumber is only used for identification purposes : no need to fill it

#filling null values in registeredcity
#propotion of cars obtained from a state should not change much
z=df.registeredcity.value_counts().index.tolist()
w,i=[],''
for i in z:
    w.append(df[df.registeredcity==i].registeredcity.notnull().sum()/df.registeredcity.notnull().sum())
    
y=df.registeredcity.fillna(pd.Series(np.random.choice(z,p=w,size=len(df))))
df.registeredcity=y
df.registeredcity=df.registeredcity.replace('DIBBERDOBBER1234',np.nan)
df.registeredcity=df.registeredcity.replace('GCT',np.nan)
df.drop(columns=['roadtaxpaid'],inplace=True)


#checking make and model
df.make=df.make.str.upper()
df.make=df.make.str.replace(' ','')
df.make=df.make.str.replace('-','')
df.model=df.model.str.replace(' ','')
df.model=df.model.str.upper()
#make has no null values

#model has 105 null values
x=df[df.model.isna()].make.value_counts()
#make of the car
df.drop_duplicates(subset=['make','model'])[['make','model']].to_csv('type.csv')

df['make']=df['make'].replace({'ASTON':'ASTONMARTIN','CARSHONDA':'HONDA','FORCEMOTORS':'FORCE','HINDUSTAN':'HINDUSTANMOTORS','MAHINDRA':'MAHINDRARENAULT','MERCEDES':'MERCEDESBENZ','MERCEDESBENZ1':'MERCEDESBENZ','OPELCORSA':'OPEL','ASHOK':'ASHOKLEYLAND'})
df.make.nunique()
df.model.replace({'MARTINDB9':'DB9','MARTINDB11':'DB11','MARTINRAPIDE':'RAPIDE','MARTINVANTAGE':'VANTAGE'},inplace=True)
Z=df[df.make=='ASTONMARTIN']
#ASHOKLEYLAND
df.model.replace({'LEYLANDSTILE':'STILE'},inplace=True)
#AUDI
df.model.replace({'AUDI-A4':'A4','AUDI-A8':'A8','AUDI-Q5':'Q5','AUDI-A6':'A6'},inplace=True)
Z=df[df.make=='AUDI']
df.model.replace({'BMW-3SERIES':'3SERIES','BMW-5SERIES':'5SERIES','BMW-7SERIES':'7SERIES'},inplace=True)
df.model.replace({'CARS-HONDA-CITY':'CITY','CARS-HONDA-AMAZE':'AMAZE','CARS-HONDA-ACCORD':'ACCORD','CARS-HONDA-CRV':'CR-V','CARS-HONDA-CIVIC':'CIVIC','CIVICHYBRID':'CIVIC','CARS-HONDA-CITY-ZX':'CITY-ZX','CARS-HONDA-BRIO':'BRIO','CARS-HONDA-WRV':'WR-V','CARS-HONDA-JAZZ':'JAZZ'},inplace=True)
Z=df[df.make=='HONDA']
df.model.replace({'CHEVROLET-BEAT':'BEAT','CHEVROLET-OPTRA':'OPTRA','CHEVROLET-ENJOY':'ENJOY','CHEVROLET-SAIL':'SAIL'},inplace=True)
df.model.replace({'DATSUN-REDI-GO1':'GO','DATSUN-GO-PLUS':'GOPLUS'},inplace=True)
df.model.replace({'GRANDPUNTO':'GRANDEPUNTO','FIAT-GRANDE-PUNTO':'GRANDEPUNTO','FIAT-PUNTO':'PUNTO'},inplace=True)
df.model.replace({'FORCE-MOTORS-FORCE-ONE':'ONE','FORCEONE':'ONE'},inplace=True)
df.model.replace({'FORD-FIESTA':'FIESTA','FORD-ECOSPORT':'ECOSPORT','FORD-FIGO':'FIGO','FORD-FIGO-ASPIRE':'FIGOASPIRE','FORD-ENDEAVOUR':'ENDEAVOUR','FORD-IKON':'IKON','FORD-FUSION':'FUSION','FORD-FIESTA-CLASSIC':'CLASSIC'},inplace=True)
df.model.replace({'HYUNDAI-CRETA':'CRETA','HYUNDAI-I20':'I20','HYUNDAI-ACCENT':'ACCENT','HYUNDAI-I10':'I10','HYUNDAI-VERNA':'VERNA','HYUNDAI-GRAND-I10':'GRANDI10','HYUNDAI-SANTRO':'SANTRO','HYUNDAI-EON':'EON','HYUNDAI-SANTRO-XING':'SANTROXING','HYUNDAI-ELITE-I20':'ELITEI20','HYUNDAI-GRAND-I10-NIOS':'GRANDI10NIOS','HYUNDAI-FLUIDIC-VERNA':'FLUIDICVERNA','HYUNDAI-XCENT':'XCENT','HYUNDAI-ELANTRA':'ELANTRA','HYUNDAI-SONATA':'SONATA','HYUNDAI-I20-ACTIVE':'I20ACTIVE','HYUNDAI-GRAND-I-10':'GRANDI10','HYUNDAI-VENUE':'VENUE','HYUNDAI-SONATA-EMBERA':'SONATAEMBERA','HYUNDAI-SANTA-FE':'SANTAFE','KONAELECTRIC':'KONA','HYUNDAI-GETZ-PRIME':'GETZPRIME'},inplace=True)
Z=df[df.make=='HYUNDAI'].model.value_counts()
df.model.replace({'ISUZU-D-MAX':'D-MAX'},inplace=True)
df.model.replace({'JEEP-COMPASS':'COMPASS'},inplace=True)
df.model.replace({'KIA-SELTOS':'SELTOS','KIA-SONET':'SONET'},inplace=True)
df.model.replace({'MAHINDRA-SCORPIO':'SCORPIO','MAHINDRA-THAR':'THAR','MAHINDRA-XUV500':'XUV500','MAHINDRA-REXTON':'REXTON','MAHINDRA-BOLERO':'BOLERO','MAHINDRA-LOGAN':'LOGAN','MAHINDRA-KUV-100':'KUV100','SCORPIOGETAWAY':'SCORPIO','MAHINDRA-TUV':'TUV','MAHINDRA-EKUV100':'EKUV100','MAHINDRA-XUV300':'XUV300','MAHINDRA-MARAZZO':'MARAZZO','MAHINDRA-WILLYS':'WILLYS','MAHINDRA-XUV700':'XUV700','MAHINDRA-E-VERITO':'EVERITO','MAHINDRA-JEEP':'JEEP','MAHINDRA-QUANTO':'QUANTO','MAHINDRA-XYLO':'XYLO','MAHINDRA-SSANGYONG-REXTON':'SSANGYONGREXTON','U321MPV':'MARAZZO'},inplace=True)
Z=df[df.make=='MAHINDRARENAULT'].model.value_counts()
df.model.replace({'MARUTI-SUZUKI-VERSA':'VERSA','VERNA':'VERSA','MARUTI-SUZUKI-WAGON-R':'WAGONR','MARUTI-SUZUKI-SWIFT':'SWIFT','MARUTI-SUZUKI-RITZ':'RITZ','MARUTI-SUZUKI-ZEN-ESTILO':'ZENESTILO','WAGONR1.0':'WAGONR','MARUTI-SUZUKI-SWIFT-DZIRE':'SWIFTDZIRE','MARUTI-SUZUKI-CELERIO':'CELERIO','MARUTI-SUZUKI-GYPSY':'GYPSY','MARUTI-SUZUKI-WAGON-R-1-0':'WAGONR','MARUTI-SUZUKI-800':'800','MARUTI-SUZUKI-ESTILO':'ESTILO','MARUTI-SUZUKI-CELERIO-X':'CELERIOX','WAGONRDUO':'WAGONR','MARUTI-SUZUKI-BALENO':'BALENO','MARUTI-SUZUKI-ALTO':'ALTO','MARUTI-SUZUKI-ALTO-800':'ALTO800','MARUTI-SUZUKI-OMNI':'OMNI','WAGONRELECTRIC':'WAGONR','MARUTI-SUZUKI-S-CROSS1':'SCROSS','MARUTI-SUZUKI-ALTO-K10':'ALTOK10','MARUTI-SUZUKI-CIAZ-S':'CIAZS','MARUTI-SUZUKI-VITARA-BREZZA':'VITARABREZZA','MARUTI-SUZUKI-S-PRESSO':'SPRESSO','MARUTI-SUZUKI-WAGON-R-STINGRAY':'WAGONR','MARUTI-SUZUKI-WAGON-R-DUO':'WAGONR','S-PRESSO(FUTURES)':'SPRESSO','MARUTI-SUZUKI-WAGON-R-ELECTRIC':'WAGONR','MARUTI-SUZUKI-XL6':'XL6'},inplace=True)
Z=df[df.make=='MARUTISUZUKI'].model.value_counts()
df.model.replace({'MARUTI-SUZUKI-SWIFT-DZIRE-TOUR':'SWIFTDZIRETOUR','MARUTI-SUZUKI-IGNIS':'IGNIS','MARUTI-SUZUKI-EECO':'EECO','MARUTI-SUZUKI-CIAZ':'CIAZ','MARUTI-SUZUKI-ZEN':'ZEN','MARUTI-SUZUKI-ERTIGA':'ERTIGA','MARUTI-SUZUKI-SX4':'SX4'},inplace=True)
df.model.replace({'5DOOR':'COOPER5DOOR','3DOOR':'COOPER5DOOR','CLUBMAN':'COOPERCLUBMAN'},inplace=True)
df.model.replace({'GLACLASS':'GLA','C-CLASS':'CCLASS','MB-CLASS':'BCLASS','MERCEDES-BENZ-M-CLASS':'M-CLASS','CLS':'CLS-CLASS','GCLASS':'G','MERCEDES-BENZ-E-CLASS':'E-CLASS','MLCLASS':'MCLASS','MERCEDES-BENZ-S-CLASS':'S-CLASS','ECLASS':'E-CLASS','MERCEDES-BENZ-A-CLASS':'ACLASS','MERCEDES-BENZ-GLA-CLASS':'GLA','MERCEDES-BENZ-CLA-CLASS':'CLA','MERCEDES-BENZ-C-CLASS':'CCLASS','GLECOUPE':'GLECLASS','C250AMG':'CCLASS','MERCEDES-BENZ-B-CLASS':'BCLASS'},inplace=True)
Z=df[df.make=='MERCEDESBENZ'].model.value_counts()
df.model.replace({'MITSUBISHI-PAJERO':'PAJERO','MITSUBISHI-MONTERO':'MONTERO'},inplace=True)
df.model.replace({'DATSUNREDIGO':'REDIGO','NISSAN-MICRA':'MICRA','NISSAN-TERRANO':'TERRANO','NISSAN-MICRA-ACTIVE':'MICRAACTIVE','GTR':'GT-R','NISSAN-DATSUN-REDI-GO':'REDIGO','NISSAN-SUNNY':'SUNNY'},inplace=True)
Z=df[df.make=='NISSAN'].model.value_counts()
df.model.replace({'OPELCORSA':'CORSA','OPEL-ASTRA':'ASTRA'},inplace=True)
df.model.replace({'118NE':'NE118'},inplace=True)
df.model.replace({'RENAULT-KOLEOS':'KOLEOS','RENAULT-KWID':'KWID','RENAULT-CAPTUR':'CAPTUR','RENAULT-DUSTER':'DUSTER'},inplace=True)
df.model.replace({'SKODA-RAPID':'RAPID','SKODA-OCTAVIA':'OCTAVIA','SKODA-FABIA':'FABIA','SKODA-SUPERB':'SUPERB','SKODA-LAURA':'LAURA'},inplace=True)
df.model.replace({'TATA-SAFARI-STORME':'SAFARISTORME','TATA-INDICA':'INDICA','TATA-MANZA':'MANZA','TATA-SAFARI':'SAFARI','TATA-INDICA-V2-XETA':'INDICAV2XETA','TATA-INDICA-VISTA':'INDICAVISTA','TATA-NEXON':'NEXON','TATA-INDICA-V2':'INDICAV2','TATA-TIAGO':'TIAGO','INDICAB':'INDICA','TATA-NANO':'NANO','TATA-ZEST-':'ZEST','TATA-HEXA':'HEXA','SUMOGRANDEMKII':'SUMOGRANDE','TIAGOEV':'TIAGO','TATA-SUMO-GRANDE':'SUMOGRANDE','TATA-INDICA-E-V2':'INDICAEV2','TATA-TIGOR':'TIGOR','TATA-INDIGO-CS':'INDIGOCS','TATA-INDIGO':'INDIGO'},inplace=True)
Z=df[df.make=='TATA'].model.value_counts()
df.model.replace({'TATA-ARIA':'ARIA','TATA-BOLT':'BOLT'},inplace=True)
df.model.replace({'TOYOTA-INNOVA':'INNOVA','TOYOTA-GLANZA':'GLANZA','TOYOTA-ETIOS-LIVA':'ETIOSLIVA','TOYOTA-FORTUNER':'FORTUNER','TOYOTA-INNOVA-CRYSTA':'INNOVACRYSTA','TOYOTA-COROLLA':'COROLLA','TOYOTA-COROLLA-ALTIS':'COROLLAALTIS','TOYOTA-QUALIS':'QUALIS'},inplace=True)
Z=df[df.make=='TOYOTA'].model.value_counts()
df.model.replace({'TOYOTA-ETIOS':'ETIOS'},inplace=True)
df.model.replace({'VOLKSWAGEN-JETTA':'JETTA','VOLKSWAGEN-VENTO':'VENTO','VOLKSWAGEN-POLO':'POLO','VOLKSWAGEN-MULTIVAN':'MULTIVAN','VOLKSWAGEN-GTI':'GTI','VOLKSWAGEN-AMEO':'AMEO','VOLKSWAGEN-CROSS-POLO':'CROSSPOLO','TAIGUN':'TIGUAN'},inplace=True)
Z=df[df.make=='VOLKSWAGEN'].model.value_counts()
df.model.replace({'VOLVO-XC-90':'XC90','VOLVO-XC60':'XC60','A60':'S60','VOLVO-S60':'S60'},inplace=True)
i=0
for i in df[(df.make=='ASTONMARTIN') & (df.model=='SANTROXING')].index:
    df['make'][i]='HYUNDAI'
i=0
for i in df[(df.make=='ALTO800')].index:
    df['make'][i]='MARUTIZUZUKI'
    df['model'][i]='ALTO800'

i=0
for i in df[(df.make=='BALENO')].index:
    df['make'][i]='MARUTIZUZUKI'
    df['model'][i]='BALENO'
    
i=0
for i in df[(df.make=='BMW') & (df.model=='EON')].index:
    df['make'][i]='HYUNDAI'
    print(df['make'][i])

i=0
for i in df[(df.make=='HONDA') & (df.model=='BMAX')].index:
    df['make'][i]='FORD'

i=0
for i in df[(df.make=='CHEVROLET') & (df.model=='I20')].index:
    df['make'][i]='HYUNDAI'

i=0
for i in df[(df.make=='FIAT') & (df.model=='PUNTOABARTH')].index:
    df['make'][i]='ABARTH'

i=0
for i in df[(df.make=='DZIRE')].index:
    df['make'][i]='MARUTIZUZUKI'
    df['model'][i]='DZIRE'

i=0
for i in df[(df.model=='HINDUSTAN-MOTORS-OTHERS')].index:
    df['model'][i]='OTHERS'

i=0
for i in df[(df.model=='AMBASSADOR')|(df.make=='AMBASSADOR')].index:
    df['model'][i]='AMBASSADOR'
    df.make[i]='HINDUSTANMOTORS'
    
i=0
for i in df[(df.make=='HYUNDAI') & (df.model=='SWIFT')].index:
    df['make'][i]='MARUTISUZUKI'
   
i=0
for i in df[(df.make=='HYUNDAI') & (df.model=='AMAZE')].index:
    df['make'][i]='HONDA'
    
i=0
for i in df[(df.model=='MAHINDRA-OTHERS')].index:
    df['model'][i]='OTHERS'

i=0
for i in df[(df.make=='MERCEDESBENZ') & (df.model=='SWIFT')].index:
    df['make'][i]='MARUTISUZUKI'

i=0
for i in df[(df.make=='MERCEDESBENZ') & (df.model=='ECOSPORT')].index:
    df['make'][i]='FORD'
    

#filling null and other categories of cars    
i=0
for i in df[(df.model.isna())|(df.model=='OTHERS')].index:
    if df[(df.make==df.make[i])].model.mode().notnull().any(): 
        df.model[i]=df[(df.make==df.make[i])].model.mode()[0]
        print(df[(df.make==df.make[i])].model.mode()[0],'and',df.model[i])

#After running the loop, 17 rows of model has 'OTHERS' while 3 rows are null
Z=df[df.model=='OTHERS']
#make consists of otherbrands, tesla, mazda
df.drop(labels=['OTHERBRANDS'])
df.drop(df[(df.make=='OTHERBRANDS') & (df.model=='OTHERS')].index,inplace=True)

df.make.replace('MAHINDRARENAULT','MAHINDRA',inplace=True)
df.model.replace('VERSA','VERNA',inplace=True)
#case when mode is 'OTHERS'
i=0
for i in df[(df.model.isna())|(df.model=='OTHERS')].index:
    if df[(df.make==df.make[i])].model.mode().notnull().any(): 
        df.model[i]=df[(df.make==df.make[i])].model.value_counts().index.tolist()[1]
        print(df[(df.make==df.make[i])].model.value_counts().index.tolist()[1],'and',df.model[i])
        

Z=df[df.model.isna()]
len(df[df.model=='MIATA'])
len(df[df.model=='RX8'])
df.model.replace('OTHERS','MIATA',inplace=True)

df.dropna(subset=['model'],inplace=True)

df2=pd.read_csv('type_calculated.csv')
df['type']=pd.Series([],dtype=object)
df['transmission']=pd.Series([],dtype=object)

#getting type and transmission type of the car
i=0
for i in df[df.transmission.isna()].index:
    if df2[(df2.make==df.make[i]) & (df2.model==df.model[i])].index.notnull().any(): 
        j=df2[(df2.make==df.make[i]) & (df2.model==df.model[i])].index[0]
        df['type'][i]=df2.type[j]
        df['transmission'][i]=df2.Transmission_Type[j]
        print(j,'amd',df['type'][i],'and',df['transmission'][i])

               

Z=df[df.transmission.isna()].drop_duplicates(['make','model'])
df.to_csv('half_cleaned_data.csv')
df.dropna(subset=['transmission'],inplace=True)


#KNN imputation for numerical methods
df.drop(columns=['Unnamed: 0'],inplace=True)
numerical_cols=df.select_dtypes(include=np.number).columns.tolist()
del numerical_cols[11]
df['age']=df['inspection_year']-df['year_y']

df.to_csv('fully_cleaned_data.csv')


######################## detecting outliers ###############################
import matplotlib.pyplot as plt
df1=pd.read_csv(r'C:\Users\NidhiGoyal\.spyder-py3\half_cleaned_data.csv')
#df2=pd.read_csv('fully_cleaned_data.csv')

#target price
plt.boxplot(df2[df2['mx_target_price']<832100].mx_target_price,notch=True,patch_artist=True)
df1.describe(percentiles=[0.01,0.03,0.05,0.95,0.97,0.99])
df3=df1[df1.mx_target_price>10000000]    #remove one zero from the back : 16 rows
i=0
for i in df1[df1.mx_target_price>10000000].index:
    df1['mx_target_price'][i]/=10
df1.mx_target_price.describe(percentiles=[0.01,0.03,0.05,0.95,0.97,0.99])
df1.mx_target_price.replace(0,np.nan,inplace=True)
#capping with 99th percentile and 1st percentile
df1.loc[df1.mx_target_price>df1.mx_target_price.quantile(0.99),'mx_target_price']=df1.mx_target_price.quantile(0.99)
df1.loc[df1.mx_target_price<df1.mx_target_price.quantile(0.01),'mx_target_price']=df1.mx_target_price.quantile(0.01)
    

#km
df3=df2[df2.mileage<1000]  #1349 : so this is not mileage
df1[['mx_km','mileage']].max(axis=1).describe(percentiles=[0.01,0.03,0.05,0.95,0.97,0.99])
df1.mx_km.replace(0,np.nan,inplace=True)
df1.mileage.replace(0,np.nan,inplace=True)
#capping
df1['km']=df1[['mx_km','mileage']].max(axis=1)
df1.loc[df1.km>df1.km.quantile(0.97),'km']=df1.km.quantile(0.97)
df1.loc[df1.km<df1.km.quantile(0.03),'km']=df1.km.quantile(0.03)

#age capping 
df1[df1.age<2022].describe()
#analyse age by inspecting year_y column
len(df2[df2.age>30])   #219
#replace year_y by np nan
df3=df2[df2.age>40]   #19 rows
df1.loc[df1.year_y<1980,'year_y']=df1.year_y.quantile(0.005)
df1.loc[df1.year_y>2021,'year_y']=df1.year_y.quantile(0.995)
df1['type']=df1['type'].fillna(df2['type'])
df1['transmission']=df1['transmission'].fillna(df2['transmission'])

#cubiccapacity capping
df1.loc[df1.cubiccapacity>df1.cubiccapacity.quantile(0.95),'cubiccapacity']=df1.cubiccapacity.quantile(0.95)
df1.loc[df1.cubiccapacity<df1.cubiccapacity.quantile(0.05),'cubiccapacity']=df1.cubiccapacity.quantile(0.05)

#updations in make and model
i=0
for i in df1[(df1.make=='INFINITI')].index:
    df1['make'][i]='NISSAN'
    df1['model'][i]='INFINITI'

i=0
for i in df1[(df1.make=='SAN') & (df1.model=='ALTOK10')].index:
    df1['make'][i]='MARUTISUZUKI'

i=0
for i in df1[(df1.make=='SWIFT')].index:
    df1['make'][i]='MARUTIZUZUKI'
    df1['model'][i]='SWIFT'
    
i=0
for i in df1[(df1.make=='WAGONR')].index:
    df1['make'][i]='MARUTIZUZUKI'
    df1['model'][i]='WAGONR'

i=0
for i in df1[(df1.make=='XUV500')].index:
    df1['make'][i]='MAHINDRA'
    df1['model'][i]='XUV500'

i=0
for i in df1[(df1.make=='SKODA') & (df1.model=='CITYCZ')].index:
    df1['model'][i]='CITIGO'

i=0
for i in df1[(df1.make=='OTHERBRANDS') & (df1.model=='WAGONR')].index:
    df1['make'][i]='MARUTISUZUKI'

i=0
for i in df1[(df1.make=='MARUTISUZUKI') & (df1.model=='VERNA')].index:
    df1['make'][i]='HYUNDAI'

i=0
for i in df1[(df1.make=='SKODA') & (df1.model=='CITYZX')].index:
    df1['make'][i]='HONDA'
    
i=0
for i in df1[(df1.make=='MASERATI') & (df1.model=='VITARABREZZA')].index:
    df1['make'][i]='MARUTISUZUKI'

df1.model.replace('CITY-ZX','CITYZX',inplace=True)
df1.model.replace('BMW-3-SERIES','3SERIES',inplace=True)

df1.loc[(df1.model=='STS')&(df1.make=='MARUTISUZUKI'),'make']='CADILLAC'
df1.loc[(df1.model=='ESTILO')&(df1.make=='HYUNDAI'),'make']='MARUTISUZUKI'
df1.loc[(df1.model=='REDIGO')&(df1.make=='NISSAN'),'make']='DATSUN'
df1.model.replace('ESTILLO','ESTILO',inplace=True)
df1.model.replace('HYUNDAI-GETZ','ESTILO',inplace=True)
df1.model.replace('BMW-5-SERIES','5SERIES',inplace=True)
df1.model.replace('MCLASS','M-CLASS',inplace=True)
df1.make.replace('MARUTIZUZUKI','MARUTISUZUKI',inplace=True)
df1.model.replace('BMW-7-SERIES','7SERIES',inplace=True)

df1.loc[(df1.model=='HYUNDAI-OTHERS'),'model']=df1[(df1.make=='HYUNDAI')].model.mode()[0]
df1.loc[(df1.model=='MERCEDES-BENZ-OTHERS'),'model']=df1[(df1.make=='MERCEDESBENZ')].model.mode()[0]
df1.loc[(df1.model=='.'),'model']=df1[(df1.make=='SKODA')].model.mode()[0]

df1.loc[df1.model=='PUNTOABARTH','type']='Hatchback'
df1.loc[df1.model=='PUNTOABARTH','transmission']='Auto'

df1.loc[df1.model=='LEYLANDSTILE','type']='Minivan'
df1.loc[df1.model=='LEYLANDSTILE','transmission']='Manual'
  
df1.loc[df1.model=='LM','type']='Sedan'
df1.loc[(df1.model=='LM')&(df1.make=='LEXUS'),'transmission']='Auto'  


df1.loc[(df1.make=='TOYOTA') & (df1.model=='ESTIMAEMINA'),'type']='MUV'
df1.loc[(df1.make=='TOYOTA') & (df1.model=='ESTIMAEMINA'),'transmission']='Auto'

df1.loc[(df1.make=='HINDUSTANMOTORS') & (df1.model=='CONTESSA'),'type']='Luxury'
df1.loc[(df1.make=='HINDUSTANMOTORS') & (df1.model=='CONTESSA'),'transmission']='Manual'

#getting type and transmission of the updated make and models
df3=pd.read_csv('type_calculated.csv')
i=0
for i in df1[df1.transmission.isna()].index:
    if df3[(df3.make==df1.make[i]) & (df3.model==df1.model[i])].index.notnull().any(): 
        j=df3[(df3.make==df1.make[i]) & (df3.model==df1.model[i])].index[0]
        df1['type'][i]=df3.type[j]
        df1['transmission'][i]=df3.Transmission_Type[j]
        print(j,'amd',df1['type'][i],'and',df1['transmission'][i])

df1.dropna(subset=['model'],inplace=True)


from sklearn.impute import KNNImputer
knn=KNNImputer()
numerical_cols=['km','mx_target_price','year_y','cubiccapacity','damagessummary', 'bodyexteriordesign', 'bodyinteriordesign']
df1[numerical_cols]=knn.fit_transform(df1[numerical_cols])

#cap mx_km or mileage by 99 percentile and 1 percentile
#define junkflag from the start

#Scaling for numerical columns
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
y=scaler.fit_transform(df1[numerical_cols])
df1['age']=df1['inspection_year']-df1['year_y']

df1.to_csv('outliers_removed+knn.csv')
#categorical columns null values have been treated
df=pd.read_csv('outliers_removed+knn.csv')
df['car']=df['make']+' '+df['model']  #562 unique cars
df.type.replace({'luxury':'Luxury','Suv':'SUV','Luxury\t':'Luxury'},inplace=True)
df.transmission.replace({'Manual/auto':'Manual/Auto','manual':'Manual','mANUAL/Auto':'Manual/Auto','auto':'Auto','aUTO':'Auto'},inplace=True)
df.type=df.type.str.replace(' ','') 
df['zone']=pd.Series([],dtype=object)

i=0
for i in df.index:
    if any(j in df.registeredcity[i] for j in ['DL','HR','UK','HP','UA']):
        df.zone[i]='NORTH'
    elif any(j in df.registeredcity[i] for j in ['KA','PY','TN','AP','TS','KL','GA']):
        df.zone[i]='SOUTH'
    elif any(j in df.registeredcity[i] for j in ['WB']):
        df.zone[i]='EAST'
    elif any(j in df.registeredcity[i] for j in ['PB','MH','GJ','RJ','CH','DD']):
        df.zone[i]='WEST'
    elif any(j in df.registeredcity[i] for j in ['UP','MP','JH','CG','BR']):
        df.zone[i]='CENTRAL'
    elif any(j in df.registeredcity[i] for j in ['AS','OD','MN','ML','AR','OR','TR','NL','MZ']):
        df.zone[i]='NORTH-EAST'
        #DD,DN,JK,AN,SK,LD,BH

df.fuel.replace({'petrolElectric':'hybrid','dieselElectric':'hybrid','diesel/hybrid':'hybrid','petrol/hybrid':'hybrid'},inplace=True) 
     
df1=df[['make','mx_target_price','fuel','type', 'transmission', 'km','age','cubiccapacity','insurancetype','numberofowners','zone','caronhypothecation','chassiscolor','damagessummary','bodyexteriordesign', 'bodyinteriordesign']]
df.caronhypothecation=df.caronhypothecation.map({True:1,False:0})
df1.to_csv('new_clustering_data.csv')


    

    

