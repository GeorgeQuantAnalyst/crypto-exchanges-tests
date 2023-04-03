import unittest

import requests
from pybit import usdt_perpetual

from exchanges.bybit_extend import BybitExtend
from utils import load_config


class BybitFuturesTest(unittest.TestCase):

    def setUp(self) -> None:
        self.config = load_config("../config.yaml")
        self.exchange = BybitExtend({
            "apiKey": self.config["bybitApi"]["apiKey"],
            "secret": self.config["bybitApi"]["secretKey"]}
        )
        self.pybit_client = usdt_perpetual.HTTP(
            endpoint=self.config["bybitApi"]["url"],
            api_key=self.config["bybitApi"]["apiKey"],
            api_secret=self.config["bybitApi"]["secretKey"]
        )
        self.exchange.set_sandbox_mode(True)

    def test_get_btc_current_price(self):
        url = "https://api-testnet.bybit.com/v5/market/orderbook?category={}&symbol={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("linear", "BTCUSDT"), headers=headers, data=payload).json()
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

    def test_get_btc_daily_ohlc(self):
        url = "https://api-testnet.bybit.com/v5/market/kline?category={}&symbol={}&interval={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("linear", "BTCUSDT", "D"), headers=headers, data=payload).json()
        result = response["result"]
        ohlc_daily = result["list"]

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        self.assertTrue(len(ohlc_daily) > 1)

    def test_get_instruments_info(self):
        url = "https://api-testnet.bybit.com/v5/market/instruments-info?category={}&symbol={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("linear", "BTCUSDT", headers=headers, payload=payload)).json()
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

    def test_get_available_usdt_balance_on_account(self):
        response = self.exchange.fetch_balance({"coin": "USDT"})
        total_balance = float(response["USDT"]["total"])
        free_balance = float(response["USDT"]["free"])

        print("Total balance: {} USDT, Free balance: {} USDT".format(round(total_balance, 2), round(free_balance, 2)))

        self.assertEqual(response["info"]["retCode"], "0")
        self.assertEqual(response["info"]["retMsg"], "OK")
        self.assertTrue(total_balance >= 0)
        self.assertTrue(free_balance >= 0)

    def test_buy_btc_by_market_order(self):
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="market",
                                              side="buy",
                                              amount=0.001,
                                              params={
                                                  "positionIdx": 1})

        self.assertTrue("id" in response)

    def test_sell_btc_by_market_order(self):
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="market",
                                              side="sell",
                                              amount=0.001,
                                              params={
                                                  "positionIdx": 2})

        self.assertTrue("id" in response)

    def test_buy_btc_by_limit_order(self):
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="limit",
                                              side="buy",
                                              amount=0.001,
                                              price=20000,
                                              params={
                                                  "positionIdx": 1})

        self.assertTrue("id" in response)

    def test_sell_btc_by_limit_order(self):
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="limit",
                                              side="sell",
                                              amount=0.001,
                                              price=30000,
                                              params={
                                                  "positionIdx": 2})

        self.assertTrue("id" in response)

    def test_buy_btc_with_take_profit_and_stop_loss(self):
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="limit",
                                              side="buy",
                                              amount=0.001,
                                              price=20000,
                                              params={
                                                  "triggerPrice": "20000",
                                                  "takeProfit": "22000",
                                                  "stopLoss": "18000",
                                                  "positionIdx": 1})

        self.assertTrue("id" in response)

    def test_place_trailing_stop(self):
        # Actually not implemented in CCXT library, you must use pybit library
        pass

    def test_get_open_positions(self):
        pass

    def test_get_pending_orders(self):
        pass

    def test_cancel_all_pending_orders(self):
        pass

    def test_cancel_all_open_positions(self):
        pass

    def test_set_hedge_mode(self):
        response = self.exchange.set_position_mode(hedged=True)

        self.assertEqual(response["retCode"], "0")
        self.assertEqual(response["retMsg"], "All symbols switched successfully.")

    def test_change_margin_mode(self):
        try:
            response = self.exchange.set_margin_mode(
                marginMode="ISOLATED",
                symbol="ETHUSDT",
                params={
                    "buy_leverage": 1,
                    "sell_leverage": 1,
                    "category": "linear"
                })

            self.assertEqual(response["retCode"], "0")
            self.assertEqual(response["retMsg"], "OK")
        except Exception as e:
            if "Isolated not modified" not in str(e):
                raise e

    def test_change_buy_and_sell_leverage(self):
        try:
            response = self.exchange.set_buy_and_sell_leverage(buyLeverage=30, sellLeverage=20, symbol="ETHUSDT")

            self.assertEqual(response["retCode"], "0")
            self.assertEqual(response["retMsg"], "OK")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
