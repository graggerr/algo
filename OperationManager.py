#TBD

import requests
from config import td_consumer_key
from config import account_id

class OperationManager():

    def __init__(self):
       print('init')

    def placeOrder(self,payload):
        header = {'Authorization':"Bearer {}".format(td_consumer_key),
          "Content-Type":"application/json"}

        # define the endpoint for Saved orders, including your account ID
        endpoint = r"https://api.tdameritrade.com/v1/accounts/{}/savedorders".format(account_id)

        # make a post 
        content = requests.post(url = endpoint, json = payload, headers = header)

        # show the status code, we want 200
        print(content.status_code)
        print(endpoint)

if __name__ == '__main__':
   manager =  OperationManager()
   payload  = {
            "orderStrategyType":
            "SINGLE",
            "orderType":
            "MARKET",
            "orderLegCollection": [{
                "instrument": {
                    "assetType": "OPTION",
                    "symbol": "XYZ_011819P45"
                },
                "instruction": "SELL_TO_OPEN",
                "quantity": 1
            }, {
                "instrument": {
                    "assetType": "OPTION",
                    "symbol": "XYZ_011720P43"
                },
                "instruction": "BUY_TO_OPEN",
                "quantity": 2
            }],
            "complexOrderStrategyType":
            "CUSTOM",
            "duration":
            "DAY",
            "session":
            "NORMAL"
        }
   manager.placeOrder(payload)