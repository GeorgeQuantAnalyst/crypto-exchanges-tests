import unittest

import requests
import ccxt

from utils import load_config


class BinanceFuturesTest(unittest.TestCase):
    def setUp(self) -> None:
        print("Start SetUp")

        print("Load config")
        self.config = load_config("../config.yaml")

        print("Init CCXT Binance client")
        self.exchange = ccxt.binance({
            "apiKey": self.config["binanceApi"]["apiKey"],
            "secret": self.config["binanceApi"]["secretKey"]}
        )

        self.exchange.set_sandbox_mode(True)
       # self.set_default_setting()

        print("Finished SetUp")

    # TODO: @ Lucka doupravit a dokoncit tak aby bylo funkcni
    # def tearDown(self) -> None:
    #     print("Start Tear down")
    #
    #     print("Cancel all derivatives orders")
    #     orders = self.exchange.fetch_orders()
    #     for order in orders:
    #         order_info = order["info"]
    #         self.exchange.cancel_all_orders(symbol=order_info["symbol"])
    #
    #     print("Cancel all derivatives positions")
    #     positions = self.exchange.fetch_positions()
    #     for position in positions:
    #         position_info = position["info"]
    #         self.exchange.create_order(symbol=position_info["symbol"],
    #                                    type="market",
    #                                    side="Sell" if position_info["side"] == "Buy" else "Buy",
    #                                    amount=position_info["size"],
    #                                    params={
    #                                        "positionIdx": position_info["positionIdx"],
    #                                        "reduceOnly": True})

       # self.set_default_setting()

        print("Finished Tear down")

    def test_get_btc_current_price(self):
        print("Start test_get_btc_current_price")
        url = "https://api.binance.com/api/v3/depth?limit={}&symbol={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format(10, "BTCUSDT"), headers=headers, data=payload).json()
        print("Response: {}".format(response))
        bid = float(response["bids"][0][0])
        ask = float(response["asks"][0][0])
        spread = ask - bid

        print("Bid price is: {}, ask price is: {} and spread is: {}".format(bid, ask, spread))

        self.assertTrue(bid > 0)
        self.assertTrue(ask > 0)
        self.assertTrue(bid < ask)

        print("Finished test_get_btc_current_price")

    def test_get_btc_daily_ohlc(self):
        print("Start test_get_btc_daily_ohlc")
        url = "https://fapi.binance.com/fapi/v1/klines?symbol={}&interval={}"

        response = requests.request("GET", url.format("BTCUSDT", "1d")).json()
        print("Response: {}".format(response))

        self.assertTrue(len(response) > 1)
        print("Finished test_get_btc_daily_ohlc")

    def test_get_btcusdt_info(self):
        print("Start test_get_btcusdt_info")
        url = "https://fapi.binance.com/fapi/v1/exchangeInfo"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format(headers=headers, payload=payload)).json()
        print("Response: {}".format(response))

        btc_info = response["symbols"][0]

        print(btc_info)

        # Base info
        self.assertEqual(btc_info["symbol"], "BTCUSDT")
        self.assertEqual(btc_info["contractType"], "PERPETUAL")
        self.assertEqual(btc_info["onboardDate"], 1569398400000)
        self.assertEqual(btc_info["pricePrecision"], 2)
        self.assertEqual(btc_info["quoteAsset"], "USDT")

        # Lot size filter
        self.assertEqual(btc_info["filters"][2]["maxQty"], "120")
        self.assertEqual(btc_info["filters"][2]["minQty"], "0.001")
        self.assertEqual(btc_info["filters"][2]["stepSize"], "0.001")

        print("Finished test_get_btcusdt_info")

    def test_get_available_usdt_balance_on_account(self):
        print("Start test_get_available_usdt_balance_on_account")
        response = self.exchange.fetch_balance({"type": "future"})  # TODO: @lucka dokoncit metodu
        print("Response: {}".format(response))

    # TODO: @ Lucka doupravit a dokoncit tak aby bylo funkcni
    #def set_default_setting(self):
        # print("Set one-way trading mode")
        # self.exchange.set_position_mode(hedged=False)

        # print("Set isolated margin mode on BTC and default leverage")
        # try:
        #     self.exchange.set_margin_mode(
        #         marginMode="ISOLATED",
        #         symbol="BTCUSDT",
        #         params={
        #             "buy_leverage": 20,
        #             "sell_leverage": 20,
        #             "category": "linear"
        #         })
        # except Exception as e:
        #     if "Isolated not modified" not in str(e):
        #         raise e

        # print("Set isolated margin mode on ETH and default leverage")
        # try:
        #     self.exchange.set_margin_mode(
        #         marginMode="ISOLATED",
        #         symbol="ETHUSDT",
        #         params={
        #             "buy_leverage": 20,
        #             "sell_leverage": 20,
        #             "category": "linear"
        #         })
        # except Exception as e:
        #     if "Isolated not modified" not in str(e):
        #         raise e
        #
        # print("Set default leverage for BTC")
        # try:
        #     self.exchange.set_leverage(leverage=20, symbol="BTCUSDT")
        # except Exception as e:
        #     if "leverage not modified" not in str(e):
        #         raise e
        #
        # print("Set default leverage for ETH")
        # try:
        #     self.exchange.set_leverage(leverage=20, symbol="ETHUSDT")
        # except Exception as e:
        #     if "leverage not modified" not in str(e):
        #         raise e
