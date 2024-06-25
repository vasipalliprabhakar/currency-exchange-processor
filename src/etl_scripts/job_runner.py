from utilities import config_reader
from exchange_api import make_api_calls
from transform import transform_response
from repository import save_exchange_rates, get_all_exchanges_by_dates
from schemas.db import init_db
import asyncio


def main():
    """
    Service orchestration to call extract, transform and load logic
    :return: None
    """
    init_db()

    # Read the API configuration from YAML
    config_params = config_reader.get_api_config_params()

    # Call API asynchronous 30 times for given configuration
    results = asyncio.run(make_api_calls(config_params))
    print(f"Total records from API : {len(results)}")

    # Transform the results
    transformed_results = transform_response(results)
    print(transformed_results)

    # Load exchange rate to DB
    save_exchange_rates(transformed_results)
    print(get_all_exchanges_by_dates('2024-06-12', '2024-06-14'))


if __name__ == "__main__":
    main()
