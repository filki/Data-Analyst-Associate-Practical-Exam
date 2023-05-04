#!/usr/bin/env python
# coding: utf-8

# # Data Analyst Associate Practical Exam Submission
# 
# **You can use any tool that you want to do your analysis and create visualizations. Use this template to write up your summary for submission.**
# 
# You can use any markdown formatting you wish. If you are not familiar with Markdown, read the [Markdown Guide](https://s3.amazonaws.com/talent-assets.datacamp.com/Markdown+Guide.pdf) before you start.
# 
# 

# ## Task 1
# 
# 

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kurtosis
from scipy.stats import skew


# Loading file

# In[2]:


df = pd.read_csv('food_claims_2212.csv')


# First rows

# In[4]:


df.head()


# Everything looks fine

# Shape of file

# In[5]:


df.shape


# We can see that file contains 2000 rows and 8 columns

# Information about data frame

# In[6]:


df.info()


# We can see that there are some missing values in Data Frame(36 for amount_paid and 26 for linked_cases)

# Some aggregated stastistics

# In[7]:


df.describe()


# We can use unique() function to determine unique values for each column to investigate further into data frame.

# In[8]:


col_names = df.columns
for i in col_names:
    print(df[i].unique())


# Besied missing values, there are some non-standarized values in the last column. Everything else looks fine

# We will replace missing values in amount_paid with overall median amount paid.

# In[9]:


overall_median = df['amount_paid'].median(skipna = True)
#overall median calculation


# In[10]:


df['amount_paid'] = df['amount_paid'].fillna(overall_median)
#filling missing values


# In[11]:


df['amount_paid'].isna().sum()
#final check


# There are no more missing values in column amount_paid.

# Let's get into linked_cases. We will replace missing values fith False

# In[12]:


df['linked_cases'] = df['linked_cases'].fillna(False)
#filling Na values with False boolean


# In[13]:


df['linked_cases'].isna().sum()
#final check


# There are no more missing values in linked_cases

# We can see that column cause have some non-standarized values and some that require trimming. We should take care of it.

# In[14]:


df['cause'] = df['cause'].str.lower()
#standarizing according to requirements


# In[15]:


df['cause'] = df['cause'].str.strip()
#deleting unnecessary spaces


# In[16]:


df['cause'] = df['cause'].replace(['vegetables'],'vegetable')
#replacing vegetables with vegetable


# In[17]:


df['cause'].unique()
#final check


# We can see that everything is fine now.

# The original data is 2000 rows and 8 columns. After validation, there were 2000 rows remaining. The following describes what has been done to each column:
# 
# - **claim_id**: There were 2000 unique values,as expected
# - **time_to_close**: Discrete. The number of days to close the claim. Any positive value,as expected.
# - **claim_amount**:Continuous. The initial claim requested in the currency of Brazil,rounded to 2 decimal places, as expected
# - **amount_paid**: Continuous. Final amount paid. In the currency of Brazil. Rounded to 2 decimal places. Missing values have been replaced with overall median, besides that everything as expected.
# - **location**: Nominal. Location of the claim, one of “RECIFE”, “SAO LUIS”,
# “FORTALEZA”, or “NATAL”. As expected.
# - **individuals_on_claim**: Discrete. Number of individuals on this claim. Minimum 1 person. As expected
# - **linked_cases**: Nominal. Whether this claim is linked to other cases. Either TRUE or FALSE. Missing values have been replaced with FALSE, everything else as expected.
# - **cause** :Nominal. Cause of the food poisoning. One of “vegetable”, “meat”
# or “unknown”. There were some unstandarized values which have been taken care of, everything else as expected.

# ## Task 2

# In[40]:


plt.subplots(figsize=(20,15))
count = df["location"].value_counts(ascending = False)
df_plat = df.filter(["location"], axis = 1)
df_plat['count'] = 1
df_plat
grouped_plat_genre = df_plat.groupby("location", as_index = False,sort= False).sum()
grouped_plat_genre.sort_index(ascending = False)
grouped_plat_genre= grouped_plat_genre.sort_values('count', ascending = False)
sns.barplot(data = grouped_plat_genre, x = "count", y = "location")
plt.title("Claim per location", fontsize = 17)


# a) _Recife_ is **locatio**n with biggest number of observations
# b) The observations are not balanced across categories, _Recife_ stands out very much, _Sao Luis_ also, only _Natal_ and _Fortaleza_ are fairly balanced

# ## Task 3

# In[20]:


sns.histplot(data = df, x = "time_to_close").set(title = 'Distribution of time_to_close')
#creating histogram to inspect distribution


# In[21]:


print(kurtosis(df['time_to_close'], fisher=False)), print(skew(df['time_to_close']))
#calculating kurtosis and skewness


# We can see that the distribution of the **time_to_close** kinda reminds the normal distribution with some of the outliers. Positive kurtosis indicate that we have many outliers. The skewness is positive, which means the distribution is right-skewed, which means the most extreme values of **time_to_close** are on the right side.

# ## Task 4

# We have to convert **location** datatype to categorical in order to inspect correlation

# In[22]:


df_with_category =df.copy()
#copying data frame so it won't mess our previous work


# In[23]:


df_with_category['location']=df_with_category['location'].astype('category').cat.codes


# In[24]:


plt.subplots(figsize=(20,15))
sns.heatmap(df_with_category.corr(),annot=True,robust = True).set(title = 'Correlation Heatmap')


# Correlation is very small so there is no relationships between **time_to_close** and **location**
