import sqlite3
from pathlib import Path

TABLE_NAME = 'exchange_rates'
CREATE_TABLE_QRY = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} ( 
                      from_currency TEXT, 
                      to_currency TEXT,
                      exchange_time TEXT,
                      conversion_rate REAL NOT NULL,
                      PRIMARY_KEY(from_currency, to_currency, exchange_time) 
                    )
                    '''
ALL_RATE_QRY = f'''SELECT from_currency, to_currency, exchange_time, conversion_rate
                        FROM {TABLE_NAME};
                     '''
RATES_BETWEEN_DATES_QRY = f'''SELECT from_currency, to_currency, exchange_time, conversion_rate
                        FROM {TABLE_NAME} between exchange_time between %(start_date) and %(end_date)
                     '''
RATE_RANKING_BETWEEN_DATES_QRY = f'''SELECT conversion_rate, 
                               MAX(conversion_rate) as best_rate,
                               MIN(conversion_rate) as lowest_rate
                              AVG(conversion_rate) as average-rate
                        FROM {TABLE_NAME} between exchange_time  %(start_date) and %(end_date);
                     '''

DB_PATH = Path(__file__).parent.parent.parent.joinpath("resources/mydatabase.db")

db_connection = sqlite3.connect(DB_PATH)


def init_db():
    cursor = db_connection.cursor()
    cursor.execute(CREATE_TABLE_QRY)
    db_connection.commit()


init_db()
