# etl/transform.py

import pandas as pd
from datetime import datetime, timedelta

def analyze_trends(data):
    """
    this function analyzis the trends over several days

    Args: data - collected data from RESTful API 
    """

    if not data:
        print('no data for trend analysis')
        raise
    
    try:
        df = pd.DataFrame(data)
        
        # check whether neccessary columns exist
        required_columns = ['ticker', 'sentiment', 'date']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError('there are missing columns in data')
        
        df["date"] = pd.to_datetime(df["date"])
        trends = []
        analyzes_days = [7, 14, 21]

        for days in analyzes_days:
            cutoff = datetime.utcnow() - timedelta(days=days)
            filtered = df[df["date"] >= cutoff]
            summary = (
                filtered.groupby("ticker")["sentiment"]
                .value_counts()
                .unstack()
                .fillna(0)
            )

            # calculate bullish_ratio
            summary["bullish_ratio"] = summary.get("bullish", 0) / (summary.sum(axis=1) + 1e-9)
            summary["days"] = days
            trends.append(summary.reset_index()[["ticker", "bullish_ratio", "days"]])
        
        return pd.concat(trends)
    except Exception as e:
        print('error while analyzing trends: ' + e)
        raise

