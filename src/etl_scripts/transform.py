import polars as pl
from flatten_json import flatten_json


def transform_api_msg(json_records):
    schema = {
        'centralBankCode': pl.Utf8,
        'centralBankName': pl.Utf8,
        'terms': pl.Utf8,
        'privacy': pl.Utf8,
        'from': pl.Utf8,
        'amount': pl.Float64,
        'timestamp': pl.Utf8,
        'to_0_quotecurrency': pl.Utf8,
        'to_0_mid': pl.Float64,
    }
    input_df = pl.DataFrame([flatten_json(rec) for rec in json_records], schema=schema)

    filter_df = input_df.select(
        pl.col("from"),
        pl.col("to_0_quotecurrency"),
        pl.col("to_0_mid"),
        pl.col("timestamp"))

    target_df = filter_df.rename({"from": "from_currency",
                                  "timestamp": "exchange_time",
                                  "to_0_quotecurrency": "to_currency",
                                  "to_0_mid": "conversion_rate"});
    return target_df.select(['from_currency', 'exchange_time', 'to_currency', 'conversion_rate'])
