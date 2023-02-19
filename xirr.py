import pandas as pd
from datetime import datetime
filelist = ['trades2.csv','trades1.csv']
current_val = 351173
ipodates=['2021-02-02','2021-03-26','2021-07-28','2021-08-05']

#%%
df=pd.DataFrame()
for i in range(len(filelist)):
    df=pd.concat([df,pd.read_csv(filelist[i])])
#%%
df=df[df.symbol.str.contains("SGB")==False]

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
ipoamounts = [-15000]*len(ipodates)
ipopd = pd.DataFrame({'dates':ipodates,'amount':ipoamounts})
data=pd.concat([data,ipopd])


#%%
from pyxirr import xirr
xirrpercentage = xirr(pd.DataFrame(data))*100
print("XIRR = ",f'{xirrpercentage:.2f}',"%",end='\n')

abs_profit = df.amount.sum()+current_val+sum(ipoamounts)
print("Absolute profit = ",u"\u20B9",f'{abs_profit:.2f}')

#%%
iponames=['GLS','NAZARA','HOMEFIRST','TATVA']
ipotxns = pd.DataFrame()
for i in range(len(iponames)):
    temp = df[df.symbol.str.contains(iponames[i])]
    ipotxns = pd.concat([ipotxns,temp])

    
