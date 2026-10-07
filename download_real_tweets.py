import pandas as pd
from datasets import load_dataset
import random

print("Downloading real Twitter Financial News dataset from HuggingFace...")
try:
    # Load the zeroshot financial news sentiment dataset
    dataset = load_dataset("zeroshot/twitter-financial-news-sentiment", split="train")
    df = pd.DataFrame(dataset)
    
    # We rename 'text' to 'tweet' to match our ingestion script
    df = df.rename(columns={"text": "tweet"})
    
    # Since this dataset doesn't have an explicit 'ticker' column, 
    # we'll extract common tickers if they appear in the tweet, or assign a generic one
    tickers = ["AAPL", "MSFT", "TSLA", "JPM", "FINANCE"]
    
    def extract_ticker(text):
        for t in tickers:
            if t in text:
                return t
        return "FINANCE"
        
    df['ticker'] = df['tweet'].apply(extract_ticker)
    
    # Let's save a good chunk of it (e.g., 5000 tweets) to keep it fast
    df = df.head(5000)
    
    # Save to CSV
    csv_path = "data/tweets.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"Successfully downloaded and saved {len(df)} real financial tweets to {csv_path}!")
    
except Exception as e:
    print(f"Failed to download dataset: {e}")
    print("Please make sure you have the 'datasets' library installed: pip install datasets")
