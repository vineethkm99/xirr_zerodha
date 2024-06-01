import pandas as pd
from datetime import datetime
from pyxirr import xirr
INCLUDE_IPOS=False
filelist = []
current_val = 0
equity_val = 0
gold_val = 0

#%%
df=pd.DataFrame()
for i in range(len(filelist)):
    df=pd.concat([df,pd.read_csv(filelist[i])])
#%%
condition = df['symbol'].str.contains('SGB|GOLDBEES', regex=True)
gold_df=df[condition]
equity_df=df[~condition]

ipos = equity_df[equity_df['trade_id'] == 'IPO']['symbol'].unique()
no_ipo_df = equity_df[~equity_df['symbol'].isin(ipos)]
ipo_df = equity_df[equity_df['symbol'].isin(ipos)]

#%%
def process_df(trade_df, trade_val):
    # Calculate amount
    # trade_values = trade_df.price * trade_df.quantity
    # trade_df['amount'] = trade_values.where(trade_df.trade_type == 'sell', other=-trade_values)
    
    trade_df = trade_df.copy()

    trade_df['amount'] = trade_df['price'] * trade_df['quantity']
    trade_df['amount'] = trade_df['amount'].mask(trade_df['trade_type'] != 'sell', -trade_df['amount'])

    data = pd.DataFrame()
    data['dates'] = trade_df.trade_date
    data['amount'] = trade_df.amount

    last_row = pd.DataFrame({'amount': [trade_val], 'dates': [datetime.now().strftime("%d-%m-%Y")]})
    data = pd.concat([data, last_row])
    data['dates'] = pd.to_datetime(data['dates'], dayfirst=True)

    xirr_percentage = xirr(data) * 100
    print("XIRR = ", f'{xirr_percentage:.2f}', "%")

    abs_profit = trade_df.amount.sum() + trade_val
    print("Absolute profit = ", u"\u20B9", f'{abs_profit:.2f}')
    return data

equity_data = process_df(no_ipo_df, equity_val)
gold_data = process_df(gold_df, gold_val)
ipo_data = process_df(ipo_df, 0)