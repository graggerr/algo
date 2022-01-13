import pandas as pd
from functools import reduce

if __name__ == '__main__':
    # Notice we don't prefix this with "python" because this is a script that was
    # installed by pip when you installed tda-api
    # tda - orders - codegen.py - -token_file < your token file path > --api_key < your  API key >

    tdmarket_data= pd.DataFrame()
    tdmarket_data['symbol'] = ['S', 'S','S', 'S', 'S', 'S']
    tdmarket_data['strikePrice'] = [1, 1, 2, 2,1,1]
    tdmarket_data['mark'] = [2,1,1,2,0.1,0.1]
    tdmarket_data['daysToExpiration'] = [1, 1, 1, 1,2,2]
    tdmarket_data['putCall'] = ['CALL', 'PUT', 'CALL', 'PUT','CALL', 'PUT']

    print(tdmarket_data)

    dfcalls = tdmarket_data.loc[(tdmarket_data.putCall == 'CALL') & (tdmarket_data['mark'] != 0)][
        ['symbol', 'strikePrice', 'mark', 'daysToExpiration', ]]


    dfcalls = dfcalls.rename(
        columns={'symbol': 'callsymbol','mark': 'callmark'})

    dfputts = tdmarket_data.loc[(tdmarket_data.putCall == 'PUT') & (tdmarket_data['mark'] != 0)][
        ['symbol', 'strikePrice', 'mark', 'daysToExpiration', ]]
    dfputts = dfputts.reindex()
    dfputts = dfputts.rename(columns={'symbol': 'putsymbol','mark': 'putmark' })

    dfmerged = pd.merge(dfcalls, dfputts, on=['strikePrice', 'daysToExpiration'])

    print("dfmerged",dfmerged)

    dfshifted = dfmerged.add_suffix('1').assign(**dfmerged.shift(-1).add_suffix('2'))
    print("dfshifted", dfshifted)
    print("cleaned", dfshifted.loc[(dfshifted.daysToExpiration1 == dfshifted.daysToExpiration2)])


    # dfshifted =grouped_t=dfmerged.groupby('daysToExpiration').add_suffix('1').shift(-1).add_suffix('2')
    # dfshifted =grouped_t.add_suffix('1').assign(**grouped_t.shift(-1).add_suffix('2'))

    # tdmarket_data[['diff_put_mark{}'.format(1)]] = tdmarket_data.groupby('daysToExpiration')[['putmark']].diff(periods=(-(1)))

    # dfshifted = dfmerged[['strikePrice', 'mark']].add_suffix('1').assign(**dfmerged.shift(-1).add_suffix('2'))
    # dfmerged[['dif_strike_price1', 'diff_call_mark1']] = \
    #     dfmerged.groupby('daysToExpiration')[['strikePrice', 'callmark']].diff(periods=1)





    # print (dfmerged.groupby('daysToExpiration')[['strikePrice', 'callmark']].assign(**dfmerged.shift(-1).add_suffix('2')))
    # dfshifted = dfmerged.groupby('daysToExpiration')[['strikePrice', 'daysToExpiration']].assign(**dfmerged.shift(-1).add_suffix('2'))

    # print(dfshifted)


