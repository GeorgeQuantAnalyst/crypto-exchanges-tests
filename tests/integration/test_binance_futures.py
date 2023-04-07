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
    #     print("Cancel all orders")
    #     orders = self.exchange.cancel_all_orders()
    #     for order in orders:
    #         order_info = order["info"]
    #         self.exchange.cancel_all_orders(symbol=order_info["symbol"])
    #
    #     print("Cancel all positions")
    #     positions = self.exchange.fetch_positions()
    #    for position in positions:
    #             position_info = position["info"]
    #             self.exchange.create_order(symbol=position_info["symbol"],
    #                                        type="market",
    #                                        side="short" if position["side"] == "long" else "long",
    #                                        amount=position["side"],
    #                                        params={
    #                                            "reduceOnly": True})

       # self.set_default_setting()

        # print("Finished Tear down")

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

    def test_get_btc_daily_ohlc(self):  # TODO: @lucka zkontrolovat metodu
        print("Start test_get_btc_daily_ohlc")
        url = "https://fapi.binance.com/fapi/v1/klines?symbol={}&interval={}"

        response = requests.request("GET", url.format("BTCUSDT", "1d")).json()
        print("Response: {}".format(response))

        self.assertTrue(len(response) > 1)
        print("Finished test_get_btc_daily_ohlc")

    def test_get_btcusdt_info(self):  # TODO: @lucka zkontrolovat metodu
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

    def test_get_available_usdt_balance_on_account(self):  # TODO: @lucka zkontrolovat metodu
        print("Start test_get_available_usdt_balance_on_account")
        response = self.exchange.fetch_balance({"type": "future"})
        print("Response: {}".format(response))

    def test_buy_btc_by_market_order(self):  # TODO: @lucka dokoncit metodu zkontrolovat permisions for api
        print("Start test_buy_btc_by_market_order")
        response = self.exchange.create_order(symbol="BTC/USDT:USDT",
                                              type="market",
                                              side="buy",
                                              amount=0.001
                                              )

        print("Response: {}".format(response))
        self.assertTrue("id" in response)

        print("Finished test_buy_btc_by_market_order")

    def test_sell_btc_by_market_order(self):  # TODO: @lucka zkontrolovat metodu
        print("Start test_sell_btc_by_market_order")
        response = self.exchange.create_order(symbol="BTC/USDT:USDT",
                                              type="market",
                                              side="sell",
                                              amount=0.001
                                              )

        print("Response: {}".format(response))
        self.assertTrue("id" in response)
        print("Finished test_sell_btc_by_market_order")

    def test_buy_btc_by_limit_order(self):  # TODO: @lucka dokoncit metodu zkontrolovat permisions for api
        print("Start test_buy_btc_by_limit_order")
        response = self.exchange.create_order(symbol="BTC/USDT:USDT",
                                              type="limit",
                                              side="buy",
                                              amount=0.001,
                                              price=20000
                                              )

        print("Response: {}".format(response))
        self.assertTrue("id" in response)

        print("Finished test_buy_btc_by_limit_order")

    def test_sell_btc_by_limit_order(self):  # TODO: @lucka zkontrolovat metodu
        print("Start test_sell_btc_by_limit_order")
        response = self.exchange.create_order(symbol="BTC/USDT:USDT",
                                              type="limit",
                                              side="sell",
                                              amount=0.001,
                                              price=30000
                                              )
        print("Response: {}".format(response))
        self.assertTrue("id" in response)

        print("Finished test_sell_btc_by_limit_order")

    def test_get_positions(self):  # TODO: @lucka dokoncit metodu
        print("Start test_get_open_positions")

        print("Create small positions on BTC and ETH")
        self.create_small_btc_long_position()
        self.create_small_eth_long_position()

        print("Get positions")
        positions = self.exchange.fetch_positions()
        print(positions)

        self.assertEqual(len(positions["contracts"] == 0), 2)  # TODO: @lucka zjistit jak vyfilrovat otevrene pozice
        self.assertEqual(positions["symbol"], "BTC/USDT:USDT")
        self.assertEqual(positions["symbol"], "ETH/USDT:USDT")

        print("Finished test_get_open_positions")

    def create_small_btc_long_position(self, type_of_order="market", limit_price=None):  # TODO: @lucka zkontrolovat metodu
        return self.exchange.create_order(symbol="BTC/USDT:USDT",
                                          type=type_of_order,
                                          side="buy",
                                          amount=0.001,
                                          price=limit_price
                                          )

    def create_small_eth_long_position(self, type_of_order="market", limit_price=None):  # TODO: @lucka zkontrolovat metodu
        return self.exchange.create_order(symbol="ETH/USDT:USDT",
                                          type=type_of_order,
                                          side="buy",
                                          amount=0.01,
                                          price=limit_price,
                                          )


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
