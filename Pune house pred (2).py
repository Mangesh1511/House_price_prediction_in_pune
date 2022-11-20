#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


data = pd.read_csv('Pune_house_data.csv')


# In[3]:


data.shape


# In[4]:


data.info


# In[5]:


for column in data.columns:
    print(data[column].value_counts())
    print("*"*20)


# In[6]:


data.isna().sum()


# In[7]:


data.drop(columns=['area_type','availability','society','balcony'],inplace=True)


# In[8]:


data.describe()


# In[9]:


data['site_location'].value_counts()


# In[10]:


data['size'].value_counts()


# In[11]:


data['size'] = data['size'].fillna('2 BHK')


# In[12]:


data['bath'] = data['bath'].fillna(data['bath'].median())


# In[13]:


data.info()


# In[14]:


data['bhk']= data['size'].str.split().str.get(0).astype(int)   #extract element from each component at specified position
    # to cast a pandas object to a specified dtype


# In[15]:


data[data.bhk>20]


# In[16]:


data['total_sqft'].unique()


# In[17]:


def convertRange(x):
    
    temp =x.split('-')
    if len(temp) == 2: #if we get two values then
        return (float(temp[0]) + float(temp[1]))/2 # conveting into float and finding mean
    try:
        return float(x) #if we get only one value (not range ) then will return that value
    except:
        return None
    
    #it will convert data range in single value by taking its mean 


# In[18]:


data['total_sqft'] =data['total_sqft'].apply(convertRange)


# In[19]:


data.head()


# In[20]:


data['price_per_sqft'] = data['price']*100000 / data['total_sqft'] #in lakhs


# In[21]:


data['price_per_sqft']


# In[22]:


data.describe()


# In[23]:


(data['total_sqft']/data['bhk']).describe()


# In[24]:


data = data[((data['total_sqft'])>=300)]


# In[25]:


data.describe()


# In[26]:


data.shape


# In[27]:


data.price_per_sqft.describe()


# In[28]:


def remove_outliers_sqft(df):
    df_output = pd.DataFrame()
    for key,subdf in df.groupby('site_location'):
        m= np.mean(subdf.price_per_sqft)
        
        st = np.std(subdf.price_per_sqft)
        
        gen_df = subdf[(subdf.price_per_sqft > (m-st)) & (subdf.price_per_sqft <= (m+st))]
        df_output = pd.concat([df_output,gen_df] , ignore_index = True)
    return df_output
data = remove_outliers_sqft(data)
data.describe()


# In[29]:


def bhk_outlier_remover(df):
    exclude_indices = np.array([])
    for site_location,site_location_df in df.groupby('site_location'):
        bhk_stats = {}
        for bhk,bhk_df in site_location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk,bhk_df in site_location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
        return df.drop(exclude_indices,axis='index')


# In[30]:


data =bhk_outlier_remover(data)


# In[31]:


data.shape


# In[32]:


data.drop(columns = ['size','price_per_sqft'],inplace=True)


# In[33]:


data.to_csv("Cleaned_data.csv")


# In[34]:


X=data.drop(columns=['price'])
y=data['price']


# In[35]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score


# In[36]:


X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 0.2,random_state = 0)


# In[37]:


print(X_train.shape)
print(X_test.shape)


# In[38]:


column_trans = make_column_transformer((OneHotEncoder(sparse=False),['site_location']),remainder='passthrough')


# In[39]:


scaler = StandardScaler()


# In[40]:


lr = LinearRegression(normalize = True)


# In[41]:


pipe = make_pipeline(column_trans,scaler,lr)


# In[42]:


pipe.fit(X_train,y_train)


# In[45]:


y_pred_lr = pipe.predict(X_test)


# In[46]:


r2_score(y_test,y_pred_lr)


# In[47]:


lasso = Lasso()


# In[48]:


pipe = make_pipeline(column_trans,scaler,lasso)


# In[49]:


pipe.fit(X_train,y_train)


# In[50]:


y_pred_lasso = pipe.predict(X_test)


# In[51]:


r2_score(y_test,y_pred_lasso)


# In[52]:


ridge = Ridge()


# In[55]:


pipe = make_pipeline(column_trans,scaler,ridge)


# In[56]:


pipe.fit(X_train,y_train)


# In[57]:


import pickle


# In[58]:


pickle.dump(pipe,open('RidgeModel.pkl','wb'))

print(ypre)


# In[ ]:




