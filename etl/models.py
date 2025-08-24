# etl/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RedditSentiment(Base):
    '''
    this is a class to set the format of the stored data
    '''
    __tablename__ = 'reddit_sentiment_trend'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String)
    bullish_ratio = Column(Float, nullable=False)
    days = Column(Integer, nullable=False)