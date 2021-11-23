# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
from testwithconsumerkey import zerrolossstrategubuilder

if __name__ == '__main__':
    requester = zerrolossstrategubuilder()

    _symbol = 'SAVA'
    filename = "output_zerrowloss_{}.xlsx".format(_symbol)

    # dataDF = requester.getstrategydata(symbol=_symbol.upper())
    dataDF = requester.getstrategypreparedbasedataDF(symbol=_symbol.upper())
    print(dataDF)

    dataDF.to_excel(filename)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
