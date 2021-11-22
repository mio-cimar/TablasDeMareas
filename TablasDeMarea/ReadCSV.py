#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 10:35:41 2021

@author: miocimar
"""
 
import pandas as pd

df = pd.read_csv('mareas_csv/Uvita.csv')

data = []
datoInicial = 0
datoFinal = 0


for i in range(len(df)):
    # print(df.iloc[i,0])
    
    if ("2022" in str(df.iloc[i,0])):
        data.append(i)
        # print(df.iloc[i,0])
        
# print(data)
print(min(data))
print(max(data))


# dlist = [[] for i in range(365)]
# print(dlist)