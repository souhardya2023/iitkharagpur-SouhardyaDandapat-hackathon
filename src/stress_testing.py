import pandas as pd
import os

class StrategicStressTester:
    def __init__(self):
        """
        Module B: Strategic Portfolio Stress Testing
        Simulates the impact of major real-world events on a synthetic portfolio.
        """
        self.portfolio = self._load_synthetic_portfolio()
        self.total_value = sum(self.portfolio.values())

    def _load_synthetic_portfolio(self):
        """Loads a synthetic portfolio from the financial transactions dataset."""
        try:
            csv_path = "data/transactions.csv"
            if not os.path.exists(csv_path):
                csv_path = "../data/transactions.csv"
            df = pd.read_csv(csv_path)
            
            # Create a mock portfolio derived from transaction volumes
            portfolio = {
                "Retail Loans": df[df['category'] == 'Loan Repayment']['amount'].sum() * 100,
                "Mortgages": df[df['category'] == 'Mortgage']['amount'].sum() * 50,
                "Investments": df[df['category'] == 'Investment']['amount'].sum() * 10,
                "Corporate Bonds": 200000.0 # Synthetic base
            }
            return portfolio
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return {
                "Retail Loans": 500000.0,
                "Mortgages": 300000.0,
                "Investments": 200000.0
            }

    def update(self, signal):
        """
        Observer update method: Checks if the signal is a high-impact event and triggers stress test.
        """
        event_classification = signal.get("event_classification")
        impact_score = signal.get("impact_score", 0.0)

        # Trigger stress test if impact is high
        if impact_score > 7.0:
            print(f"High Impact Event Detected: {event_classification} with Impact: {impact_score}")
            self.apply_stress_event(event_classification, impact_score)

    def apply_stress_event(self, event_classification, impact_score):
        """
        Applies a shock to the portfolio based on the event type and impact score.
        """
        print(f"Applying Stress Test for Event: {event_classification} with Impact: {impact_score}")
        
        shock_factor = impact_score * 0.01 # 1% shock per impact point
        
        if event_classification == "Macroeconomic Shift":
            self.portfolio["Corporate Bonds"] *= (1 - shock_factor * 1.5)
            self.portfolio["Retail Loans"] *= (1 - shock_factor * 0.5)
            self.portfolio["Mortgages"] *= (1 - shock_factor * 0.2)
        elif event_classification == "Credit Event":
            self.portfolio["Retail Loans"] *= (1 - shock_factor * 2.0)
            self.portfolio["Mortgages"] *= (1 - shock_factor * 1.5)
        elif event_classification == "Regulatory Action":
            self.portfolio["Investments"] *= (1 - shock_factor * 2.0)
        else:
            # General shock across all assets
            for asset in self.portfolio:
                self.portfolio[asset] *= (1 - shock_factor)
                
        new_total = sum(self.portfolio.values())
        value_lost = self.total_value - new_total
        
        self.total_value = new_total
        return {
            "new_portfolio": self.portfolio,
            "new_total_value": self.total_value,
            "value_lost": value_lost
        }

if __name__ == "__main__":
    tester = StrategicStressTester()
    result = tester.apply_stress_event("Macroeconomic Shift", 8.5)
    print("Stress Test Result:", result)
