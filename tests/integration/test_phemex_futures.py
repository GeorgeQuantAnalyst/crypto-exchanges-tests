import unittest

import ccxt
import requests

from tests.integration.utils import load_config


class PhemexFuturesTest(unittest.TestCase):

    def setUp(self) -> None:
        print("Start SetUp")

        print("Load config")
        self.config = load_config("../config.yaml")

        print("Init CCXT Phemex client")
        self.exchange = ccxt.phemex({
            "apiKey": self.config["phemexApi"]["apiKey"],
            "secret": self.config["phemexApi"]["secretKey"]
        })

        self.exchange.load_markets()
        self.exchange.set_sandbox_mode(True)
        self.set_default_setting()

        print("Finished SetUp")

    def tearDown(self) -> None:
        print("Start Tear down")

        print("Cancel all derivatives orders on BTCUSDT and ETHUSDT")
        self.exchange.cancel_all_orders("BTCUSDT")
        self.exchange.cancel_all_orders("BTCUSDT", params={"untriggered": True})

        self.exchange.cancel_all_orders("ETHUSDT")
        self.exchange.cancel_all_orders("ETHUSDT", params={"untriggered": True})

        print("Cancel all derivatives positions on BTCUSDT and ETHUSDT")
        positions = self.exchange.fetch_positions(symbols=["BTCUSDT", "ETHUSDT"])
        for position in positions:
            position_info = position["info"]

            if position_info["side"] == 'None':
                continue

            self.exchange.create_order(symbol=position_info["symbol"],
                                       type="market",
                                       side="Sell" if position_info["side"] == "Buy" else "Buy",
                                       amount=position_info["size"],
                                       params={"reduceOnly": True})

        self.set_default_setting()

        print("Finished Tear down")

    def test_get_btc_current_price(self):
        url = "https://testnet-api.phemex.com/md/orderbook?symbol={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("BTCUSD"), headers=headers, data=payload).json()
        result = response["result"]
        bid = result["book"]["bids"][0][0] / 10000
        ask = result["book"]["asks"][0][0] / 10000
        spread = ask - bid

        print("Bid price is: {}, ask price is: {} and spread is: {}".format(bid, ask, spread))

        self.assertEqual(response["id"], 0)
        self.assertEqual(response["error"], None)
        self.assertEqual(response["result"]["symbol"], "BTCUSD")
        self.assertTrue(bid > 0)
        self.assertTrue(ask > 0)
        self.assertTrue(bid < ask)
        print(response)
        pass

    def test_get_btc_daily_ohlc(self):
        print("Start test_get_btc_daily_ohlc")
        url = "https://testnet-api.phemex.com/exchange/public/md/v2/kline?symbol={}&resolution={}&limit={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("BTCUSD", 86400, 100), headers=headers, data=payload).json()
        print("Response: {}".format(response))
        ohlc_daily = response["data"]["rows"]

        self.assertEqual(response["code"], 0)
        self.assertEqual(response["msg"], "OK")
        self.assertTrue(len(ohlc_daily) == 100)
        print("Finished test_get_btc_daily_ohlc")

    def test_get_btcusdt_info(self):
        print("Start test_get_btcusdt_info")
        url = "https://testnet-api.phemex.com/public/products"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload).json()
        print("Response: {}".format(response))

        btc_info = None
        for product in response["data"]["perpProductsV2"]:
            if product["symbol"] == "BTCUSDT":
                btc_info = product

        print("BTCUSDT info: {}".format(btc_info))

        self.assertEqual(response["code"], 0)
        self.assertEqual(response["msg"], "")

        # Base info
        self.assertTrue(btc_info is not None)
        self.assertEqual(btc_info["symbol"], "BTCUSDT")
        self.assertEqual(btc_info["type"], "PerpetualV2")
        self.assertEqual(btc_info["listTime"], 1662854400000)
        self.assertEqual(btc_info["priceScale"], 0)
        self.assertEqual(btc_info["fundingInterval"], 28800)
        self.assertEqual(btc_info["settleCurrency"], "USDT")

        # Leverage filter
        self.assertEqual(btc_info["maxLeverage"], 100)

        # Lot size filter
        self.assertEqual(btc_info["maxOrderQtyRq"], "100000")
        self.assertEqual(btc_info["minOrderValueRv"], "1")
        self.assertEqual(btc_info["qtyStepSize"], "0.001")

        print("Finished test_get_btcusdt_info")

    def test_get_available_usdt_balance_on_account(self) -> None:
        # Support only get available balance on spot account
        print("Start test_get_available_usdt_balance_on_account")

        response = self.exchange.fetch_balance(params={"currency": "USDT"})
        print("Response: {}".format(response))

        total_balance = float(response["total"]["USDT"])
        free_balance = float(response["free"]["USDT"])

        print("Total balance: {} USDT, Free balance: {} USDT".format(round(total_balance, 2), round(free_balance, 2)))

        self.assertEqual(response["info"]["code"], "0")
        self.assertEqual(response["info"]["msg"], "")
        self.assertTrue(total_balance >= 0)
        self.assertTrue(free_balance >= 0)

        print("Finished test_get_available_usdt_balance_on_account")

    def test_buy_btc_by_market_order(self) -> None:
        print("Start test_buy_btc_by_market_order")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="market",
                                              side="buy",
                                              amount=0.001)
        print("Response: {}".format(response))

        self.assertTrue("orderID" in response["info"])
        print("Finished test_buy_btc_by_market_order")

    def test_sell_btc_by_market_order(self):
        print("Start test_sell_btc_by_market_order")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="market",
                                              side="sell",
                                              amount=0.001)
        print("Response: {}".format(response))

        self.assertTrue("orderID" in response["info"])
        print("Finished test_sell_btc_by_market_order")

    def test_buy_btc_by_limit_order(self):
        print("Start test_buy_btc_by_limit_order")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="limit",
                                              side="buy",
                                              amount=0.001,
                                              price=20000)
        print("Response: {}".format(response))

        self.assertTrue("orderID" in response["info"])
        print("Finished test_buy_btc_by_limit_order")

    def test_sell_btc_by_limit_order(self):
        print("Start test_sell_btc_by_limit_order")
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="limit",
                                              side="sell",
                                              amount=0.001,
                                              price=30000)
        print("Response: {}".format(response))

        self.assertTrue("orderID" in response["info"])

        print("Finished test_sell_btc_by_limit_order")

    def test_buy_btc_by_stop_order_with_take_profit_and_stop_loss(self):
        print("Start test_buy_btc_by_stop_order_with_take_profit_and_stop_loss")

        markets = self.exchange.load_markets()
        market = markets["BTC/USDT"]

        # TODO: Jirka solve error ccxt.base.errors.InvalidOrder: phemex {"code":11046,"msg":"TE_TRIGGER_PRICE_TOO_SMALL","data":null}
        print("stopPxEp: {}".format(self.exchange.to_ep("25000", market)))
        response = self.exchange.create_order(symbol="BTCUSDT",
                                              type="LimitIfTouched",
                                              side="buy",
                                              amount=0.001,
                                              price=25000,
                                              params={
                                                  "stopPxEp": self.exchange.to_ep("25000", market),
                                                  "priceEp": self.exchange.to_ep("25000", market),
                                                  "triggerType": "ByLastPrice"})
        print("Response: {}".format(response))

        self.assertTrue("orderID" in response["info"])
        print("Finished test_buy_btc_by_stop_order_with_take_profit_and_stop_loss")

    def test_place_trailing_stop(self):
        pass

    def test_get_positions(self):
        pass

    def test_get_pending_orders(self):
        pass

    def test_cancel_all_pending_orders(self):
        pass

    def test_cancel_all_positions(self):
        pass

    def test_set_hedge_mode(self):
        pass

    def test_change_margin_mode_to_cross(self):
        pass

    def test_change_leverage(self):
        pass

    def test_change_buy_and_sell_leverage_in_hedge_mode(self):
        pass

    def set_default_setting(self) -> None:
        print("Set one-way trading mode")
        self.exchange.set_position_mode(hedged=False, symbol="BTCUSDT")

        print("Set isolated margin mode and default leverage on BTC")
        self.exchange.set_leverage(leverage=20, symbol="BTCUSDT")

        print("Set isolated margin mode and default leverage on ETH")
        self.exchange.set_leverage(leverage=20, symbol="ETHUSDT")
