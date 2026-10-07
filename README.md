# AI/NLP Risk Engine - S&P Global & Crisil Campus Hackathon

**Candidate Name:** Souhardya Dandapat
**College Email ID:** [sdandapat@kgpian.iitkgp.ac.in]
**College / Campus:** IIT Kharagpur
**Demo Video Link:** [YouTube / Unlisted - ADD LINK HERE]
**Slide Deck Link (if hosted externally):** [ADD LINK HERE]

## 1. Project Overview / Problem Statement & Approach

Financial institutions increasingly rely on unstructured data (news, social media) to anticipate market movements and credit risks. The objective of this project was to design and implement a real-time platform capable of ingesting vast amounts of unstructured text to generate actionable financial risk signals.

To solve this, I built an event-driven **AI/NLP Risk Engine** that acts as a central processing unit. It continuously ingests text from multiple sources, processes them through a pre-trained financial language model (FinBERT) and a zero-shot classifier, and extracts three core signals: a Sentiment Score, an Event Classification, and an Impact Score. 

Downstream business applications subscribe to this Risk Engine to react to these signals dynamically. I implemented **Module A (Tactical Index Rebalancing)**, which automatically shifts portfolio weights based on live sentiment, and **Module B (Strategic Portfolio Stress Testing)**, which simulates shocks to a banking portfolio derived from synthetic open banking transactions upon detecting high-impact macroeconomic events.

## 2. Architecture & Tech Stack

This project strictly follows an **Observer/Subscriber Design Pattern**. The NLP Risk Engine (`src/nlp_engine.py`) acts as the Publisher, while downstream modules (`portfolio_rebalancer.py` and `stress_testing.py`) act as independent Subscribers waiting for signal events.

**Data Flow:**
1. **Ingestion**: Live news and social media are fetched from APIs and datasets.
2. **Analysis**: Text is passed through Hugging Face NLP models to extract structured signals.
3. **Publishing**: The Engine broadcasts the signal to all subscribed downstream modules.
4. **Action**: Modules update portfolio weights or trigger stress tests.
5. **Visualization**: A unified Streamlit dashboard displays the real-time pipeline.

**Tech Stack:**
* **Language**: Python 3.x
* **AI/NLP**: Hugging Face `transformers`, `torch` (ProsusAI/finbert, facebook/bart-large-mnli)
* **Data Sources**: NewsAPI (Live News), Alpha Vantage (Live News Sentiment), GDELT Project v2 API (Live Global Events), `yfinance` (Live Market Prices)
* **Frontend**: Streamlit, Plotly (Interactive Data Visualization)
* **Data Processing**: Pandas

## 3. Dataset Used

This project utilizes 5 data sources combining both live APIs and static datasets:
1. **Live News APIs**: NewsAPI & Alpha Vantage (Financial news headlines and summaries).
2. **GDELT Project**: Real-time event extraction via the GDELT v2 JSON API.
3. **Kaggle Financial Tweets Dataset (`data/tweets.csv`)**: Derived from the open-source Hugging Face `zeroshot/twitter-financial-news-sentiment` dataset. This contains 5,000 real financial tweets simulating historical social media feed ingestion.
4. **yfinance API**: Used to fetch real-time closing prices for the 10 target assets in Module A.
5. **Synthetic Banking Transactions (`data/transactions.csv`)**: A generated dataset mimicking open banking records (loans, mortgages, investments) used to dynamically construct the synthetic portfolio for Module B's stress testing.

## 4. Quickstart & Installation

**Runtime:** Python 3.x on Windows / Linux / macOS

**Step 1: Clone the repository**
```bash
git clone https://github.com/souhardya2023/iitkharagpur-SouhardyaDandapat-hackathon.git
cd iitkharagpur-SouhardyaDandapat-hackathon
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```
*(Note: Downloading the Hugging Face NLP models requires approximately 2GB of free space).*

**Step 3: Configure API Keys**
Rename the `.env.example` file to `.env` and insert your free API keys:
```env
NEWSAPI_KEY=your_newsapi_key
ALPHA_VANTAGE_KEY=your_alphavantage_key
HF_TOKEN=your_hugging_face_token
```

**Step 4: Run the Application**
Launch the interactive Streamlit dashboard:
```bash
streamlit run src/app.py
```

## 5. Key Results & Domain Impact

* **Real-time Event-Driven Architecture:** The implementation of the Observer pattern ensures the pipeline is highly scalable; new risk modules can be added easily without altering the core engine.
* **Multi-Source Resilience:** By integrating three separate unstructured text feeds (NewsAPI, Alpha Vantage, GDELT), the engine protects against the failure or rate-limiting of any single data provider.
* **Domain Impact:** The automated ingestion of unstructured data significantly reduces the latency between a global event occurring and a financial institution reacting. Module A demonstrates an automated, algorithmic trading edge, while Module B allows risk managers to instantly visualize the impact of breaking geopolitical or macroeconomic news on their balance sheet.
