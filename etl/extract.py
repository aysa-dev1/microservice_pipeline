#etl/extrac.py
import requests
from datetime import datetime, timedelta
import random

use_mock = True

# URL for RESTful API
url = "https://tradestie.com/api/v1/apps/reddit"

def get_data():
    """
    this function collects the data from RESTful API of tradestie or return mock data

    Returns:
        data - collected data
    """
    
    if use_mock:
        return get_mock_data()
    else:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print('Error getting data from API: ' + e)
            raise


def get_mock_data():
    ''' 
    this is a help function to mock API data
    '''

    tickers = ['AAPL', 'TSLA', 'GOOGL', 'MSFT']
    data = []

    for _ in range(50):
        days_ago = random.randint(0,25)
        sentiment = random.choice(['bullish', 'bearish'])

        data.append(
            {
                'ticker': random.choice(tickers),
                'sentiment': sentiment,
                'date': (datetime.now() - timedelta(days=days_ago)).date()
            }
        )
    
    return data