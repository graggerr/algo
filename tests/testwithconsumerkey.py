
# def testjsonrun():
#
#
#     requester=zerrolossstrategyestimator()
#
#     # recive option DF
#
#     _symbol='MSFT'
#     # _strategy="SINGLE"
#     # _strategy="VERTICAL"
#     _strategy="ANALYTICAL"
#     _contractType='ALL'
#     _includeQuotes=True
#     filename="output_zerrowloss_{}_{}_{}.xlsx".format(_symbol,_strategy,_contractType)
#     # dataDF = requester.optionsDF(symbol=_symbol.upper(), strategy=_strategy.upper(), #'VERTICAL',
#     #                     includeQuotes= True,contractType=_contractType)
#     # print(dataDF)
#     # dataDF.to_excel(filename)
#
#     dataDF = requester.singleOptionsDF(symbol=_symbol.upper(),strategy=_strategy.upper(),
#                         includeQuotes= True,contractType=_contractType)
#     print(dataDF)
#
#     #to excel
#
#     dataDF.to_excel(filename)
#
#     #to DB
#
#     engine = create_engine("sqlite:///:memory:")
#     dataDF.to_sql(_symbol, engine,  if_exists="replace", index=False)
#     # print(df.describe())
#     metadata = MetaData()
#     metadata.reflect(engine)
#     # for table in metadata.tables.values():
#     #     print(table.name)
#     #     for column in table.c:
#     #         print(column.name)
#
#     ask=engine.execute("SELECT * FROM {}".format(_symbol)).fetchone()
#
#
#     # print(ask)
#
#     #  json
#
#     datajson = requester.options(symbol=_symbol.upper(), strategy=_strategy.upper(),
#                         contractType=_contractType)
#
#     # print(json.dumps(datajson, indent=4, sort_keys=True))
#     # print(datajson)
#
from strategies.estimators.zerrolossstrategyestimator import zerroloss_strategy_TD_estimator
from strategies.handlers.zerrolosstrategyhandler import zerroloss_strategy_handler


def teststrategy():
    _symbol = 'SAVA'
    requester = zerroloss_strategy_TD_estimator(_symbol)


    filename = "output_zerrowloss_{}.xlsx".format(_symbol)

    # dataDF = requester.getstrategydata(symbol=_symbol.upper())
    dataDF = requester.getstrategydataDF()
    print(dataDF)

    dataDF.to_excel(filename)

    # return best operations
    print(zerroloss_strategy_handler().handlestrategyDF(requester))

if __name__ == '__main__':
    teststrategy()
