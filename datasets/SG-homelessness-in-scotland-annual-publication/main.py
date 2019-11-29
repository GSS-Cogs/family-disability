#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import glob

py_files = [i for i in glob.glob('*.{}'.format('py'))]

for i in py_files:
    file = "'" + i + "'"
    if file.startswith("'main") == True:
        continue
    get_ipython().run_line_magic('run', '$file')

