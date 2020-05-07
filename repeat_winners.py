import pandas as pd 
import numpy as np
import os
from datetime import datetime


path = "C:\\Users\\lm44\\Documents\\Data\\Repeat Winners Research"

list = os.listdir(path)

def probability_predictions(future_pct, pct_change, weight):
    incorrect_dont_buy = []
    incorrect_buy = []
    correct_dont_buy = []
    correct_buy = []
    total_return = []
    market_return = []
    missed_returns = []

    for i in list: 
        df = pd.read_csv(f'{path}\\{i}')
        df['%change'] = (df['Close'] - df['Open']) / df['Open'] * 100
        future_length = int(len(df) / 100 * future_pct)
        df.dropna(inplace=True)
        
        if len(df) < 100:
            pass
        else:
            future_df = df[-future_length:]
            days = len(future_df)
            df = df[:-future_length]
            df['w%change'] = df['%change'] / (weight/df.index)
            df_buy = df.loc[df['%change'] >= pct_change]
            df_not_buy = df.loc[df['%change'] < pct_change]
            df.dropna(inplace=True)
            future_df.dropna(inplace=True)
            mean_change = np.mean(df['w%change'].values)
            mean_buy = np.mean(df_buy['w%change'].values)
            mean_sell = np.mean(df_not_buy['w%change'].values)
            probability_buy = len(df_buy) / len(df)
            probability_sell = len(df_not_buy) / len(df)
            future_return = (np.cumsum(future_df['%change'].values))
            future_mean = future_return[-1]
            market_return.append(future_mean)
            last_price = df['Close'].iloc[-1]
            last_3_prices = df['w%change'].iloc[-3:]
            
            if ((probability_buy*mean_buy) > abs(probability_sell*mean_sell)) and not all(n < 0 for n in last_3_prices):
                df['buy or sell'] = 1
            else:
                df['buy or sell'] = 0

            if (df['buy or sell'].values[1] == 1) and (future_mean >= pct_change):
                print(f'correct buy: {future_mean}')
                correct_buy.append(future_mean)
                total_return.append(future_mean)
#                 print(df)
            
            elif (df['buy or sell'].values[1] == 0) and (future_mean < pct_change):
#                 print(f'correct dont buy: {future_mean}')
                correct_dont_buy.append(future_mean)
            
            elif (df['buy or sell'].values[1] == 0) and (future_mean >= pct_change):
#                 print(f'incorrect dont buy: {future_mean}')
                incorrect_dont_buy.append(future_mean)
                missed_returns.append(future_mean)
            
            elif (df['buy or sell'].values[1] == 1) and (future_mean < pct_change):
                print(f'incorrect buy: {future_mean} ')
                incorrect_buy.append(future_mean)
                total_return.append(future_mean)
#                 print(df)

    print(f'\nincorrect dont buys: {len(incorrect_dont_buy)}', 
          f'incorrect buys: {len(incorrect_buy)}', 
          f'correct buys: {len(correct_buy)}',
          f'correct dont buys: {len(correct_dont_buy)}',
          f'\n\nSTRATEGY RETURN :({np.mean(total_return)})%.',
          f'\nMARKET PORTFOLIO RETURN :({np.mean(market_return)})%',
          f'\nMISSED RETURN :({np.mean(missed_returns)})%.'
         )

probability_predictions(20, 5, 1)
