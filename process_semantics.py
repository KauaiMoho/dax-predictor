from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
analyzer = SentimentIntensityAnalyzer()

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

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

dax_merged['processed_title'] = dax_merged['title'].apply(preprocess_text)

def vader_sentiment(text):
    return analyzer.polarity_scores(text)['compound']

dax_merged['sentiment'] = dax_merged['processed_title'].apply(vader_sentiment)