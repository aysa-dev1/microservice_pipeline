# etl/load.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from etl.models import Base, RedditSentiment

# engine and session setup
engine = create_engine("sqlite:///sentiment.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def store_data(data):
    '''
    this function is used to store the data into the database

    Args:
    data - list of Dictionaries with sentiments
    '''

    if not data:
        print('no data to store')
        raise

    session = Session()
    
    try:
        for item in data:
            entry = RedditSentiment(**item)
            session.merge(entry)
        session.commit()
        print('data successfuly stored')
    
    except Exception as e:
        session.rollback()
        print('While storing the data: ' + e)
        raise
    
    finally:
        session.close()
