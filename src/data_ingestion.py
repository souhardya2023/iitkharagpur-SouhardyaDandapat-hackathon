import os
import pandas as pd
import requests
from newsapi import NewsApiClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_news(query="finance OR stock OR market", limit=10):
    """Fetches top news headlines using NewsAPI."""
    api_key = os.environ.get("NEWSAPI_KEY")
    if not api_key or api_key == "your_newsapi_key_here":
        print("Warning: NEWSAPI_KEY not found or invalid. Returning empty list.")
        return []
    
    try:
        newsapi = NewsApiClient(api_key=api_key)
        q = query.split()[0] if query else "finance"
        all_articles = newsapi.get_everything(q=q, language='en', sort_by='publishedAt', page_size=limit)
        
        articles = []
        if all_articles['status'] == 'ok':
            for article in all_articles['articles']:
                title = article.get('title', '')
                description = article.get('description', '')
                text = f"{title}. {description}" if description else title
                articles.append({
                    "source": article.get("source", {}).get("name", "NewsAPI"),
                    "text": text,
                    "url": article.get("url", "")
                })
        return articles
    except Exception as e:
        print(f"Error fetching from NewsAPI: {e}")
        return []

def fetch_alpha_vantage_news(query="finance", limit=10):
    """Fetches financial news using Alpha Vantage."""
    api_key = os.environ.get("ALPHA_VANTAGE_KEY")
    if not api_key or api_key == "your_alphavantage_key_here":
        print("Warning: ALPHA_VANTAGE_KEY not found or invalid. Returning empty list.")
        return []

    try:
        q = query.split()[0] if query else "finance"
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={q}&limit={limit}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        articles = []
        if "feed" in data:
            for item in data["feed"][:limit]:
                title = item.get("title", "")
                summary = item.get("summary", "")
                text = f"{title}. {summary}" if summary else title
                articles.append({
                    "source": "Alpha Vantage",
                    "text": text,
                    "url": item.get("url", "")
                })
        return articles
    except Exception as e:
        print(f"Error fetching from Alpha Vantage: {e}")
        return []

def fetch_gdelt_news(query="finance", limit=10):
    """Fetches real-time global events using the GDELT Project API (No API Key Required)."""
    try:
        q = query.split()[0] if query else "finance"
        # GDELT v2 DOC API
        url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={q}&mode=ArtList&format=json&maxrecords={limit}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            print("GDELT API Rate Limited (429). Returning empty list.")
            return []
        if response.status_code != 200:
            print(f"GDELT API Error: {response.status_code}. Returning empty list.")
            return []
            
        data = response.json()
        
        articles = []
        if "articles" in data:
            for item in data["articles"]:
                title = item.get("title", "")
                text = title # GDELT gives titles
                articles.append({
                    "source": "GDELT Project",
                    "text": text,
                    "url": item.get("url", "")
                })
        return articles
    except Exception as e:
        print(f"Error fetching from GDELT: {e}")
        return []

def fetch_csv_tweets(query=None):
    """Reads tweets from a local CSV dataset (Kaggle)."""
    try:
        # Assumes this is run from the project root or src/ directory
        csv_path = "data/tweets.csv"
        if not os.path.exists(csv_path):
            csv_path = "../data/tweets.csv" # fallback if run from src/
            
        df = pd.read_csv(csv_path)
        
        # Filter by query if provided (using ticker column or text)
        if query:
            q = query.split()[0].upper()
            filtered_df = df[df['ticker'].str.contains(q, na=False, case=False) | df['tweet'].str.contains(q, case=False)]
            if filtered_df.empty:
                filtered_df = df # Fallback to all if no exact match
        else:
            filtered_df = df

        tweets = []
        for _, row in filtered_df.iterrows():
            tweets.append({
                "source": "Kaggle Dataset (Twitter)",
                "text": row['tweet'],
                "url": ""
            })
        return tweets
    except Exception as e:
        print(f"Error reading CSV tweets: {e}")
        return []

if __name__ == "__main__":
    print("Fetching NewsAPI...")
    print(fetch_news("Apple")[:1])
    print("Fetching Alpha Vantage...")
    print(fetch_alpha_vantage_news("AAPL")[:1])
    print("Fetching CSV Tweets...")
    print(fetch_csv_tweets("AAPL")[:1])
