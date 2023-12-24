#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 10:24:30 2023

@author: neo
"""

from constants import HEADER_NAME, TARGETED_TYPE1_TRI_LIST
from plot_helper import calc_after_burin_auc_from_list
import numpy as np
import pandas as pd
import os
auc_1000runs = []

fdir_path = "raw"

for i in range(0,1000):
  df = pd.read_csv(
    os.path.join(fdir_path, f'monthly_data_{i}.txt'),
    index_col=False,
    names=HEADER_NAME,
    sep='\t'
  ).fillna(0)
  assert df.shape == (361, 283)
  summed_genofreq = df.filter(items=TARGETED_TYPE1_TRI_LIST).sum(axis=1).values
  auc_1000runs.append(calc_after_burin_auc_from_list(summed_genofreq))

#%%

df = pd.read_csv("task4_params.csv")
df = df.iloc[0:1000, :]
df["auc"] = auc_1000runs

df.to_csv("task4_auc_triple_only.csv", index=False)