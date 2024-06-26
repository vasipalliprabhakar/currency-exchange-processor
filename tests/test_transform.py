import json
import pytest
from pathlib import Path
from src.etl_scripts.transform import transform_api_msg


@pytest.fixture
def setup_source():
    with open(Path(__file__).parent.joinpath("api.json"), "r") as f:
        data = json.load(f)
    return data


def test_transform_api_msg_size(setup_source):
    result_df = transform_api_msg(setup_source)
    assert len(result_df) == 24


def test_transform_api_msg_check_new_fields(setup_source):
    result_df = transform_api_msg(setup_source)
    expected_cols = ['from_currency', 'to_currency', 'exchange_time', 'conversion_rate']
    actual_cols = result_df.columns
    assert all(actual_col in expected_cols for actual_col in actual_cols)



