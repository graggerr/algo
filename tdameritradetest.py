import os

# client_id = os.getenv('TDAMERITRADE_CLIENT_ID')
# account_id = os.getenv('TDAMERITRADE_ACCOUNT_ID')
# refresh_token = os.getenv('TDAMERITRADE_REFRESH_TOKEN')
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

from config import client_id, refresh_token, account_id

tdclient = td.TDClient(client_id=client_id, refresh_token=refresh_token, account_ids=[account_id])
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