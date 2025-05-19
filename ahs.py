import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_url_end(idx):
    if idx:
        return "&r=" + str((idx-1)*20 + 21)
    return ""

def get_healthcare_tickers():
    """
    Fetch tickers of healthcare sector stocks from Finviz screener.
    Returns:
        List of tickers in the healthcare sector.
    """
    tickers = []
    for i in range(59):
        url = "https://finviz.com/screener.ashx?v=111&f=sec_healthcare&o=-marketcap" + get_url_end(i)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for row in soup.find_all('a', class_='tab-link'): #fixed this class type based on html
            if(row.text.upper() == row.text): #isolates tickers from junk
                tickers.append(row.text)

    return tickers

def find_large_jumps_in_sector(start_date="2018-01-01", end_date="2023-12-31", threshold=70):
    """
    Identify stocks in the healthcare sector that jumped more than a threshold percentage in a single day.
    """
    tickers = get_healthcare_tickers()
    results = []

    for ticker in tickers:
        try:
            print(f"Fetching data for {ticker}...")
            # Fetch historical data
            data = yf.download(ticker, start=start_date, end=end_date)

            # Calculate daily percentage change
            data['Daily Change (%)'] = (data['Close'] - data['Open']) / data['Open'] * 100

            # Filter rows where the daily change exceeds the threshold
            significant_jumps = data[data['Daily Change (%)'] > threshold]

            if not significant_jumps.empty:
                for date, row in significant_jumps.iterrows():
                    results.append({
                        'Ticker': ticker,
                        'Date': date,
                        'Open': row['Open'],
                        'Close': row['Close'],
                        'Daily Change (%)': row['Daily Change (%)']
                    })

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    # Convert results to a DataFrame and save to CSV
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        results_df.to_csv(f"significant_jumps_healthcare_threshold{str(threshold)}.csv", index=False)
        print("Results saved to significant_jumps_healthcare.csv")
    else:
        print("No significant jumps found.")
    
    return results_df

# Run the function

find_large_jumps_in_sector(threshold=70)

