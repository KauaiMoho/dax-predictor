
import pandas as pd
from finvader import finvader                         

#VADER Scores
# positive sentiment: compound score >= 0.05
# neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
# negative sentiment: compound score <= -0.05

dax_ft = pd.read_csv('dax_ft.csv')
dax_investing = pd.read_csv('dax_investing.csv', parse_dates=["date"])
dax_tradingview = pd.read_csv('dax_tradingview.csv', parse_dates=["date"])

dax_yahoo = pd.read_csv('dax_yahoo.csv')
dax_yahoo["date"] = dax_yahoo["date"].str.extract(r"([A-Za-z]+ \d{1,2}, \d{4})")
dax_yahoo['date'] = pd.to_datetime(dax_yahoo['date'], format='mixed')

dax_ft['date'].fillna(method='ffill',inplace=True)
dax_ft['date'] = pd.to_datetime(dax_ft['date'], format='mixed')

dax_ft.set_index('date', inplace=True)
dax_investing.set_index('date', inplace=True)
dax_tradingview.set_index('date', inplace=True)
dax_yahoo.set_index('date', inplace=True)

dax_merged = pd.concat([dax_ft, dax_investing, dax_tradingview, dax_yahoo])
dax_merged.sort_index(inplace=True, ascending=False)

dax_merged['sentiment'] = dax_merged['title'].apply(finvader, use_sentibignomics = True, use_henry = True, indicator="compound")   

dax_merged.to_csv('sentiments_merged.csv') 