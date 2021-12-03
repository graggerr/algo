import os
import json
# client_id = os.getenv('TDAMERITRADE_CLIENT_ID')
# account_id = os.getenv('TDAMERITRADE_ACCOUNT_ID')
# refresh_token = os.getenv('TDAMERITRADE_REFRESH_TOKEN')
import tdameritrade as td


client_id = 'XFLXH6H6DJ1X93WCMNVSJMNUTFZAWGSW@AMER.OAUTHAP'
account_id = '279681183'
refresh_token='D7M6wZb6A2lrIuaNVIrydWvqAPictB4KQp8CWLHOMwD9+y2diqdeVl3TJNLBjeDFmQR/nfE6tm6G/5jLOLH8O9AAgSHtDkULBd3OHMg4GTb7LX6w+AbjCpHT0qBTfE1QZEBt8fXSR43W2xaR8OwTeyy8IW+oQ47Ib5kIgbTgyKaCRMSDt4nLWixw11QKYKsIj4yFSdGj14hx82Ugy+T9WQsvIVZOycJCjGCsrjcm+h1DNzcxex3fKgOvKTCSAykKtRM5ZsVhWIygKtleonU9tW3AyAx7vn1q44i5BE9gF6zlrOatESAeCguqwhlWSNAIgb4zCSqCDZkGz76iK/Y55aJTPisUKP6vHeNMWutDTyBx0p0v0qb39KgwSZYWZBnRRbZ5unejEkQSOrsLo9ESAR7halDvZt5HmMlkFPnv66zfP4hQA8Jpa28PMe0100MQuG4LYrgoVi/JHHvlSnUYtoAP5UNX96E2JX0TEfzwRLaMMYIf4qlhLnoR7raV3OZSyDZiafyaYKSqIMGptYKZ/2aGvBf6rGD5ACiuf8cDepSk2DMIsrx0Qfn8rZOssb7R3n2ZRnZlEj8wQBjhBp/CpdwAj4oNHJ/afI65ysv5unYVtfuI11RqqJdutzxol9PtOI86xd3MV4gkWCTsdpIngvyksX/L46m2IF49PzfPqmWVvng9J8jst5lH5j0cOwhyRx3OIkOQt18LFr1KpT1tPGzck5gTnZAUVSCfHpszKUMyxgfg/L6+Nkk2evibK7ux1t9FhO9UBcUJqBPQpdOzfVigCWSSt91bWQwCUW5FLUqzw58fSRJiw3Hx2UYotkMSClZZkUO8Z0/l7NEKYKsQ4bQk0XXutyBRi5iKjzt8PMrgVgc9DcGHEV1wFd32ML3L7XnrYZ2ABPI=212FD3x19z9sWBHDJACbC00B75E'

tdclient = td.TDClient(client_id=client_id, refresh_token=refresh_token, account_ids=[account_id])
# print(tdclient.accounts())
tdclient.session.headers = {
    "Content-Type": "application/json"
}

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


#ef=tdclient.optionsDF('SPY')
res = tdclient.placeOrder(int(account_id),payload)
print(res)