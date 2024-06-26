import pytest
from polars.testing import assert_frame_equal
import tempfile
import os
import polars as pl
from src.etl_scripts.repository import save_exchange_rates, get_exchange_aggregates
from datetime import datetime

lake_path = os.path.join(tempfile.TemporaryDirectory().name, "exchange.delta")


@pytest.fixture
def setup_dataframe():
    data = [{"from_currency": "AUS", "to_currency": "NZD", "exchange_time": "2024-06-10", "conversion_rate": 1.080},
            {"from_currency": "AUS", "to_currency": "NZD", "exchange_time": "2024-05-18", "conversion_rate": 1.078},
            {"from_currency": "AUS", "to_currency": "NZD", "exchange_time": "2024-05-12", "conversion_rate": 1.082},
            {"from_currency": "AUS", "to_currency": "NZD", "exchange_time": "2024-03-02", "conversion_rate": 1.079},
            {"from_currency": "AUS", "to_currency": "NZD", "exchange_time": "2024-02-08", "conversion_rate": 1.071},
            {"from_currency": "AUS", "to_currency": "NZD", "exchange_time": "2024-02-23", "conversion_rate": 1.089}]
    df = pl.DataFrame(data)
    return df


def test_save_exchange_rates(setup_dataframe):
    saved_status = save_exchange_rates(setup_dataframe, lake_path)
    actual_df = pl.read_delta(lake_path)
    assert saved_status == True
    assert_frame_equal(setup_dataframe, actual_df)


def test_get_exchange_aggregates(setup_dataframe):
    current_date = datetime.strptime("2024-06-21", "%Y-%m-%d")
    previous_date = datetime.strptime("2024-03-02", "%Y-%m-%d")
    actual_ranks=get_exchange_aggregates(lake_path, previous_date, current_date)
    assert actual_ranks is not None
    assert actual_ranks[0] == 1.082
    assert actual_ranks[1] == 1.078

