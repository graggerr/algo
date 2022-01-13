import os
from configparser import ConfigParser

import pandas as pd

# from splinter import Browser
from td.client import TDClient
from tda.orders.common import Duration, OrderType, Destination, Session, OptionInstruction, ComplexOrderStrategyType,OrderStrategyType

# from config import td_consumer_key
import requests

from config.Util import get_project_root
from tdatrade.exeptions import TDAAPIError, GeneralError, ServerError, ExdLmtError, NotFndError, ForbidError, \
    TknExpError, NotNulError
from tdatrade.trade_strategy import TradeStrategy


class tdbase:
    fee=6
    BASE = 'https://api.tdameritrade.com/v1/'
    #
    # _params= {'apikey': td_consumer_key}
    def __init__(self,trading_account,client_id,redirect_uri,credentials_path):
        # if tdconsumer_key is None:
        #     tdconsumer_key = td_consumer_key

        self.trading_account = trading_account
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.credentials_path = credentials_path
        self.session: TDClient = self._create_session()


    def _create_session(self) -> TDClient:
        """Start a new session.

        Creates a new session with the TD Ameritrade API and logs the user into
        the new session.

        Returns:
        ----
        TDClient -- A TDClient object with an authenticated sessions.

        """

        # Create a new instance of the client
        td_client = TDClient(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            credentials_path=self.credentials_path
        )

        # log the client into the new session
        td_client.login()

        return td_client

    def execute_order(self, order_obj) :
        """Executes a Trade Object.

        Overview:
        ----
        The `execute_orders` method will execute trades as they're signaled. When executed,
        the `Trade` object will have the order response saved to it, and the order response will
        be saved to a JSON file for further analysis.

        Arguments:
        ----
        trade_obj {Trade} -- A trade object with the `order` property filled out.

        Returns:
        ----
        {dict} -- An order response dicitonary.
        """

        # Execute the order.
        order_dict = self.session.place_order(
            account=self.trading_account,
            order=order_obj
        )

        # Store the order.
        _order_response = order_dict

        # # Process the order response.
        # trade_obj._process_order_response()

        return _order_response

class tdclientOrderhelper(tdbase):
    # endpoint = tdbase.BASE+"marketdata/chains"

    #################
    # OPTION CHAINS #
    #################
    # https://developer.tdameritrade.com/option-chains/apis



    # make the request
    # ORDER_END_POINT = tdbase.BASE + 'accounts/{}/orders'.format(super.trading_account)

    def createOreder(self,call_buy='SAVA_012822C54',call_buy_ammount=1.0,call_sell='SAVA_012822C55',call_sell_ammount=1.0, \
            put_buy='SAVA_012822P55',put_buy_ammount=1.0,put_sell='SAVA_012822P54',put_sell_ammount=1.0):
        tradeorder = TradeStrategy().set_complex_order_strategy_type(ComplexOrderStrategyType.IRON_CONDOR) \
            .set_duration(Duration.DAY) \
            .set_order_strategy_type(OrderStrategyType.SINGLE) \
            .set_order_type(OrderType.NET_DEBIT) \
            .copy_price(0.05) \
            .set_quantity(1.0) \
            .set_requested_destination(Destination.AUTO) \
            .set_session(Session.NORMAL) \
            .add_option_leg(OptionInstruction.BUY_TO_OPEN, call_buy, call_buy_ammount) \
            .add_option_leg(OptionInstruction.SELL_TO_OPEN, call_sell, call_sell_ammount) \
            .add_option_leg(OptionInstruction.BUY_TO_OPEN, put_buy, put_buy_ammount) \
            .add_option_leg(OptionInstruction.SELL_TO_OPEN, put_sell, put_sell_ammount)
        return tradeorder.build()

        headers = self._headers(mode='json')

        data: dict = None

        # Define a new session.
        request_session = requests.Session()
        request_session.verify = True

        # Define a new request.
        request_request = requests.Request(
            method="POST",
            headers=headers,
            url=self.ORDER_END_POINT,
            params = self._params,
            data=data,
            json=json_order
        ).prepare()

        # Send the request.
        response: requests.Response = request_session.send(request=request_request)

        request_session.close()

        # grab the status code
        status_code = response.status_code

        # grab the response headers.
        response_headers = response.headers

        # Grab the order id, if it exists.
        if 'Location' in response_headers:
            order_id = response_headers['Location'].split('orders/')[1]
        else:
            order_id = ''

        # If it's okay and we need details, then add them.
        if response.ok :

            response_dict = {
                'order_id': order_id,
                'headers': response_headers,
                'content': response.content,
                'status_code': status_code,
                'request_body': response.request.body,
                'request_method': response.request.method
            }

            return response_dict

        # If it's okay and no details.
        elif response.ok:
            return response.json()

        else:

            if response.status_code == 400:
                raise NotNulError(message=response.text)
            elif response.status_code == 401:
                try:
                    self.grab_access_token()
                except:
                    raise TknExpError(message=response.text)
            elif response.status_code == 403:
                raise ForbidError(message=response.text)
            elif response.status_code == 404:
                raise NotFndError(message=response.text)
            elif response.status_code == 429:
                raise ExdLmtError(message=response.text)
            elif response.status_code == 500 or response.status_code == 503:
                raise ServerError(message=response.text)
            elif response.status_code > 400:
                raise GeneralError(message=response.text)



if __name__ == '__main__':
    # Grab configuration values.
    config = ConfigParser()
    CONFIG_PATH = os.path.join(get_project_root(), 'config/config.ini')  # requires `import os`
    config.read(CONFIG_PATH)

    CLIENT_ID = config.get('main', 'CLIENT_ID')
    REDIRECT_URI = config.get('main', 'REDIRECT_URI')
    CREDENTIALS_PATH = os.path.join(get_project_root(), config.get('main', 'JSON_PATH'))
    ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

    helper=tdclientOrderhelper(trading_account=ACCOUNT_NUMBER,client_id=CLIENT_ID,redirect_uri=REDIRECT_URI,credentials_path=CREDENTIALS_PATH)
    # order_reply=helper.sendOreder(ACCOUNT_NUMBER)
    order_reply=helper.execute_order(helper.createOreder())
    print(order_reply)



