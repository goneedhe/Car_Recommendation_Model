#importing libraries
import psycopg2
import pandas as pd

#establishing connection with database
connection_string = "host='doppler.c4nfnb3d0ywp.eu-west-1.redshift.amazonaws.com' dbname='panameraods' user='nidhi_goyal' password='cUNXrIhMNc6GsMg#1' port='5439'"
conn_pg = psycopg2.connect(connection_string)

#saving inspection file from southasia_cmc_sandbox.fcg_inspectionreport to csv called inspection
df6=pd.read_sql("select inspection_date,fuel,make,year,model,price,mileage,location,odometer,roadtaxpaid,cubiccapacity,insurancetype,numberofowners,registeredcity,roadtaxvalidity,manufacturingdate,caronhypothecation,registrationnumber,chassiscolor,insurancetype,damagessummary,pricewebsitequote,bodyexteriordesign,bodyinteriordesign from southasia_cmc_sandbox.fcg_inspectionreport;",conn_pg).to_csv('inspection.csv')
#reading inspection data from csv with date-time dtype
df7=pd.read_csv(r'C:\Users\NidhiGoyal\.spyder-py3\inspection.csv',parse_dates=['inspection_date'])

#fetching data for last 2.5 years
df7['inspection_year']=pd.to_datetime(df7['inspection_date']).dt.year
df8=df7[df7['inspection_year']>2019]

#df6=pd.read_sql("select inspection_date;",conn_pg).to_csv('inspection.csv')
#saving price details from southasia_cmc_sandbox.ods_leads_inc to csv called price
df=pd.read_sql("select location,createdon,mx_target_price ,mx_km, mx_price_offered_to_customer , mx_make ,mx_model, mx_final_buying_price , mx_final_selling_price, mx_reg_no, min_quote_price , max_quote_price,junkflag from southasia_cmc_sandbox.ods_leads_inc;",conn_pg).to_csv('price.csv')
#saving price data into csv with date-time dtype
df9=pd.read_csv(r'C:\Users\NidhiGoyal\.spyder-py3\price.csv',parse_dates=['createdon'])
#fetching data for last 2.5 years
df9['year']=pd.to_datetime(df9['createdon']).dt.year
df10=df9[df9['year']>2019]
#taking registration number as identifier
df11=df8.dropna(subset=['registrationnumber'])
df8.registrationnumber=df8.registrationnumber.str.upper()
df8.registrationnumber=df8.registrationnumber.str.replace(' ','')
t=df8.registrationnumber.value_counts()
df10.mx_reg_no=df10.mx_reg_no.str.upper()
df10.mx_reg_no=df10.mx_reg_no.str.replace(' ','')

#to determine if there

df12=df10.dropna(subset=['mx_reg_no'])

#taking prices from price data
df15=pd.merge(df12,df11,left_on='mx_reg_no',right_on='registrationnumber',how="right")
#retrieving rows from inspection data which were not included in df15
df14=df8[df8.registrationnumber.isnull()]
#database with max possible price values
df16=pd.concat([df15,df14],ignore_index=True)


#dropping reducndant dataframes
del df7,df9,df11,df12,df14

#checking columns distinct values
for i in df16.columns.tolist():
    print(df16[i].value_counts())

#counting non null values
for i in df16.columns.tolist():
    print(i,df16[i].isnull().sum())

#removing null columns and useless columns
df16.drop(columns=['Unnamed: 0_x','inspection_date','Unnamed: 0'],inplace=True)
pd. set_option('display.max_columns', 500)
#saving dataframe to raw_data.csv
df16.to_csv("raw_data.csv")
         
#removing cars with no make or model
df17=df16.dropna(subset=['mx_make','make','mx_model','model'],how='all')
df17['fuel_original']=df16.dropna(subset=['mx_make','make','mx_model','model'],how='all').fuel
df17.registeredcity.isna().sum()    #20099

    
len(df17[df17.make.notnull()])      #779565
len(df17[df17.make.isna() & df17.mx_make.notnull()])  #277

#combining make and models
i=0
for i in df17[df17.model.isna() & df17.mx_model.notnull()].index:
    df17.loc[i,'model']=df17.loc[i,'mx_model']
i=0
for i in df17[df17.make.isna() & df17.mx_make.notnull()].index:
    df17.loc[i,'make']=df17.loc[i,'mx_make']

df17=df17.dropna(columns=['mx_make','mx_model'])
            
df17.make=df17.make.str.upper()
df17.model=df17.model.str.upper()

#mapping fueltype
df17.fuel=df17.fuel.map({'diesel/hybrid':'diesel/hybrid','inspection.field.option.petrolElectric':'petrolElectric',
                         'inspection.field.option.dieselElectric':'dieselElectric','petrol/hybrid':'petrol/hybrid',
                         'inspection.field.option.petrol':'petrol','Petrol':'petrol','inspection.field.fuelType.petrol':'petrol',
                         'PETROL':'petrol','selfInspection.field.option.petrol':'petrol','inspection.field.option.diesel':'diesel'
                         ,'Diesel':'diesel','inspection.field.fuelType.diesel':'diesel','DIESEL':'diesel',
                         'Electric':'elecric','inspection.field.fuelType.electric':'electric','electric(bov)':'electric',
                         'CNG':'cng','selfInspection.field.option.cng':'cng','inspection.field.option.compressedNaturalGas':'cng',
                         'inspection.field.fuelType.CGN':'cng','cng only':'cng','inspection.field.option.petrolCompressedNaturalGas':'cng_petrol',
                         'inspection.field.fuelType.CGNpetrol':'cng_petrol','cng petrol':'cng_petrol','CNGPETROL':'cng_petrol',
                         'inspection.field.option.petrolLiquifiedPetroleumGas':'lpg_petrol','inspection.field.fuelType.LPGpetrol':'lpg_petrol',
                         'petrol/lpg':'lpg_petrol','LPGPETROL':'lpg_petrol','petrol lpg':'lpg_petrol',
                         'inspection.field.option.liquifiedPetroleumGas':'lpg','lpg only':'lpg'})


df17.registrationnumber.nunique()   #    
len(df17[df17.registrationnumber.isna()]) #327857
#duplicates=34198
df17=df17.drop_duplicates(subset=['model','make','registrationnumber','mx_target_price','inspection_year','year_y','fuel'])

######################## extracting location ##################################

#len(df17[df17.city.isna() & df17.registrationnumber.notnull()])     #0
#len(df17[df17.city.isna() & df17.location_x.notnull()])    #0
#len(df17[df17.city.notnull() & df17.location_y.isna()])         #402    
#len(df17[df17.city.isna() & df17.registrationnumber.notnull()]) #1001
#df17.city.fillna(df17.registrationnumber[i][0:2],inplace=True)
#x=df17.city.value_counts()

#city column has max cities
df17.city.isna().sum()      #0

df17.registeredcity=df17.registeredcity.str.upper()
#mapping for location

i=0
for i in df17.loc[df17.registeredcity=='KARNATAKA'].index:
    df17.registeredcity[i]='KA'
i=0
for i in df17.loc[df17.registeredcity=='WEST BENGAL'].index:
    df17.registeredcity[i]='WB'
i=0
for i in df17.loc[(df17.registeredcity=='GUJARAT')|(df17.registeredcity=='AHMEDABAD')].index:
    df17.registeredcity[i]='GJ'
i=0
for i in df17.loc[df17.registeredcity=="DELHI"].index:
    df17.registeredcity[i]='DL'
i=0
for i in df17.loc[(df17.registeredcity=='ASSAM')|(df17.registeredcity=='AASAM')|(df17.registeredcity=='ASAM')|(df17.registeredcity=='ASSAM (GUWAHATI - KAMRUP)')|(df17.registeredcity=='ASSSAM')|(df17.registeredcity=='AS01BW7350')|(df17.registeredcity=='AS01DB1903')].index:
    df17.registeredcity[i]='AS'
i=0
for i in df17.loc[df17.registeredcity=='MAHARASHTRA'].index:
    df17.registeredcity[i]='MH'    
i=0    
for i in df17.loc[df17.registeredcity=='HARYANA'].index:
    df17.registeredcity[i]='HR'
i=0
for i in df17.loc[df17.registeredcity=='PUNJAB'].index:
    df17.registeredcity[i]='PB'
i=0
for i in df17.loc[df17.registeredcity=='CHANDIGHAR'].index:
    df17.registeredcity[i]='CH'
i=0
for i in df17.loc[(df17.registeredcity=='RAJASTHAN')|(df17.registeredcity=='RAJSTHAN')].index:
    df17.registeredcity[i]='RJ' 
i=0
for i in df17.loc[(df17.registeredcity=='KARNATKA')|(df17.registeredcity=='KA04MM2323')].index:
    df17.registeredcity[i]='KA' 
i=0
for i in df17.loc[(df17.registeredcity=='ODISHA')|(df17.registeredcity=='ORISSA')|(df17.registeredcity=='ORISSA STATE')].index:
    df17.registeredcity[i]='OD'
i=0
for i in df17.loc[df17.registeredcity=='UTTARANCHAL'].index:
    df17.registeredcity[i]='UK'
i=0
for i in df17.loc[(df17.registeredcity=='TELENGANA')|(df17.registeredcity=='TN01AZ3892')|(df17.registeredcity=='TELANGANA')].index:
    df17.registeredcity[i]='TS'
i=0
for i in df17.loc[(df17.registeredcity=='ANDAMAN & NICOBAR ISLAND')|(df17.registeredcity=='ANDAMAN & NICOBAR')|(df17.registeredcity=='ANDAMAN NICOBAR ISLANDS')].index:
    df17.registeredcity[i]='AN'
i=0
for i in df17.loc[(df17.registeredcity=='UP15CD2623')|(df17.registeredcity=='UTTAR PRADESH')|(df17.registeredcity=='UP16')].index:
    df17.registeredcity[i]='UP'
v=df17.registeredcity.value_counts()

#damagesummary
df17.damagessummary.isna().sum()        #324554
df17.damagessummary.value_counts()
df17.no_of_damages=pd.Series([],dtype=int)
i=0
for i in df17.loc[df17.damagessummary.notnull()].index:
    df17['damagessummary'][i]=(len(str(df17['damagessummary'][i]))//10)

#color feature
z=df17.chassiscolor.value_counts()
df17.chassiscolor=df17.chassiscolor.str.lower()
i=0
df17.color=pd.Series([],dtype=object)
a=['wh','whi','whte','sil','alabaster','wt','metallic','platinum','beige']
b=['blac','blk','granite','carbon']    
j=''
i=0
for i in df17[df17.chassiscolor.notnull()].index:
    if any(j in df17.chassiscolor[i] for j in a):
        df17.chassiscolor[i]='whitish'
    elif any(j in df17.chassiscolor[i] for j in b):
        df17.chassiscolor[i]='blacksh'
    elif 'red' in df17.chassiscolor[i]:
        df17.chassiscolor[i]='reddish'
    elif 'blue' in df17.chassiscolor[i]:
        df17.chassiscolor[i]='blueish'
    elif any(j in df17.chassiscolor[i] for j in ['yellow','gold']):
        df17.chassiscolor[i]='yellowish'
    elif 'green' in df17.chassiscolor[i]:
        df17.chassiscolor[i]='greenish'
    elif any(j in df17.chassiscolor[i] for j in ['brow','bronze','copper','choco','pearl met']):
        df17.chassiscolor[i]='brownish'
    elif any(j in df17.chassiscolor[i] for j in ['grey','dust','titanium']):
        df17.chassiscolor[i]='greyish'

i=0
for i in df17[(df17.chassiscolor.notnull())].index:
    if 'ish' not in df17.chassiscolor[i]:
        if any(j in df17.chassiscolor[i] for j in ['bieg','beig','beid','ivory','earth','chill','cashmere','slvr','dew','mist','sivl','sliv','b diam']):
            df17.chassiscolor[i]='whitish'
        elif any(j in df17.chassiscolor[i] for j in ['blck','graphite','balck','corbon']):
            df17.chassiscolor[i]='blacksh'
        elif any(j in df17.chassiscolor[i] for j in ['champ','burgandy','r ','wine','maroon','brunello','passion','pink','brick','blazing r']):
            df17.chassiscolor[i]='reddish'
        elif any(j in df17.chassiscolor[i] for j in ['aqua','starr','blu','teal','ocean','breeze']):
            df17.chassiscolor[i]='blueish'
        elif any(j in df17.chassiscolor[i] for j in ['mustard','orange','canyon','mustard']):
            df17.chassiscolor[i]='yellowish'
        elif any(j in df17.chassiscolor[i] for j in ['squeeze','foliage','gr']):
            df17.chassiscolor[i]='greenish'
        elif any(j in df17.chassiscolor[i] for j in ['brw','bron','deep','choc']):
            df17.chassiscolor[i]='brownish'
        elif any(j in df17.chassiscolor[i] for j in ['gray','smoke']):
            df17.chassiscolor[i]='greyish'

i=0
for i in df17[(df17.chassiscolor.notnull())].index:
    if 'ish' not in df17.chassiscolor[i]:
        if any(j in df17.chassiscolor[i] for j in ['purp','prp','viol','pink','lav']):
            df17.chassiscolor[i]='purplish'
        elif any(j in df17.chassiscolor[i] for j in ['organ','tan','yel','gol','sun','sand']):
            df17.chassiscolor[i]='yellowish'
        elif any(j in df17.chassiscolor[i] for j in ['met','sw','havanna']):
            df17.chassiscolor[i]='greyish'
        elif any(j in df17.chassiscolor[i] for j in ['aqu','celes']):
            df17.chassiscolor[i]='bluish'
        elif any(j in df17.chassiscolor[i] for j in ['bl','night','caviar']):
            df17.chassiscolor[i]='blacksh'
        elif any(j in df17.chassiscolor[i] for j in ['cooper','titan','quartz']):
            df17.chassiscolor[i]='brownish'
        elif any(j in df17.chassiscolor[i] for j in ['w ','abs','siv','eart','slv','pearl','spark','plat','spark']):
            df17.chassiscolor[i]='whitish'
        elif any(j in df17.chassiscolor[i] for j in [' r','scarlet','burg','maha','re','orc','win']):
            df17.chassiscolor[i]='reddish'
            
for i in df17[(df17.chassiscolor.notnull())].index:
    if 'ish' not in df17.chassiscolor[i]:
        if any(j in df17.chassiscolor[i] for j in ['p ']):
            df17.chassiscolor[i]='purplish'
        elif any(j in df17.chassiscolor[i] for j in ['organ','tan','yel','gol','sun','sand']):
            df17.chassiscolor[i]='yellowish'
        elif any(j in df17.chassiscolor[i] for j in ['glisten','kyara','ste']):
            df17.chassiscolor[i]='greyish'
        elif any(j in df17.chassiscolor[i] for j in ['aqu','celes','topaz','mari','serene','lake']):
            df17.chassiscolor[i]='bluish'
        elif any(j in df17.chassiscolor[i] for j in ['b b m']):
            df17.chassiscolor[i]='blacksh'
        elif any(j in df17.chassiscolor[i] for j in ['bake']):
            df17.chassiscolor[i]='brownish'
        elif any(j in df17.chassiscolor[i] for j in ['s ','tit','mush','cr.w','tw']):
            df17.chassiscolor[i]='whitish'
        elif any(j in df17.chassiscolor[i] for j in ['ina','carnelian']):
            df17.chassiscolor[i]='reddish'
        elif any(j in df17.chassiscolor[i] for j in ['g ',' g']):
            df17.chassiscolor[i]='greenish'
df17.chassiscolor=df17.chassiscolor.replace('blueish','bluish')        
#removing non-recognizable colors with very low frequency
df17.chassiscolor=df17.chassiscolor.map({'whitish':"white",'blacksh':"black",'reddish':"red",'bluish':"blue",'yellowish':"yellow",'greyish':"grey",'greenish':"green",'brownish':"brown",'purplish':"purple"})
        
#checking prices
len(df17.dropna(subset=['mx_target_price','mx_price_offered_to_customer','mx_final_buying_price','mx_final_selling_price','min_quote_price','max_quote_price','price','pricewebsitequote'],how='all'))
df17.count()
#mx_target_price;mx_price_offered_to_customer;mx_final_buying_price;                 397448
#mx_final_selling_price                                                              397408
#min_quote_price,max_quote_price                                                     216613
#price                                                                               455225
#pricewebsitequote               232077
len(df17[df17.price.isna() & df17.pricewebsitequote.notnull()]) #0
len(df17[df17.price.isna() & df17.max_quote_price.notnull()]) #0
len(df17[df17.price.isna() & df17.mx_final_buying_price.notnull()]) #0
#use only price column but price column consists of only 0
#drop price
#checking number of zero values in different columns
len(df17[df17.mx_final_selling_price==0])       #335341
len(df17[df17.mx_target_price==0])               #5252
len(df17[df17.mx_price_offered_to_customer==0])     #90495
len(df17[df17.min_quote_price==0])              #0
len(df17[df17.mx_target_price.isna() & df17.min_quote_price.notnull()])
#choose from mx_target_price and min_quote_price

#checking number of owners
df17.numberofowners.isna().sum()  #20794
df17.numberofowners.value_counts()
y=df17.numberofowners.map({1:1,2:2,3:3,4:4,5:5,'selfInspection.field.option.two':2,'selfInspection.field.option.one':1})
df17.numberofowners=y
    

#dealing with number of years
df17.year_y.notnull().sum()     #435492
len(df17[df17.year_y.notnull() & df17.year_x.notnull()])    #396996
len(df17[df17.year_y.notnull() & df17.inspection_year.notnull()]) #435492
# choose year_y and inspection_year 
df17.age=pd.Series([],dtype=int)
df17['age']=df17.inspection_year-df17.year_y

#drop year_x,year_y,createdon,inspection_year,inspection_date

#checking 0 values in mx_km
df17.mx_km.isna().sum()             #353923
len(df17[df17.mx_km==0])            #11273

#mileage column ready
df17.mileage.isna().sum()           #4441
len(df17[df17.mileage==0])          #1527

#insurancetype column
df17.insurancetype.isna().sum()
df17.insurancetype.value_counts()  #5 broad categories
w=df17.insurancetype.map({'thirdParty':'thirdParty','comprehensive':'comprehensive','expired':'expired','inspection.field.insuranceType.none':'none','zeroDepreciation':'zeroDepreciation','inspection.field.option.comprehensive':'comprehensive','inspection.field.insuranceType.comprehensive':'comprehensive','inspection.field.option.zeroDepreciation':'zeroDepreciation','inspection.field.option.3rdParty':'thirdParty','inspection.field.insuranceType.zeroDep':'zeroDepreciation','inspection.field.insuranceType.3rdParty':'thirdParty','ThirdParty':'thirdParty','InsuranceExpired':'expired','Comprehensive':'comprehensive','ZeroDep':'zeroDepreciation','selfInspection.field.option.expired':'expired','selfInspection.field.option.thirdParty':'thirdParty'})
df17['insurancetype']=w

#bodyexteriordesign
df17.bodyexteriordesign.isna().sum()
df17.bodyexteriordesign.value_counts()      #0/1/2/3/4/5
y=df17.bodyexteriordesign.map({'inspection.field.option.3':3,'inspection.field.option.4':4,'inspection.field.option.2':2,'3':3,'4':4,'inspection.field.option.5':5,3.0:3,'inspection.field.option.1':1,4.0:4,'2':2,'5':5,2.0:2,5.0:5,'inspection.field.option.0':0,'1':1,1.0:1,'0':0,0.0:0})

#interiorbodydesign
df17.bodyinteriordesign.value_counts()
z=df17.bodyinteriordesign.map({'inspection.field.option.3':3,'inspection.field.option.4':4,'inspection.field.option.2':2,'3':3,'4':4,'inspection.field.option.5':5,3.0:3,'inspection.field.option.1':1,4.0:4,'2':2,'5':5,2.0:2,5.0:5,'inspection.field.option.0':0,'1':1,1.0:1,'0':0,0.0:0})


df17['bodyexteriordesign']=y
df17['bodyinteriordesign']=z


#dropping unnecessary columns
df17.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'location_x', 'createdon', 'mx_price_offered_to_customer','mx_make','mx_model', 'mx_final_buying_price', 'mx_final_selling_price','min_quote_price', 'max_quote_price', 'year_x','price','odometer','roadtaxvalidity','insurancetype.1','pricewebsitequote','Unnamed: 0_y',],inplace=True)
df17.drop(columns=['location','year','mx_reg_no','location_y','manufacturingdate'],inplace=True)

#save cleaned data
df17.to_csv("cleaned_data.csv")

#roadtaxvalidity
y=df17.roadtaxpaid.value_counts()
df17.drop(columns=['year_y','inspection_year'])

"""   COLUMN NAMES  

Index(['mx_target_price', 'mx_km', 'mx_reg_no', 'junkflag', 'fuel', 'make',
       'year_y', 'model', 'mileage', 'location_y', 'roadtaxpaid',
       'cubiccapacity', 'insurancetype', 'numberofowners', 'registeredcity',
       'manufacturingdate', 'caronhypothecation', 'registrationnumber',
       'chassiscolor', 'damagessummary', 'bodyexteriordesign',
       'bodyinteriordesign', 'inspection_year', 'year', 'location','age'],
      dtype='object')
               
df16[['location_x','location_y','registeredcity','location','mx_reg_no','registrationnumber']]

"""