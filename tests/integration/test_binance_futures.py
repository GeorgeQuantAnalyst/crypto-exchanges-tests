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
        self.set_default_setting()

        print("Finished SetUp")

    def tearDown(self) -> None:
        print("Start Tear down")

        print("Cancel all pending orders")
        symbols = ["BTC/USDT:USDT", "ETH/USDT:USDT", "SOL/USDT:USDT"]

        print("Get pending orders")
        open_orders_response = [x for x in symbols if self.exchange.fetch_open_orders(x)]
        print("Pending response orders: {}".format(open_orders_response))

        print("Cancel all pending orders")
        for x in open_orders_response:
            cancel_orders_response = self.exchange.cancel_all_orders(x)
            print("Cancel orders response: {}".format(cancel_orders_response))

        print("Finished cancel all pending orders")

        print("Cancel all positions")

        print("Get positions")
        response = self.exchange.fetch_positions()
        print("Filtering active positions")
        active_positions = [x for x in response if float(x["info"]["positionAmt"]) != 0]
        print("Active positions: {}".format(active_positions))
        print("Finished get positions")

        print("Cancel all positions")
        for position in active_positions:
            position_info = position["info"]
            self.exchange.create_order(symbol=position["symbol"],
                                       type="market",
                                       side="sell" if position["side"] == "long" else "buy",
                                       amount=abs(float(position_info["positionAmt"])),
                                       params={
                                           "reduceOnly": True})

        print("Finished cancel all positions")
        self.set_default_setting()
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
        response = self.exchange.fetch_balance({"type": "future"})
        print("Response: {}".format(response))

        total_balance = float(response["USDT"]["total"])
        free_balance = float(response["USDT"]["free"])
        used_balance = float(response["USDT"]["used"])

        print("Total balance is: {} USDT, Free balance is: {} USDT, Used balance is: {} USDT".format(
            round(total_balance, 2),
            round(free_balance, 2),
            round(used_balance, 2)))

        self.assertTrue(total_balance >= 0)
        self.assertTrue(free_balance >= 0)
        self.assertTrue(used_balance == 0)

        print("Finished test_get_available_usdt_balance_on_account")

    def test_buy_btc_by_market_order(self):
        print("Start test_buy_btc_by_market_order")
        response = self.exchange.create_order(symbol="BTC/USDT:USDT",
                                              type="market",
                                              side="buy",
                                              amount=0.001
                                              )

        print("Response: {}".format(response))
        self.assertTrue("id" in response)

        print("Finished test_buy_btc_by_market_order")

    def test_sell_btc_by_market_order(self):
        print("Start test_sell_btc_by_market_order")
        response = self.exchange.create_order(symbol="BTC/USDT:USDT",
                                              type="market",
                                              side="sell",
                                              amount=0.001
                                              )

        print("Response: {}".format(response))
        self.assertTrue("id" in response)
        print("Finished test_sell_btc_by_market_order")

    def test_buy_btc_by_limit_order(self):
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

    def test_sell_btc_by_limit_order(self):
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

    def test_buy_btc_with_take_profit_and_stop_loss(self):
        raise Exception("Api actually not supported this function - verify date 24.4.2023")

    def test_place_trailing_stop(self):
        print("Start test_place_trailing_stop")
        print("Create small position on BTC")
        self.create_small_btc_long_position()

        print("Get positions")
        response = self.exchange.fetch_positions()
        print("Response: {}".format(response))

        print("Create trailing stop")
        response = self.exchange.create_order(
            symbol="BTC/USDT:USDT",
            type="TRAILING_STOP_MARKET",
            side="sell",
            amount=0.001,
            params={
                "reduceOnly": True,
                'callbackRate': 5
            })

        print("Response {}".format(response))
        self.assertEqual(response["symbol"], "BTC/USDT:USDT")
        self.assertEqual(response["info"]["status"], "NEW")
        self.assertEqual(response["type"], "trailing_stop_market")
        self.assertEqual(response["reduceOnly"], True)
        self.assertEqual(response["timeInForce"], "GTC")
        self.assertTrue(0.001, response["amount"])

        print("Finished creating trailing stop")
        print("Finished test_place_trailing_stop")

    def test_get_positions(self):
        print("Start test_get_open_positions")

        print("Create small positions on BTC and ETH")
        self.create_small_btc_long_position()
        self.create_small_eth_short_position()

        print("Get positions")
        response = self.exchange.fetch_positions()
        print("Response: {}".format(response))

        active_positions = [x for x in response if float(x["info"]["positionAmt"]) != 0]
        print("Active positions: {}".format(active_positions))

        self.assertEqual(len(active_positions), 2)
        self.assertTrue("BTCUSDT" in [x["info"]["symbol"] for x in active_positions])
        self.assertTrue("ETHUSDT" in [x["info"]["symbol"] for x in active_positions])

        print("Finished test_get_open_positions")

    def test_get_pending_orders(self):
        print("Start test_cancel_all_pending_orders")

        print("Create small limit orders on BTC and ETH")
        # buy limit btc on 20 000 USD
        # sell limit eth on 2500 USD
        self.create_small_btc_long_position("limit", 20000)
        self.create_small_eth_short_position("limit", 2500)

        symbols = ["BTC/USDT:USDT", "ETH/USDT:USDT", "SOL/USDT:USDT"]

        print("Get pending orders")

        open_orders_response = [x for x in symbols if self.exchange.fetch_open_orders(x)]

        print("Pending response orders: {}".format(open_orders_response))

        self.assertEqual(len(open_orders_response), 2)
        self.assertTrue("BTC/USDT:USDT" in [x for x in open_orders_response])
        self.assertTrue("ETH/USDT:USDT" in [x for x in open_orders_response])

    def test_cancel_all_pending_orders(self):
        print("Start test_cancel_all_pending_orders")

        print("Create small limit orders on BTC and ETH")
        # buy limit btc on 20 000 USD
        # sell limit eth on 2500 USD
        self.create_small_btc_long_position("limit", 20000)
        self.create_small_eth_short_position("limit", 2500)

        symbols = ["BTC/USDT:USDT", "ETH/USDT:USDT", "SOL/USDT:USDT"]

        print("Get pending orders")

        open_orders_response = [x for x in symbols if self.exchange.fetch_open_orders(x)]

        print("Pending response orders: {}".format(open_orders_response))

        self.assertEqual(len(open_orders_response), 2)
        self.assertTrue("BTC/USDT:USDT" in [x for x in open_orders_response])
        self.assertTrue("ETH/USDT:USDT" in [x for x in open_orders_response])

        print("Cancel all pending orders")
        for x in open_orders_response:
            cancel_orders_response = self.exchange.cancel_all_orders(x)
            print("Cancel orders response: {}".format(cancel_orders_response))

        print("Get pending orders")
        pending_orders_response = [x for x in symbols if self.exchange.fetch_open_orders(x)]
        print("Pending orders response: {}".format(pending_orders_response))

        self.assertEqual(len(pending_orders_response), 0)

        print("Finished test_cancel_all_pending_orders")

    def test_cancel_all_positions(self):
        print("Start test_cancel_all_positions")

        print("Create small positions on BTC and ETH")
        self.create_small_btc_long_position()
        self.create_small_eth_short_position()

        print("Get positions")
        response = self.exchange.fetch_positions()
        print("Response: {}".format(response))

        active_positions = [x for x in response if float(x["info"]["positionAmt"]) != 0]
        print("Active positions: {}".format(active_positions))

        self.assertEqual(len(active_positions), 2)
        self.assertTrue("BTCUSDT" in [x["info"]["symbol"] for x in active_positions])
        self.assertTrue("ETHUSDT" in [x["info"]["symbol"] for x in active_positions])

        print("Finished filtering active position")

        print("Cancel all positions")
        for position in active_positions:
            position_info = position["info"]
            self.exchange.create_order(symbol=position["symbol"],
                                       type="market",
                                       side="sell" if position["side"] == "long" else "buy",
                                       amount=abs(float(position_info["positionAmt"])),
                                       params={
                                           "reduceOnly": True})

        print("Finished cancel all positions")

        print("Get positions")
        response = self.exchange.fetch_positions()
        print("Response: {}".format(response))

        active_positions = [x for x in response if float(x["info"]["positionAmt"]) > 0]
        print("Active positions: {}".format(active_positions))

        self.assertEqual(len(active_positions), 0)

        print("Finished test_cancel_all_positions")

    def test_set_hedge_mode(self):
        print("Start test_set_hedge_mode")
        response = self.exchange.set_position_mode(hedged=True)
        print("Response {}".format(response))

        self.assertEqual(response["code"], "200")
        self.assertEqual(response["msg"], "success")
        print("Finished test_set_hedge_mode")

    def test_change_margin_mode_to_cross(self):
        print("Start test_change_margin_type")
        response = self.exchange.set_margin_mode(
            marginMode="CROSS",
            symbol="ETH/USDT:USDT"
        )
        print("Response: {}".format(response))

        self.assertEqual(response["code"], "200")
        self.assertEqual(response["msg"], "success")

        print("Finished test_change_margin_type")

    def test_change_leverage(self):
        print("Start test_change_leverage")
        try:
            response = self.exchange.set_leverage(leverage=30, symbol="ETH/USDT:USDT")
            print("Response: {}".format(response))

            self.assertEqual(response["symbol"], "ETHUSDT")
            self.assertEqual(response["leverage"], "30")

        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
        print("Finished test_change_leverage")

    def test_change_buy_and_sell_leverage_in_hedge_mode(self):
        raise Exception("Api actually not supported this function - verify date 24.4.2023")

    def create_small_btc_long_position(self, type_of_order="market",
                                       limit_price=None):
        return self.exchange.create_order(symbol="BTC/USDT:USDT",
                                          type=type_of_order,
                                          side="buy",
                                          amount=0.001,
                                          price=limit_price
                                          )

    def create_small_eth_short_position(self, type_of_order="market",
                                        limit_price=None):
        return self.exchange.create_order(symbol="ETH/USDT:USDT",
                                          type=type_of_order,
                                          side="sell",
                                          amount=0.01,
                                          price=limit_price,
                                          )

    def set_default_setting(self):
        try:
            print("Set one-way trading mode")
            self.exchange.set_position_mode(hedged=False)
        except Exception as e:
            if "No need to change position side." not in str(e):
                raise e

        print("Set isolated margin mode on BTC and default leverage")

        self.exchange.set_margin_mode(
            marginMode="ISOLATED",
            symbol="BTC/USDT:USDT"
        )

        print("Set isolated margin mode on ETH and default leverage")
        self.exchange.set_margin_mode(
            marginMode="ISOLATED",
            symbol="ETH/USDT:USDT"
        )

        print("Set default leverage for BTC")
        try:
            self.exchange.set_leverage(leverage=20, symbol="BTC/USDT:USDT")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e

        print("Set default leverage for ETH")
        try:
            self.exchange.set_leverage(leverage=20, symbol="ETH/USDT:USDT")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
