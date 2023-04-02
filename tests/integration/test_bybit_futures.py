import unittest

from pybit import usdt_perpetual

from exchanges.bybit_extend import BybitExtend
from utils import load_config


class BybitFuturesTest(unittest.TestCase):

    def setUp(self) -> None:
        config = load_config("../config.yaml")
        self.exchange = BybitExtend({
            "apiKey": config["bybitApi"]["apiKey"],
            "secret": config["bybitApi"]["secretKey"]}
        )
        self.pybit_client = usdt_perpetual.HTTP(
            endpoint=config["bybitApi"]["url"],
            api_key=config["bybitApi"]["apiKey"],
            api_secret=config["bybitApi"]["secretKey"]
        )
        self.exchange.set_sandbox_mode(True)

    def test_get_btc_current_price(self):
        pass

    def test_get_btc_daily_ohlc(self):
        pass

    def test_get_instruments_info(self):
        pass

    def test_get_available_balance_on_account(self):
        pass

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
