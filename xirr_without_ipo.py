# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 11:36:58 2022

@author: Vineeth
"""

import pandas as pd
from datetime import datetime
filelist = ['trades2.csv','trades1.csv']
current_val = 351173
iponames=['SGB','GLS','NAZARA','HOMEFIRST','TATVA']
#%%
df=pd.DataFrame()
for i in range(len(filelist)):
    df=pd.concat([df,pd.read_csv(filelist[i])])
#%%
for i in range(len(iponames)):
    df=df[df.symbol.str.contains(iponames[i])==False]

#%%
values=df.price*df.quantity
df['amount'] = values.where(df.trade_type == 'sell', other=-values)

#%%
data = pd.DataFrame()
data['dates'] = df.trade_date
data['amount'] = df.amount

#%%
lastrow = pd.DataFrame({'amount':[current_val],'dates':[datetime.now().strftime("%Y-%m-%d")]})
data=pd.concat([data,lastrow])
#%%
from pyxirr import xirr
xirrpercentage = xirr(pd.DataFrame(data))*100
print("XIRR = ",f'{xirrpercentage:.2f}',"%",end='\n')

abs_profit = df.amount.sum()+current_val
print("Absolute profit = ",u"\u20B9",f'{abs_profit:.2f}')
