import polars as pl
from datetime import datetime
from schemas.db import db_connection, TABLE_NAME, RATES_BETWEEN_DATES_QRY


def save_exchange_rates(transformed_records: pl.DataFrame):
    try:
        if not transformed_records.empty:
            pd_df = transformed_records.to_pandas();
            pd_df.to_sql(TABLE_NAME, con=db_connection, if_exists="replace")
    except Exception as ex:
        print(f"Error saving exchange rates to DB, {ex}")
        False
    return True


def get_all_exchanges_by_dates(start_date_str: str, end_date_str: str):
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        RATES_BETWEEN_DATES_QRY.replace("%(start_date)",start_date).replace("%(end_date)",end_date)

        df = pd.read_sql(RATES_BETWEEN_DATES_QRY, db_connection)
        print(df)
    except Exception as ex:
        print(f"Error saving exchange rates to DB, {ex}")
        False


