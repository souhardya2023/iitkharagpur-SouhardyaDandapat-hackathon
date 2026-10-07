import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

class NLPRiskEngine:
    def __init__(self):
        print("Loading NLP Models (this might take a moment)...")
        # For sentiment: FinBERT is specifically trained on financial text
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        
        # For event classification: Zero-shot classification
        self.event_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        
        # Observers/Subscribers list
        self.subscribers = []
        
        # Predefined event types
        self.event_labels = [
            "Geopolitical Event", 
            "Macroeconomic Shift", 
            "Credit Event", 
            "Merger and Acquisition", 
            "Product Launch",
            "Earnings Report",
            "Regulatory Action",
            "Executive Change"
        ]

    def subscribe(self, module):
        """Allows downstream modules to subscribe to the risk engine."""
        if module not in self.subscribers:
            self.subscribers.append(module)

    def notify_subscribers(self, signal):
        """Pushes the structured signal to all subscribed modules."""
        if self.subscribers:
            print(f"📢 Publishing signal to {len(self.subscribers)} subscriber(s)!")
            
        for module in self.subscribers:
            # Each module must implement an `update` method
            module.update(signal)

    def process_text(self, text, metadata=None):
        """Processes a single piece of text and extracts risk signals."""
        
        # 1. Sentiment Score
        # FinBERT returns labels like 'positive', 'negative', 'neutral' with a score
        sentiment_result = self.sentiment_pipeline(text)[0]
        label = sentiment_result['label']
        confidence = sentiment_result['score']
        
        # Map to -1.0 to 1.0 scale
        if label == "positive":
            sentiment_score = confidence
        elif label == "negative":
            sentiment_score = -confidence
        else:
            sentiment_score = 0.0

        # 2. Event Classification
        event_result = self.event_pipeline(text, candidate_labels=self.event_labels)
        event_classification = event_result['labels'][0]
        event_confidence = event_result['scores'][0]

        # 3. Impact Score (Heuristic: 1 to 10)
        # We derive impact based on sentiment magnitude and event confidence
        # A strong sentiment (positive or negative) usually means higher impact.
        base_impact = abs(sentiment_score) * 5  # 0 to 5
        event_impact = event_confidence * 5     # 0 to 5
        impact_score = round(base_impact + event_impact, 1)
        
        # Ensure it's between 1 and 10
        impact_score = max(1.0, min(10.0, impact_score))

        signal = {
            "text": text,
            "sentiment_label": label,
            "sentiment_score": round(sentiment_score, 3),
            "event_classification": event_classification,
            "impact_score": impact_score
        }
        
        if metadata:
            signal.update(metadata)
        
        # Publish to subscribers
        self.notify_subscribers(signal)

        return signal

if __name__ == "__main__":
    engine = NLPRiskEngine()
    sample_text = "The central bank unexpectedly raised interest rates by 50 basis points today, causing a sharp sell-off in equity markets."
    print("Processing:", sample_text)
    result = engine.process_text(sample_text)
    print("Result:", result)
