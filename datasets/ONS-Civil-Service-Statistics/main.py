# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from gssutils import *
from gssutils.metadata import THEME
import pandas as pd

next_table = pd.DataFrame()

# +
# %%capture

#†odo, split table 1-5 up 

# %run "table6.py"
next_table = pd.concat([next_table, new_table])
# %run "table8.py"
next_table = pd.concat([next_table, new_table])
# %run "table9.py"
# -

next_table


