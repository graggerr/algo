
class outputUtil:
    def dataToExl(symbol_name,data):
            filename = "output_zerrowloss_{}.xlsx".format(symbol_name)
            data.to_excel(filename)