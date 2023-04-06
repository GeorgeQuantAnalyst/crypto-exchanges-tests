import unittest

import requests
from pybit import usdt_perpetual

from exchanges.bybit_extend import BybitExtend
from utils import load_config


class BybitFuturesTest(unittest.TestCase):

    def setUp(self) -> None:
        print("Start SetUp")

        print("Load config")
        self.config = load_config("../config.yaml")

        print("Init CCXT Bybit client")
        self.exchange = BybitExtend({
            "apiKey": self.config["bybitApi"]["apiKey"],
            "secret": self.config["bybitApi"]["secretKey"]}
        )

        print("Init Pybit official Bybit client")
        self.pybit_client = usdt_perpetual.HTTP(
            endpoint=self.config["bybitApi"]["url"],
            api_key=self.config["bybitApi"]["apiKey"],
            api_secret=self.config["bybitApi"]["secretKey"]
        )
        self.exchange.set_sandbox_mode(True)
        self.set_default_setting()

        print("Finished SetUp")

    def tearDown(self) -> None:
        print("Start Tear down")

        print("Cancel all derivatives orders")
        self.exchange.cancel_all_derivatives_orders()

        print("Cancel all derivatives positions")
        positions = self.exchange.fetch_derivatives_positions()
        for position in positions:
            position_info = position["info"]
            self.exchange.create_order(symbol=position_info["symbol"],
                                       type="market",
                                       side="Sell" if position_info["side"] == "Buy" else "Buy",
                                       amount=position_info["size"],
                                       params={
                                           "positionIdx": position_info["positionIdx"],
                                           "reduceOnly": True})

        self.set_default_setting()

        print("Finished Tear down")

    def test_get_btc_current_price(self):
        print("Start test_get_btc_current_price")
        url = "https://api-testnet.bybit.com/v5/market/orderbook?category={}&symbol={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("linear", "BTCUSDT"), headers=headers, data=payload).json()
        print("Response: {}".format(response))
        result = response["result"]
        bid = float(result["b"][0][0])
        ask = float(result["a"][0][0])
        spread = ask - bid

        print("Bid price is: {}, ask price is: {} and spread is: {}".format(bid, ask, spread))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        self.assertTrue(bid > 0)
        self.assertTrue(ask > 0)
        self.assertTrue(bid < ask)

        print("Finished test_get_btc_current_price")

    def test_get_btc_daily_ohlc(self):
        print("Start test_get_btc_daily_ohlc")
        url = "https://api-testnet.bybit.com/v5/market/kline?category={}&symbol={}&interval={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("linear", "BTCUSDT", "D"), headers=headers, data=payload).json()
        print("Response: {}".format(response))
        result = response["result"]
        ohlc_daily = result["list"]

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        self.assertTrue(len(ohlc_daily) > 1)
        print("Finished test_get_btc_daily_ohlc")

    def test_get_btcusdt_info(self):
        print("Start test_get_btcusdt_info")
        url = "https://api-testnet.bybit.com/v5/market/instruments-info?category={}&symbol={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("linear", "BTCUSDT", headers=headers, payload=payload)).json()
        print("Response: {}".format(response))
        result = response["result"]

        btc_info = result["list"][0]

        print(btc_info)

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")

        # Base info
        self.assertEqual(btc_info["symbol"], "BTCUSDT")
        self.assertEqual(btc_info["contractType"], "LinearPerpetual")
        self.assertEqual(btc_info["launchTime"], "1585526400000")
        self.assertEqual(btc_info["priceScale"], "2")
        self.assertEqual(btc_info["fundingInterval"], 480)
        self.assertEqual(btc_info["settleCoin"], "USDT")

        # Leverage filter
        self.assertEqual(btc_info["leverageFilter"]["minLeverage"], "1")
        self.assertEqual(btc_info["leverageFilter"]["maxLeverage"], "100.00")
        self.assertEqual(btc_info["leverageFilter"]["leverageStep"], "0.01")

        # Lot size filter
        self.assertEqual(btc_info["lotSizeFilter"]["maxOrderQty"], "100.000")
        self.assertEqual(btc_info["lotSizeFilter"]["minOrderQty"], "0.001")
        self.assertEqual(btc_info["lotSizeFilter"]["qtyStep"], "0.001")

        print("Finished test_get_btcusdt_info")

    def test_get_available_usdt_balance_on_account(self):
        print("Start test_get_available_usdt_balance_on_account")
        response = self.exchange.fetch_balance({"coin": "USDT"})
        print("Response: {}".format(response))
        total_balance = float(response["USDT"]["total"])
        free_balance = float(response["USDT"]["free"])

        print("Total balance: {} USDT, Free balance: {} USDT".format(round(total_balance, 2), round(free_balance, 2)))

        self.assertEqual(response["info"]["retCode"], "0")
        self.assertEqual(response["info"]["retMsg"], "OK")
        self.assertTrue(total_balance >= 0)
        self.assertTrue(free_balance >= 0)
        print("Finished test_get_available_usdt_balance_on_account")

    def test_buy_btc_by_market_order(self):
        print("Start test_buy_btc_by_market_order")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="market",
                                              side="buy",
                                              amount=0.001,
                                              params={
                                                  "positionIdx": 0})
        print("Response: {}".format(response))

        self.assertTrue("id" in response)
        print("Finished test_buy_btc_by_market_order")

    def test_sell_btc_by_market_order(self):
        print("Start test_sell_btc_by_market_order")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="market",
                                              side="sell",
                                              amount=0.001,
                                              params={
                                                  "positionIdx": 0})

        print("Response: {}".format(response))

        self.assertTrue("id" in response)
        print("Finished test_sell_btc_by_market_order")

    def test_buy_btc_by_limit_order(self):
        print("Start test_buy_btc_by_limit_order")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="limit",
                                              side="buy",
                                              amount=0.001,
                                              price=20000,
                                              params={
                                                  "positionIdx": 0})
        print("Response: {}".format(response))

        self.assertTrue("id" in response)
        print("Finished test_buy_btc_by_limit_order")

    def test_sell_btc_by_limit_order(self):
        print("Start test_sell_btc_by_limit_order")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="limit",
                                              side="sell",
                                              amount=0.001,
                                              price=30000,
                                              params={
                                                  "positionIdx": 0})
        print("Response: {}".format(response))
        self.assertTrue("id" in response)
        print("Finished test_sell_btc_by_limit_order")

    def test_buy_btc_with_take_profit_and_stop_loss(self):
        print("Start test_buy_btc_with_take_profit_and_stop_loss")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="limit",
                                              side="buy",
                                              amount=0.001,
                                              price=20000,
                                              params={
                                                  "triggerPrice": "20000",
                                                  "takeProfit": "22000",
                                                  "stopLoss": "18000",
                                                  "positionIdx": 0})
        print("Response: {}".format(response))

        self.assertTrue("id" in response)
        print("Finished test_buy_btc_with_take_profit_and_stop_loss")

    def test_place_trailing_stop(self):
        print("Start test_place_trailing_stop")

        print("Open small position on BTC")
        create_order_response = self.create_small_btc_long_position()

        print("Create trailing stop 100 USD")
        trailing_stop_response = self.pybit_client.set_trading_stop(
            symbol="BTCUSDT",
            trailing_stop=100,
            position_idx=0
        )

        print("Create order response: {}".format(create_order_response))
        print("Trailing stop response: {}".format(trailing_stop_response))

        self.assertTrue("id" in create_order_response)
        self.assertEqual(trailing_stop_response["ret_code"], 0)
        self.assertEqual(trailing_stop_response["ret_msg"], "OK")

        print("Finished test_place_trailing_stop")

    def test_get_positions(self):
        print("Start test_get_open_positions")

        print("Create small positions on BTC and ETH")
        self.create_small_btc_long_position()
        self.create_small_eth_long_position()

        print("Get positions")
        positions = self.exchange.fetch_derivatives_positions()
        print(positions)

        self.assertEqual(len(positions), 2)
        self.assertEqual(positions[0]["symbol"], "BTC/USDT:USDT")
        self.assertEqual(positions[1]["symbol"], "ETH/USDT:USDT")

        print("Finished test_get_open_positions")

    def test_get_pending_orders(self):  # TODO: @Jirka: Please check me after implementation
        # TODO: @Lucka
        print("Start test_get_pending_orders")

        print("Create small limit orders on BTC and ETH")
        # buy limit btc on 20 000 USD
        # buy limit eth on 1500 USD
        self.create_small_btc_long_position("limit", 20000)
        self.create_small_eth_long_position("limit", 1500)

        print("Get pending orders")
        pending_orders = self.exchange.fetch_open_orders()  # TODO: implement me
        print("Pending orders: {}".format(pending_orders))

        # TODO: write asserts on response (result), exists 2 open orders, btc and eth
        self.assertEqual(len(pending_orders), 2)
        self.assertEqual(pending_orders[0]["symbol"], "BTC/USDT:USDT")
        self.assertEqual(pending_orders[1]["symbol"], "ETH/USDT:USDT")

        print("Finished test_get_pending_orders")

    def test_cancel_all_pending_orders(self): # TODO: @Jirka: Please check me after implementation
        # TODO: @Lucka
        print("Start test_cancel_all_pending_orders")

        print("Create small limit orders on BTC and ETH")
        # buy limit btc on 20 000 USD
        # buy limit eth on 1500 USD
        self.create_small_btc_long_position("limit", 20000)
        self.create_small_eth_long_position("limit", 1500)

        print("Get pending orders")
        pending_orders = self.exchange.fetch_open_orders()  # TODO: implement me
        print("Pending response orders: {}".format(pending_orders))

        # TODO: write asserts on response (result), exists 2 open orders, btc and eth
        self.assertEqual(len(pending_orders), 2)
        self.assertEqual(pending_orders[0]["symbol"], "BTC/USDT:USDT")
        self.assertEqual(pending_orders[1]["symbol"], "ETH/USDT:USDT")

        print("Cancel all pending orders")
        cancel_orders_response = self.exchange.cancel_all_derivatives_orders()
        print("Cancel orders response: {}".format(cancel_orders_response))

        print("Get pending orders")
        pending_orders_response = self.exchange.fetch_open_orders()  # TODO: implement me
        print("Pending orders response: {}".format(pending_orders_response))

        # TODO: verify not open any pending orders
        self.assertEqual(len(pending_orders_response), 0)

        print("Finished test_cancel_all_pending_orders")

    def test_cancel_all_positions(self): # TODO: @Jirka: Please check me after implementation
        print("Start test_cancel_all_positions")

        print("Create small positions on BTC and ETH")
        self.create_small_btc_long_position()
        self.create_small_eth_long_position()

        print("Get positions")
        positions = self.exchange.fetch_derivatives_positions()
        print("Positions: {}".format(positions))

        self.assertEqual(len(positions), 2)
        self.assertEqual(positions[0]["symbol"], "BTC/USDT:USDT")
        self.assertEqual(positions[1]["symbol"], "ETH/USDT:USDT")

        print("Cancel all positions")  # TODO: @Lucka implement me
        for position in positions:
            position_info = position["info"]
            self.exchange.create_order(symbol=position_info["symbol"],
                                       type="market",
                                       side="Sell" if position_info["side"] == "Buy" else "Buy",
                                       amount=position_info["size"],
                                       params={
                                           "positionIdx": position_info["positionIdx"],
                                           "reduceOnly": True})

        print("Get positions")
        positions = self.exchange.fetch_derivatives_positions()
        print("Positions: {}".format(positions))

        # TODO: @Lucka verify 0 positions on exchange
        self.assertEqual(len(positions), 0)

        print("Finished test_cancel_all_positions")

    def test_set_hedge_mode(self):
        print("Start test_set_hedge_mode")
        response = self.exchange.set_position_mode(hedged=True)
        print("Response {}".format(response))

        self.assertEqual(response["retCode"], "0")
        self.assertEqual(response["retMsg"], "All symbols switched successfully.")
        print("Finished test_set_hedge_mode")

    def test_change_margin_mode_to_cross(self):
        print("Start test_change_margin_mode")
        try:
            response = self.exchange.set_margin_mode(
                marginMode="CROSS",
                symbol="ETHUSDT",
                params={
                    "buy_leverage": 1,
                    "sell_leverage": 1,
                    "category": "linear"
                })
            print("Response: {}".format(response))

            self.assertEqual(response["retCode"], "0")
            self.assertEqual(response["retMsg"], "OK")
        except Exception as e:
            if "Isolated not modified" not in str(e):
                raise e

        print("Finished test_change_margin_mode")

    def test_change_leverage(self):
        print("Start test_change_leverage")
        try:
            response = self.exchange.set_leverage(leverage=30, symbol="ETHUSDT")
            print("Response: {}".format(response))

            self.assertEqual(response["retCode"], "0")
            self.assertEqual(response["retMsg"], "OK")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
        print("Finished test_change_leverage")

    def test_change_buy_and_sell_leverage_in_hedge_mode(self):
        print("Start test_change_buy_and_sell_leverage_in_hedge_mode")
        try:
            self.exchange.set_position_mode(hedged=True)
            response = self.exchange.set_buy_and_sell_leverage(buyLeverage=30, sellLeverage=20, symbol="ETHUSDT")
            print("Response: {}".format(response))

            self.assertEqual(response["retCode"], "0")
            self.assertEqual(response["retMsg"], "OK")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
        print("Finished Start test_change_buy_and_sell_leverage_in_hedge_mode")

    def create_small_btc_long_position(self, type_of_order="market", limit_price=None):
        return self.exchange.create_order(symbol="BTCUSDT",
                                          type=type_of_order,
                                          side="buy",
                                          amount=0.001,
                                          price=limit_price,
                                          params={
                                              "positionIdx": 0
                                          })

    def create_small_eth_long_position(self, type_of_order="market", limit_price=None):
        return self.exchange.create_order(symbol="ETHUSDT",
                                          type=type_of_order,
                                          side="buy",
                                          amount=0.01,
                                          price=limit_price,
                                          params={
                                              "positionIdx": 0
                                          })

    def set_default_setting(self):
        print("Set one-way trading mode")
        self.exchange.set_position_mode(hedged=False)

        print("Set isolated margin mode on BTC and default leverage")
        try:
            self.exchange.set_margin_mode(
                marginMode="ISOLATED",
                symbol="BTCUSDT",
                params={
                    "buy_leverage": 20,
                    "sell_leverage": 20,
                    "category": "linear"
                })
        except Exception as e:
            if "Isolated not modified" not in str(e):
                raise e

        print("Set isolated margin mode on ETH and default leverage")
        try:
            self.exchange.set_margin_mode(
                marginMode="ISOLATED",
                symbol="ETHUSDT",
                params={
                    "buy_leverage": 20,
                    "sell_leverage": 20,
                    "category": "linear"
                })
        except Exception as e:
            if "Isolated not modified" not in str(e):
                raise e

        print("Set default leverage for BTC")
        try:
            self.exchange.set_leverage(leverage=20, symbol="BTCUSDT")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e

        print("Set default leverage for ETH")
        try:
            self.exchange.set_leverage(leverage=20, symbol="ETHUSDT")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
