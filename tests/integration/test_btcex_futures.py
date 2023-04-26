import unittest

import ccxt
import requests

import datetime


class BtcexFuturesTest(unittest.TestCase):
    # Test only public methods, because exchange not support testnet
    # Btcex exchange support buy_btc_by_stop_order_with_take_profit_and_stop_loss and place_trailing_stop by spec

    def setUp(self) -> None:
        self.exchange = ccxt.btcex()

        # NotSupported: btcex does not have a sandbox URL
        # self.exchange.set_sandbox_mode(True)
        pass

    def test_get_btc_current_price(self):
        print("Start test_get_btc_current_price")
        url = "https://api.btcex.com/api/v1/public/get_order_book?instrument_name={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("BTC-USDT-PERPETUAL"), headers=headers, data=payload).json()
        print("Response: {}".format(response))
        result = response["result"]
        bid = float(result["bids"][0][0])
        ask = float(result["asks"][0][0])
        spread = ask - bid

        print("Bid price is: {}, ask price is: {} and spread is: {}".format(bid, ask, spread))

        self.assertTrue(bid > 0)
        self.assertTrue(ask > 0)
        self.assertTrue(bid < ask)

        print("Finished test_get_btc_current_price")

    def test_get_btc_daily_ohlc(self):
        print("Start test_get_btc_current_price")
        url = "https://api.btcex.com/api/v1/public/get_tradingview_chart_data?instrument_name={}&start_timestamp={}&end_timestamp={}&resolution={}"

        payload = {}
        headers = {}

        print("Format datetime")
        five_day_before = datetime.datetime.now() - datetime.timedelta(5)
        unix_time = five_day_before.strftime("%s")  # Second as a decimal number (or Unix Timestamp)

        print("Get response")
        response = requests.request("GET", url.format("BTC-USDT", datetime.datetime.now(), unix_time, "1D"),
                                    headers=headers, data=payload).json()
        print("Response: {}".format(response))
        ohlc_daily = response["result"]

        self.assertTrue(len(ohlc_daily) > 1)

        print("Finished test_get_btc_current_price")

    def test_get_btcusdt_info(self):
        url = "https://api.btcex.com/api/v1/public/get_instruments?currency={}&base_currency={}"

        payload = {}
        headers = {}

        response = requests.request("GET", url.format("PERPETUAL", "USDT", headers=headers, payload=payload)).json()
        print("Response: {}".format(response))
        result = response["result"]

        btc_info = result[0]

        # Base info
        self.assertEqual(btc_info["instrument_name"], "BTC-USDT-PERPETUAL")
        self.assertEqual(btc_info["currency"], "PERPETUAL")
        self.assertEqual(btc_info["show_name"], "BTCUSDT")
        self.assertEqual(btc_info["quote_currency"], "BTC")
        self.assertEqual(btc_info["creation_timestamp"], "1631004005882")
        self.assertEqual(btc_info["base_currency"], "USDT")

        # Leverage
        self.assertEqual(btc_info["leverage"], 200)

        # Lot size filter
        self.assertEqual(btc_info["min_qty"], "0.001")

        print("Finished test_get_btcusdt_info")
