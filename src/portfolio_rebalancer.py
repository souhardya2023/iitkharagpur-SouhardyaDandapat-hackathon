import yfinance as yf
import pandas as pd
import datetime

class TacticalRebalancer:
    def __init__(self, initial_capital=100000):
        # Mock Index (Module A)
        self.tickers = ['AAPL', 'MSFT', 'TSLA', 'JPM', 'JNJ', 'V', 'PG', 'NVDA', 'DIS', 'HD']
        self.initial_capital = initial_capital
        
        # Initial equal weights
        weight = 1.0 / len(self.tickers)
        self.portfolio = {ticker: {'weight': weight, 'sentiment_history': []} for ticker in self.tickers}
        
        self.fetch_latest_prices()

    def fetch_latest_prices(self):
        """Fetches the latest closing prices for the index."""
        try:
            data = yf.download(self.tickers, period="1d", group_by="ticker")
            self.prices = {}
            for ticker in self.tickers:
                # yfinance format can vary if single or multiple tickers, handle robustly
                if len(self.tickers) == 1:
                    self.prices[ticker] = float(data['Close'].iloc[-1])
                else:
                    self.prices[ticker] = float(data[ticker]['Close'].iloc[-1])
        except Exception as e:
            print(f"Error fetching prices: {e}")
            # Fallback mock prices
            self.prices = {ticker: 100.0 for ticker in self.tickers}

    def update(self, signal):
        """Observer update method: Adjusts the portfolio based on a new sentiment signal."""
        ticker = signal.get("target_ticker")
        sentiment_score = signal.get("sentiment_score", 0.0)
        
        if ticker not in self.tickers:
            return

        # Keep a small history of sentiment
        self.portfolio[ticker]['sentiment_history'].append(sentiment_score)
        if len(self.portfolio[ticker]['sentiment_history']) > 5:
            self.portfolio[ticker]['sentiment_history'].pop(0)

        # Rebalancing Logic:
        # Increase weight if sentiment is positive, decrease if negative
        # We'll use a simple adjustment factor
        adjustment = sentiment_score * 0.05  # Max 5% change per signal
        
        new_weight = self.portfolio[ticker]['weight'] + adjustment
        # Ensure weight doesn't go below 1% or above 30%
        new_weight = max(0.01, min(0.30, new_weight))
        
        self.portfolio[ticker]['weight'] = new_weight
        
        self.normalize_weights()

    def normalize_weights(self):
        """Ensures all weights sum to 1.0"""
        total_weight = sum(info['weight'] for info in self.portfolio.values())
        for ticker in self.portfolio:
            self.portfolio[ticker]['weight'] /= total_weight

    def get_portfolio_summary(self):
        """Returns a DataFrame of the current portfolio state."""
        summary = []
        for ticker, info in self.portfolio.items():
            price = self.prices.get(ticker, 0.0)
            shares = (self.initial_capital * info['weight']) / price if price > 0 else 0
            summary.append({
                "Ticker": ticker,
                "Weight (%)": round(info['weight'] * 100, 2),
                "Price ($)": round(price, 2),
                "Value ($)": round(shares * price, 2)
            })
        df = pd.DataFrame(summary)
        return df

if __name__ == "__main__":
    rebalancer = TacticalRebalancer()
    print("Initial Portfolio:")
    print(rebalancer.get_portfolio_summary())
    
    # Simulate a positive signal for AAPL
    rebalancer.process_signal("AAPL", 0.8)
    # Simulate a negative signal for TSLA
    rebalancer.process_signal("TSLA", -0.9)
    
    print("\nAfter Signals:")
    print(rebalancer.get_portfolio_summary())
