from td.client import TDClient
from tda.orders.common import ComplexOrderStrategyType, Duration, OrderStrategyType, OrderType, Destination, Session, \
    OptionInstruction
from tda.orders.generic import OrderBuilder
# from tdameritrade.orders.constants import OrderType
from tda.orders import common as order_enums
from tda.orders.generic import OrderBuilder


class TradeStrategy(OrderBuilder):


    # order_field_to_enum_map = dict(
    #
    #     requestedDestination='Destination',
    #     orderType='OrderType',
    #     session='Session',
    #     duration='Duration',
    #     orderStrategyType='OrderStrategyType',
    #     orderLegCollection='OrderLegCollection',
    #     complexOrderStrategyType='ComplexOrderStrategyType',
    #     # childOrderStrategies = 'ChildOrderStrategies',
    #
    # )
    #
    # leg_field_to_enum_map = dict(
    #
    #     OPTION=dict(
    #
    #         instruction='OptionInstruction',
    #         instrument='OptionInstrument',
    #
    #     ),
    #
    #     EQUITY=dict(
    #
    #         instruction='EquityInstruction',
    #         instrument='EquityInstrument'
    #
    #     ),
    #
    # )
    #
    # field_to_order_method_map = dict(
    #
    #     requestedDestination='requested_destination',
    #     orderType='order_type',
    #     session='session',
    #     duration='duration',
    #     orderStrategyType='order_strategy_type',
    #     orderLegCollection=None,
    #     complexOrderStrategyType='complex_order_strategy_type',
    #     price='price',
    #     quantity='quantity',
    #     instruction='instruction',
    #     OPTION='add_option_leg',
    #     EQUITY='add_equity_leg',
    #
    #
    # )
    #
    # def create_instrument(self,instrument_spec):
    #
    #     assetType = instrument_spec['assetType']
    #
    #     symbol = instrument_spec['symbol']
    #
    #     return getattr(order_enums, self.leg_field_to_enum_map[assetType]['instrument'])(symbol)
    #
    # def extract_leg_kwargs(self,leg_spec):
    #
    #     assetType = leg_spec['instrument']['assetType']
    #
    #     instruction_enum = self.leg_field_to_enum_map[assetType]['instruction']
    #
    #     kwargs = dict(
    #
    #         instruction=getattr(
    #             getattr(
    #                 order_enums,
    #                 instruction_enum,
    #             ),
    #             leg_spec['instruction']
    #         ),
    #
    #         symbol=leg_spec['instrument']['symbol'],
    #
    #         quantity=leg_spec['quantity'],
    #
    #     )
    #
    #     return kwargs
    #
    # def get_order_enum(self,field, val):
    #
    #     enum_name = self.order_field_to_enum_map.get(field, None)
    #
    #     if enum_name:
    #
    #         enum = getattr(
    #             getattr(order_enums, enum_name),
    #             val
    #         )
    #
    #     else:
    #
    #         enum = val
    #
    #     return enum
    #
    # def order_from_spec(self,order_spec):
    #
    #     order = OrderBuilder(enforce_enums=True)
    #
    #     for field, val in order_spec.items():
    #
    #         if field == 'orderLegCollection':
    #
    #             for leg_spec in val:
    #                 leg_kwargs = self.extract_leg_kwargs(leg_spec)
    #
    #                 add_leg_method_name = self.field_to_order_method_map[leg_spec['instrument']['assetType']]
    #
    #                 getattr(order, add_leg_method_name)(**leg_kwargs)
    #
    #             continue
    #
    #         method_name_part = self.field_to_order_method_map.get(field, None)
    #
    #         if method_name_part:
    #             set_method_name = f'set_{method_name_part}'
    #
    #             enum = self.get_order_enum(field, val)
    #
    #             getattr(order, set_method_name)(enum)
    #
    #     return order
    #
    # def _process_order_response(self) -> None:
    #     """Processes an order response, after is has been submitted."""
    #
    #     self.order_id = self._order_response["order_id"]
    #     self.order_status = "QUEUED"
    #
    # def _update_order_status(self) -> None:
    #     """Updates the current order status, to reflect what's on TD."""
    #
    #     if self.order_id != "":
    #         order_response = self._td_client.get_orders(
    #             account=self.account,
    #             order_id=self.order_id
    #         )
    #
    #         self.order_response = order_response
    #         self.order_status = self.order_response['status']

    # def check_status(self) -> object:
    #     """Used to easily identify the order status.
    #
    #     Returns
    #     -------
    #     OrderStatus
    #         An order status object that provides simple
    #         properties to grab the order status.
    #     """
    #
    #
    #
    #     return OrderStatus(trade_obj=self)

    # def to_dict(self) -> dict:
    #
    #     # Initialize the Dict.
    #     obj_dict = {
    #         "__class___": self.__class__.__name__,
    #         "__module___": self.__module__
    #     }
    #
    #     # Add the Object.
    #     obj_dict.update(self.__dict__)
    #
    #     return obj_dict

    def getOptionOrder(self,call_buy='SAVA_012822C54',call_buy_ammount=1.0,call_sell='SAVA_012822C55',call_sell_ammount=1.0, \
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



if __name__ == '__main__':
    # call_spread = {
    #     "orderType": "NET_DEBIT",
    #     "session": "NORMAL",
    #     "price": "1.20",
    #     "duration": "DAY",
    #     "orderStrategyType": "SINGLE",
    #     "orderLegCollection": [
    #         {
    #             "instruction": "BUY_TO_OPEN",
    #             "quantity": 10,
    #             "instrument": {
    #                 "symbol": "XYZ_011516C40",
    #                 "assetType": "OPTION"
    #             }
    #         },
    #         {
    #             "instruction": "SELL_TO_OPEN",
    #             "quantity": 10,
    #             "instrument": {
    #                 "symbol": "XYZ_011516C42.5",
    #                 "assetType": "OPTION"
    #             }
    #         }
    #     ]
    # }
    #
    # json_data=Trade_new().order_from_spec(call_spread).build()
    # print(json_data)






    tradeorder=TradeStrategy().set_complex_order_strategy_type(ComplexOrderStrategyType.IRON_CONDOR) \
    .set_duration(Duration.DAY) \
    .set_order_strategy_type(OrderStrategyType.SINGLE) \
    .set_order_type(OrderType.NET_DEBIT) \
    .copy_price(0.05) \
    .set_quantity(1.0) \
    .set_requested_destination(Destination.AUTO) \
    .set_session(Session.NORMAL) \
    .add_option_leg(OptionInstruction.BUY_TO_OPEN, "SAVA_012822C54", 1.0) \
    .add_option_leg(OptionInstruction.SELL_TO_OPEN, "SAVA_012822C55", 1.0) \
    .add_option_leg(OptionInstruction.BUY_TO_OPEN, "SAVA_012822P55", 1.0)\
    .add_option_leg(OptionInstruction.SELL_TO_OPEN, "SAVA_012822P54", 1.0)

    # # Set the Client.
    # tradeorder.account = self.trading_account
    # tradeorder._td_client = self.session


    json_data =tradeorder.build()
    print(json_data)

    print(  TradeStrategy().order_from_spec(json_data).build())

