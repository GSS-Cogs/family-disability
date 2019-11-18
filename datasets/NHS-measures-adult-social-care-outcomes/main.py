#!/usr/bin/env python
# coding: utf-8

# In[24]:


from gssutils import *
from databaker.framework import *
import pandas as pd
import datetime

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

year = right(str(datetime.datetime.now().year),2)

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-outcomes-framework-ascof')
scraper


# In[25]:


scraper.select_dataset(title=lambda t: year in t)
scraper


# In[28]:


dist = scraper.distribution(mediaType='text/csv')
dist


# In[34]:


file = dist.downloadURL
file = pd.read_csv(file, encoding = "ISO-8859-1", low_memory = False)
file


# In[36]:


file.to_csv('Tidy.csv', index = False)


# In[ ]:




