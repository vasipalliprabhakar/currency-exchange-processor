import polars as pl
from datetime import datetime
from pathlib import Path


def save_exchange_rates(transformed_records: pl.DataFrame, store_path: Path):
    '''
     save transformed JSON as delta table in DB STORE as delta tables in parquet format
    :param transformed_records: transformed records from API response
    :param store_path: storage location of DELTA tables
    :return: None
    '''
    try:
        transformed_records.write_delta(store_path, mode="overwrite", overwrite_schema=True)
    except Exception as ex:
        print(f"Error saving exchange rates to store, {ex}")
        False
    return True


def get_exchange_aggregates(store_path: Path, previous_date: datetime, current_date: datetime):
    try:
        df = pl.read_delta(store_path)
        new_df = df.unique()
        filter_df = new_df.filter(pl.col('exchange_time').cast(pl.Date).is_between(previous_date, current_date))
        print(f"filtered records by dates, {filter_df}")
        rank_df = filter_df.group_by("from_currency", "to_currency") \
            .agg(pl.max("conversion_rate").alias("best_rate"),
                 pl.min("conversion_rate").alias("lowest_rate"),
                 pl.mean("conversion_rate").alias("average_rate"))
        print(rank_df)
        return [rank_df.item(0, 2), rank_df.item(0, 3), rank_df.item(0, 4)]
    except Exception as ex:
        print(f"Error saving exchange rates to DB, {ex}")
