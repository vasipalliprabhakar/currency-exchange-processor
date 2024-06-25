import asyncio
import aiohttp
from pathlib import Path
from utilities import date_util

CONFIG_FILE_PATH = Path(__file__).parent.parent.joinpath("resources/config.ini")


async def fetch_data(url, credentials):
    """
    Call exchange rate API asynchronous and return the response

    :param url: URL of currency exchange API endpoint
    :param credentials: API username and password authentication
    :return: JSON response of exchange rate for specific date in query param
    """
    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(credentials.get('username'),
                                                            credentials.get('password'))) as session:
        async with session.get(url) as response:
            return await response.json()


async def make_api_calls(params):
    # Build past 30 days given the start date to read exchange rates
    req_dates = date_util.DateUtil.generate_past_30_days(params.get('start_date'), params.get('total_days'))

    # Username and password authentication headers
    auth = {"username": params.get('api_id'),
            "password": params.get('api_key')}

    # Api limitation to read specific date exchange rate so build multiple urls for last 30 days
    urls = [f"{params.get('base_url')}&to={params.get('to')}&date={d}" for d in req_dates]
    print(urls)

    tasks = [fetch_data(url, auth) for url in urls]

    # Run all api calls concurrently using asyncio library
    results = await asyncio.gather(*tasks)
    return results
