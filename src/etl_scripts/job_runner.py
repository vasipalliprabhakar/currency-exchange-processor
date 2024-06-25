import os.path

from utilities import config_reader
from exchange_api import make_api_calls
from transform import transform_api_msg
from repository import save_exchange_rates, get_exchange_aggregates
import asyncio
from pathlib import Path
import os
from datetime import datetime
import tempfile

CONFIG_FILE_PATH = Path(__file__).parent.parent.joinpath(os.path.join("resources", "config.yaml"))

DATE_FORMAT = '%Y-%m-%d'

db_path = os.path.join(tempfile.TemporaryDirectory().name, "exchange.delta")


def main_job():
    """
    Service orchestration to call extract, transform and load logic
    :return: None
    """

    # Read the API configuration from YAML
    config_params = config_reader.get_api_config(CONFIG_FILE_PATH)

    # Call API asynchronous 30 times for given configuration
    results = asyncio.run(make_api_calls(config_params))
    print(f"Total records received from API : {len(results)}")

    # Transform the results
    transformed_msg = transform_api_msg(results)
    print(f"transformed records from API\n {transformed_msg}")

    # Load exchange rate to DB
    save_exchange_rates(transformed_msg, db_path)
    print("Saved records to Delta storage!!")
    print(get_exchange_aggregates(db_path, datetime.strptime('2024-05-12', DATE_FORMAT),
                                     datetime.strptime('2024-06-25', DATE_FORMAT)))


if __name__ == "__main__":
    main_job()
