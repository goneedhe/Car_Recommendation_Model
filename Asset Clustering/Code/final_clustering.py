
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import scipy

#fetching data
df=pd.read_csv('outliers_removed+knn.csv')
#creating a single column for a car
df['car']=df['make']+' '+df['model']  #562 unique cars
df.type.replace({'luxury':'Luxury','Suv':'SUV','Luxury\t':'Luxury'},inplace=True)
df.transmission.replace({'Manual/auto':'Manual/Auto','manual':'Manual','mANUAL/Auto':'Manual/Auto','auto':'Auto','aUTO':'Auto'},inplace=True)
df.type=df.type.str.replace(' ','') 
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

df2=df[['car','mx_target_price','type','km','age','cubiccapacity','registeredcity','damagessummary']]
#df2 contains the true data
#defining numerical and categorical columns
df2.loc['registeredcity']=df2['registeredcity'].fillna('MH')
df2.dropna(subset=['car'],inplace=True)
numerical2=df2.select_dtypes(include=np.number)
categorical2=df2.select_dtypes(include=object)

#scaling numerical columns
#scaling numerical columns
from sklearn.preprocessing import StandardScaler
for i in numerical2.columns:
    Std=StandardScaler()
    numerical2.loc[:,i]=Std.fit_transform(np.array(numerical2[i]).reshape(-1,1))
     
#One hot Encoding Categorical Column
categorical2=pd.get_dummies(categorical2)

#combining scaled numerical columns and one hot encoded categorical columns
data2=numerical2.join(categorical2)
data2.to_csv('normalised+encoded_withreducedfeatures.csv')

#Dimentionality reduction : By PCA
from sklearn.decomposition import PCA
pca = PCA(.95)
principalComponents2 = pca.fit_transform(data2)
pd.DataFrame(principalComponents2).to_csv('principalComponents2.csv')

####clustering

#clusters=3
kmeans=KMeans(n_clusters=3).fit(principalComponents2)
kmeans_labels_for3_new2=KMeans(n_clusters=3).fit_predict(principalComponents2)

final33=df2.join(pd.DataFrame(kmeans_labels_for3_new2,columns=['label']))
grouped33=final33.groupby(by=['label'])
statistics_km_3_new2=final33.groupby(by=['label']).agg({'car':[pd.Series.mode],'mx_target_price':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'km':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'type':[pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'cubiccapacity':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'registeredcity':[pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,scipy.stats.mode]})


#clusters=4
kmeans=KMeans(n_clusters=4).fit(principalComponents2)
kmeans_labels_for4_new2=KMeans(n_clusters=4).fit_predict(principalComponents2)

final34=df2.join(pd.DataFrame(kmeans_labels_for4_new2,columns=['label']))
grouped34=final34.groupby(by=['label'])
statistics_km_4_new2=final34.groupby(by=['label']).agg({'car':[pd.Series.mode],'mx_target_price':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'km':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'type':[pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'cubiccapacity':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'registeredcity':[pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,scipy.stats.mode]})

#clusters=5
kmeans=KMeans(n_clusters=5).fit(principalComponents2)
kmeans_labels_for5_new2=KMeans(n_clusters=5).fit_predict(principalComponents2)

final35=df2.join(pd.DataFrame(kmeans_labels_for5_new2,columns=['label']))
grouped35=final35.groupby(by=['label'])
statistics_km_5_new2=final35.groupby(by=['label']).agg({'car':[pd.Series.mode],'mx_target_price':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'km':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'type':[pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'cubiccapacity':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'registeredcity':[pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,scipy.stats.mode]})

#getting clusters
cluster5_0=grouped35.get_group(0)
cluster5_1=grouped35.get_group(1)
cluster5_2=grouped35.get_group(2)
cluster5_3=grouped35.get_group(3)
cluster5_4=grouped35.get_group(4)

#saving clusters
cluster5_0.to_csv('cluster5_0.csv')
cluster5_1.to_csv('cluster5_1.csv')
cluster5_2.to_csv('cluster5_2.csv')
cluster5_3.to_csv('cluster5_3.csv')
cluster5_4.to_csv('cluster5_4.csv')


#different buckets obtained for cluster0 and cluster4 but damagessummary distinguishes the two clusters

#clusters=6
kmeans=KMeans(n_clusters=6).fit(principalComponents2)
kmeans_labels_for6_new2=KMeans(n_clusters=6).fit_predict(principalComponents2)

final36=df2.join(pd.DataFrame(kmeans_labels_for6_new2,columns=['label']))
grouped36=final36.groupby(by=['label'])
statistics_km_6_new2=final36.groupby(by=['label']).agg({'car':[pd.Series.mode],'mx_target_price':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'km':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'type':[pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'cubiccapacity':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'registeredcity':[pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,scipy.stats.mode]})

#cluster0 and cluster2 are similar on target price but differ in km,type,age
#Similarly, cluster1 and cluster5 differ in km,type,damagessummary

#clusters=7
kmeans=KMeans(n_clusters=7).fit(principalComponents2)
kmeans_labels_for7_new2=KMeans(n_clusters=7).fit_predict(principalComponents2)

final37=df2.join(pd.DataFrame(kmeans_labels_for7_new2,columns=['label']))
grouped37=final37.groupby(by=['label'])
statistics_km_7_new2=final37.groupby(by=['label']).agg({'car':[pd.Series.mode],'mx_target_price':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'km':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'type':[pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'cubiccapacity':[np.min,np.max,np.mean,np.std,scipy.stats.mode],'registeredcity':[pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,scipy.stats.mode]})

##############################################################################

#cluster1 and cluster5 differ in km,type

#Analysis for 5 clusters
#working on cluster5_0

#summary of cluster5_0
summary5_0=cluster5_0.groupby(by=['type']).agg({'mx_target_price':[np.min,np.max,np.mean,np.std,pd.Series.mode],'km':[np.min,np.max,np.mean,np.std,pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,pd.Series.mode]})
summary5_0.to_csv('summary5_0.csv')

#carlist for cluster5_0
cars5_0=cluster5_0.groupby(by=['car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars5_0.columns = cars5_0.columns.map('|'.join).str.strip('|')
count=cluster5_0.groupby(by=['car']).size()
x=cars5_0.join(pd.DataFrame(count))
x.to_csv('list_of_cars5_0.csv')

#carlist for each type
cars_bytype5_0=cluster5_0.groupby(by=['type','car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars_bytype5_0.columns = cars_bytype5_0.columns.map('|'.join).str.strip('|')
count=cluster5_0.groupby(by=['type','car']).size()
cars_bytype5_0=cars_bytype5_0.join(pd.DataFrame(count))


#plotting boxplots for km for different types
plt.rcParams['figure.dpi'] = 300

sns.boxplot(x='type',y='km',data=cluster5_0)
plt.xticks(fontsize=7)
plt.title('Boxplot for km feature for cluster5_0')

sns.boxplot(x='type',y='age',data=cluster5_0)
plt.xticks(fontsize=7)
plt.title('Boxplot for age feature for cluster5_0')

sns.boxplot(x='type',y='damagessummary',data=cluster5_0)
plt.xticks(fontsize=7)
plt.title('Boxplot for damagessummary feature for cluster5_0')

import plotly.express as px
from plotly.offline import plot
fig=px.histogram(cluster5_0,x='mx_target_price',marginal='box',nbins=50,title='Distribution of Target Price for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster5_0,x='km',marginal='box',nbins=50,title='Distribution of km reading for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster5_0,x='age',marginal='box',nbins=50,title='Distribution of Age for cluster 0')
fig.update_layout(bargap=0.1)
plot(fig)
#summary of cluster5_1
summary5_1_tp=cluster5_1.groupby(by=['type']).describe()
summary5_1_tp.to_csv('summary5_1.csv')

#carlist for cluster5_1
cars5_1=cluster5_1.groupby(by=['car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars5_1.columns = cars5_1.columns.map('|'.join).str.strip('|')
count=cluster5_1.groupby(by=['car']).size()
x=cars5_1.join(pd.DataFrame(count))
x.to_csv('list_of_cars5_1.csv')

cars_bytype5_1=cluster5_1.groupby(by=['type','car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars_bytype5_1.columns = cars_bytype5_1.columns.map('|'.join).str.strip('|')
count=cluster5_1.groupby(by=['type','car']).size()
cars_bytype5_1=cars_bytype5_1.join(pd.DataFrame(count))



#plotting boxplots for km for different types
plt.rcParams['figure.dpi'] = 300

sns.boxplot(x='type',y='km',data=cluster5_1)
plt.xticks(fontsize=7)
plt.title('Boxplot for km feature for cluster5_1')

sns.boxplot(x='type',y='age',data=cluster5_1)
plt.xticks(fontsize=7)
plt.title('Boxplot for age feature for cluster5_1')

sns.boxplot(x='type',y='damagessummary',data=cluster5_1)
plt.xticks(fontsize=7)
plt.title('Boxplot for damagessummary feature for cluster5_1')

fig=px.histogram(cluster5_1,x='mx_target_price',marginal='box',nbins=50,title='Distribution of Target Price for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster5_1,x='km',marginal='box',nbins=50,title='Distribution of km reading for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster5_1,x='age',marginal='box',nbins=50,title='Distribution of Age for cluster 1')
fig.update_layout(bargap=0.1)
plot(fig)


#summary of cluster5_2
summary5_2=cluster5_2.groupby(by=['type']).agg({'mx_target_price':[np.min,np.max,np.mean,np.std,pd.Series.mode],'km':[np.min,np.max,np.mean,np.std,pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,pd.Series.mode]})
summary5_2.to_csv('summary5_2.csv')

#carlist for cluster5_2
cars5_2=cluster5_2.groupby(by=['car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars5_2.columns = cars5_2.columns.map('|'.join).str.strip('|')
count=cluster5_2.groupby(by=['car']).size()
x=cars5_2.join(pd.DataFrame(count))
x.to_csv('list_of_cars5_2.csv')

cars_bytype5_2=cluster5_2.groupby(by=['type','car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars_bytype5_2.columns = cars_bytype5_2.columns.map('|'.join).str.strip('|')
count=cluster5_2.groupby(by=['type','car']).size()
cars_bytype5_2=cars_bytype5_2.join(pd.DataFrame(count))



#plotting boxplots for km for different types
plt.rcParams['figure.dpi'] = 300

sns.boxplot(x='type',y='km',data=cluster5_2)
plt.xticks(fontsize=7)
plt.title('Boxplot for km feature for cluster5_2')

sns.boxplot(x='type',y='age',data=cluster5_2)
plt.xticks(fontsize=7)
plt.title('Boxplot for age feature for cluster5_2')

sns.boxplot(x='type',y='damagessummary',data=cluster5_2)
plt.xticks(fontsize=7)
plt.title('Boxplot for damagessummary feature for cluster5_2')

fig=px.histogram(cluster5_2,x='mx_target_price',marginal='box',nbins=50,title='Distribution of km reading for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)


fig=px.histogram(cluster5_2,x='age',marginal='box',nbins=50,title='Distribution of Age for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)


fig=px.histogram(cluster5_2,x='km',marginal='box',nbins=50,title='Distribution of Target Price for cluster 2')
fig.update_layout(bargap=0.1)
plot(fig)

#summary of cluster5_3
summary5_3=cluster5_3.groupby(by=['type']).agg({'mx_target_price':[np.min,np.max,np.mean,np.std,pd.Series.mode],'km':[np.min,np.max,np.mean,np.std,pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,pd.Series.mode]})
summary5_3.to_csv('summary5_3.csv')

#carlist for cluster5_3
cars5_3=cluster5_3.groupby(by=['car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars5_3.columns = cars5_3.columns.map('|'.join).str.strip('|')
count=cluster5_3.groupby(by=['car']).size()
x=cars5_3.join(pd.DataFrame(count))
x.to_csv('list_of_cars5_3.csv')

cars_bytype5_3=cluster5_3.groupby(by=['type','car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars_bytype5_3.columns = cars_bytype5_3.columns.map('|'.join).str.strip('|')
count=cluster5_3.groupby(by=['type','car']).size()
cars_bytype5_3=cars_bytype5_3.join(pd.DataFrame(count))

fig=px.histogram(cluster5_3,x='mx_target_price',marginal='box',nbins=50,title='Distribution of Target Price for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster5_3,x='km',marginal='box',nbins=50,title='Distribution of km reading for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)
fig=px.histogram(cluster5_3,x='age',marginal='box',nbins=50,title='Distribution of Age for cluster 3')
fig.update_layout(bargap=0.1)
plot(fig)

#plotting boxplots for km for different types
sns.boxplot(x='type',y='km',data=cluster5_3)
plt.xticks(fontsize=7)
plt.title('Boxplot for km feature for cluster5_3')

sns.boxplot(x='type',y='age',data=cluster5_3)
plt.xticks(fontsize=7)
plt.title('Boxplot for age feature for cluster5_3')

sns.boxplot(x='type',y='damagessummary',data=cluster5_3)
plt.xticks(fontsize=7)
plt.title('Boxplot for damagessummary feature for cluster5_3')

#summary of cluster5_4
summary5_4=cluster5_4.groupby(by=['type']).agg({'mx_target_price':[np.min,np.max,np.mean,np.std,pd.Series.mode],'km':[np.min,np.max,np.mean,np.std,pd.Series.mode],'age':[np.min,np.max,np.mean,np.std,pd.Series.mode],'damagessummary':[np.min,np.max,np.mean,np.std,pd.Series.mode]})
summary5_4.to_csv('summary5_4.csv')

#carlist for cluster5_4
cars5_4=cluster5_4.groupby(by=['car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars5_4.columns = cars5_4.columns.map('|'.join).str.strip('|')
count=cluster5_4.groupby(by=['car']).size()
x=cars5_4.join(pd.DataFrame(count))
x.to_csv('list_of_cars5_4.csv')

cars_bytype5_4=cluster5_4.groupby(by=['type','car']).agg({'km':[np.mean],'age':[np.mean],'damagessummary':[np.mean]})
cars_bytype5_4.columns = cars_bytype5_4.columns.map('|'.join).str.strip('|')
count=cluster5_4.groupby(by=['type','car']).size()
cars_bytype5_4=cars_bytype5_4.join(pd.DataFrame(count))


#plotting boxplots for km for different types
sns.boxplot(x='type',y='km',data=cluster5_4)
plt.xticks(fontsize=7)
plt.title('Boxplot for km feature for cluster5_4')

sns.boxplot(x='type',y='age',data=cluster5_4)
plt.xticks(fontsize=7)
plt.title('Boxplot for age feature for cluster5_4')

sns.boxplot(x='type',y='damagessummary',data=cluster5_4)
plt.xticks(fontsize=7)
plt.title('Boxplot for damagessummary feature for cluster5_4')

sns.scatterplot(x='km',y='age',hue='label',data=final35)
fig=px.histogram(cluster5_4,x='mx_target_price',marginal='box',nbins=50,title='Distribution of Target Price for cluster 4')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster5_4,x='km',marginal='box',nbins=50,title='Distribution of km reading for cluster 4')
fig.update_layout(bargap=0.1)
plot(fig)

fig=px.histogram(cluster5_4,x='age',marginal='box',nbins=50,title='Distribution of Age for cluster 4')
fig.update_layout(bargap=0.1)
plot(fig)

#plotting 3d plots
#cmap=ListedColormap(sns.color_palette('husl',256).as_hex())
ax = plt.axes(projection='3d')
scat_plot=ax.scatter3D(final35['km'], final35['age'], final35['mx_target_price'], c=final35['label']);
ax.set_title('Cluster Visualisation')
ax.set_xlabel('km',fontsize=9)
ax.set_ylabel('age',fontsize=9)
ax.set_zlabel('mx_target_price',fontsize=9,labelpad=7)
ax.view_init(30,30,30)
plt.xticks(fontsize=7)
plt.yticks(fontsize=7)
plt.zticks(fontsize=7)
plt.legend(*scat_plot.legend_elements,loc='lower center',borderaxespad=-10)
