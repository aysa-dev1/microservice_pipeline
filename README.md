# Reddit Sentiment ETL Microservice

This microservice reads the data of shares from reddit, analyzes trends and store the results in a SQL-Lite Database

## Installation

```bash
python -m venv venv
venv\Scripts\activate  # Linus: source venv/bin/activate 
pip install -r requirements.txt
```

## Starting the pipeline
```bash
dagster dev -f .\pipeline\dagster_pipeline.py
```

---

## Architecture overview

- Source:
  - Reddit API (tradestie.com) or Mock-data (switchable via `use_mock` in `etl/extract.py`).
- Pipeline (Dagster-Job `reddit_etl_job`):
  1. `extract_op` → `get_data()`
     - input: API/Mock
     - output: List of Dicts `[{ticker, sentiment, date}]`
  2. `transform_op` → `analyze_trends()`
     - input: List of Dicts
     - output: DataFrame `[ticker, bullish_ratio, days]` (for 7/14/21 days)
  3. `to_dict_op`
     - input: DataFrame
     - output: List of Dicts `[{ticker, bullish_ratio, days}]`
  4. `load_op` → `store_data()`
     - input: Liste von Dicts
     - target: SQLite (table `reddit_sentiment_trend`)

### diagramm
```
[Reddit API]   [Mock Generator]
      \             /
       \           /
        --> (extract_op/get_data)
               |
               v
  [{ticker, sentiment, date}]  (list of dicts)
               |
               v
     (transform_op/analyze_trends)
               |
               v
   DataFrame [ticker, bullish_ratio, days]
               |
               v
         (to_dict_op)
               |
               v
  [{ticker, bullish_ratio, days}] (list of dicts)
               |
               v
       (load_op/store_data)
               |
               v
  (SQLite) reddit_sentiment_trend
```
