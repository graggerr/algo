import json
import os

# client_id = os.getenv('TDAMERITRADE_CLIENT_ID')
# account_id = os.getenv('TDAMERITRADE_ACCOUNT_ID')
# refresh_token = os.getenv('TDAMERITRADE_REFRESH_TOKEN')
from configparser import ConfigParser
from td.client import TDClient
import tdameritrade as td
from sqlalchemy import create_engine, desc, MetaData, Table

# class option(base):
# putCall
# symbol
# description
# exchangeName
# bid
# ask
# last
# mark
# bidSize
# askSize
# bidAskSize
# lastSize
# highPrice
# lowPrice
# openPrice
# closePrice
# totalVolume
# tradeDate
# tradeTimeInLong
# quoteTimeInLong
# netChange
# volatility
# delta
# gamma
# theta
# vega
# rho
# openInterest
# timeValue
# theoreticalOptionValue
# theoreticalVolatility
# optionDeliverablesList
# strikePrice
# expirationDate
# daysToExpiration
# expirationType
# lastTradingDay
# multiplier
# settlementType
# deliverableNote
# isIndexOption
# percentChange
# markChange
# markPercentChange
# intrinsicValue
# inTheMoney
# nonStandard
# pennyPilot
# mini
from sqlalchemy.orm import mapper

from config.Util import get_project_root

config = ConfigParser()
CONFIG_PATH = os.path.join(get_project_root(), 'config/config.ini')  # requires `import os`
config.read(CONFIG_PATH)

CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
CREDENTIALS_PATH = os.path.join(get_project_root(), config.get('main', 'JSON_PATH'))
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

with open(file=CREDENTIALS_PATH, mode='r') as json_file:
    tockens_file=json.load(json_file)

tdclient = td.TDClient(client_id=CLIENT_ID, refresh_token=tockens_file['refresh_token'], account_ids=[CLIENT_ID])
# print(tdclient.movers("$SPX.X"))
# print(tdclient.watchlists())

engine = create_engine("sqlite:///:memory:")
df=tdclient.optionsDF('AKBA',strategy='ANALYTICAL')
# print(df.iloc[132])
print(df)
df.to_excel("output.xlsx")

df.to_sql('AKBA', engine,  if_exists="replace", index=False)
# print(df.describe())
metadata = MetaData()
metadata.reflect(engine)
for table in metadata.tables.values():
    print(table.name)
    for column in table.c:
        print(column.name)

ask=engine.execute("SELECT * FROM AKBA").fetchall()


print(ask)


# users_table = Table('users', metadata, autoload=True)
# class Option(object): pass
# mapper(Option, users_table)

# print(ef.iloc[132])
# print(ef)