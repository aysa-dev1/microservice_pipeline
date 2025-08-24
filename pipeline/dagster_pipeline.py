# pipeline/dagster_pipeline.py
from dagster import job, op
from etl.extract import get_data
from etl.transform import analyze_trends
from etl.load import store_data
import pandas as pd

@op
def extract_op():
    return get_data()

@op
def transform_op(data):
    return analyze_trends(data)

@op
def to_dict_op(df):
    return df.to_dict(orient='records')

@op
def load_op(data):
    return store_data(data)

@job
def reddit_etl_job():
    raw = extract_op()
    transformed = transform_op(raw)
    data_for_db = to_dict_op(transformed)
    load_op(data_for_db)
