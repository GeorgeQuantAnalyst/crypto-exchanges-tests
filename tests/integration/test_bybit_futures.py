import unittest

from pybit.unified_trading import HTTP

from utils import load_config


class BybitFuturesTest(unittest.TestCase):
    CATEGORY = "linear"

    def setUp(self) -> None:
        print("Start SetUp")

        print("Load config")
        self.config = load_config("../config.yaml")

        print("Init exchange client")
        self.exchange = HTTP(
            testnet=self.config["bybitApi"]["testnet"],
            api_key=self.config["bybitApi"]["apiKey"],
            api_secret=self.config["bybitApi"]["secretKey"]
        )

        self.set_default_setting()

        print("Finished SetUp")

    def tearDown(self) -> None:
        print("Start Tear down")

        print("Cancel all derivatives orders")
        self.exchange.cancel_all_orders(category=self.CATEGORY, settleCoin="USDT")

        print("Cancel all derivatives positions")
        positions = self.exchange.get_positions(category=self.CATEGORY, settleCoin="USDT")

        for position in positions["result"]["list"]:
            self.exchange.place_order(
                category=self.CATEGORY,
                symbol=position["symbol"],
                orderType="Market",
                side="Sell" if position["side"] == "Buy" else "Buy",
                qty=position["size"],
                positionIdx=position["positionIdx"],
                reduceOnly=True)

        self.set_default_setting()

        print("Finished Tear down")

    def test_get_btc_current_price(self):
        print("Start test_get_btc_current_price")

        response = self.exchange.get_orderbook(
            category=self.CATEGORY,
            symbol="BTCUSDT"
        )

        print("Response: {}".format(response))
        result = response["result"]
        bid = float(result["b"][0][0])
        ask = float(result["a"][0][0])
        spread = ask - bid

        print("Bid price is: {}, ask price is: {} and spread is: {}".format(bid, ask, round(spread, 3)))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        self.assertTrue(bid > 0)
        self.assertTrue(ask > 0)
        self.assertTrue(bid < ask)

        print("Finished test_get_btc_current_price")

    def test_get_btc_daily_ohlc(self):
        print("Start test_get_btc_daily_ohlc")

        response = self.exchange.get_kline(
            category=self.CATEGORY,
            symbol="BTCUSDT",
            interval="D"
        )

        print("Response: {}".format(response))
        result = response["result"]
        ohlc_daily = result["list"]

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        self.assertTrue(len(ohlc_daily) > 1)
        print("Finished test_get_btc_daily_ohlc")

    def test_get_btcusdt_info(self):
        print("Start test_get_btcusdt_info")

        response = self.exchange.get_instruments_info(
            category=self.CATEGORY,
            symbol="BTCUSDT"
        )

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

        response = self.exchange.get_wallet_balance(
            accountType="CONTRACT",
            coin="USDT"
        )
        print("Response: {}".format(response))

        total_balance = float(response["result"]["list"][0]["coin"][0]["walletBalance"])
        free_balance = float(response["result"]["list"][0]["coin"][0]["availableToWithdraw"])

        print("Total balance: {} USDT, Free balance: {} USDT".format(round(total_balance, 2), round(free_balance, 2)))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        self.assertTrue(total_balance >= 0)
        self.assertTrue(free_balance >= 0)
        print("Finished test_get_available_usdt_balance_on_account")

    def test_buy_btc_by_market_order(self):
        print("Start test_buy_btc_by_market_order")
        response = self.exchange.place_order(
            category=self.CATEGORY,
            symbol="BTCUSDT",
            side="Buy",
            orderType="Market",
            qty=0.001,
            positionIdx=0)

        print("Response: {}".format(response))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        print("Finished test_buy_btc_by_market_order")

    def test_sell_btc_by_market_order(self):
        print("Start test_sell_btc_by_market_order")
        response = self.exchange.place_order(
            category=self.CATEGORY,
            symbol="BTCUSDT",
            side="Sell",
            orderType="Market",
            qty=0.001,
            positionIdx=0)

        print("Response: {}".format(response))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        print("Finished test_sell_btc_by_market_order")

    def test_buy_btc_by_limit_order(self):
        print("Start test_buy_btc_by_limit_order")
        response = self.exchange.place_order(
            category=self.CATEGORY,
            symbol="BTCUSDT",
            side="Buy",
            orderType="Limit",
            price="20000",
            qty=0.001,
            positionIdx=0)

        print("Response: {}".format(response))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        print("Finished test_buy_btc_by_limit_order")

    def test_sell_btc_by_limit_order(self):
        print("Start test_sell_btc_by_limit_order")
        response = self.exchange.place_order(
            category=self.CATEGORY,
            symbol="BTCUSDT",
            side="Sell",
            orderType="Limit",
            price="30000",
            qty=0.001,
            positionIdx=0)

        print("Response: {}".format(response))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        print("Finished test_sell_btc_by_limit_order")

    def test_buy_btc_by_stop_order_with_take_profit_and_stop_loss(self):
        print("Start test_buy_btc_by_stop_order_with_take_profit_and_stop_loss")
        response = self.exchange.place_order(
            category=self.CATEGORY,
            symbol="BTCUSDT",
            side="Buy",
            orderType="Limit",
            qty=0.001,
            price=20000,
            triggerDirection=2,
            triggerPrice="20000",
            positionIdx=0,
            takeProfit="22000",
            stopLoss="18000"
        )

        print("Response: {}".format(response))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        print("Finished test_buy_btc_by_stop_order_with_take_profit_and_stop_loss")

    def test_place_trailing_stop(self):
        print("Start test_place_trailing_stop")

        print("Open small position on BTC")
        create_order_response = self.create_small_btc_long_position()

        print("Create trailing stop 100 USD")
        trailing_stop_response = self.exchange.set_trading_stop(
            category=self.CATEGORY,
            symbol="BTCUSDT",
            trailingStop="100",
            positionIdx=0
        )

        print("Create order response: {}".format(create_order_response))
        print("Trailing stop response: {}".format(trailing_stop_response))

        self.assertTrue("orderId" in create_order_response["result"])
        self.assertEqual(trailing_stop_response["retCode"], 0)
        self.assertEqual(trailing_stop_response["retMsg"], "OK")

        print("Finished test_place_trailing_stop")

    def test_get_positions(self):
        print("Start test_get_open_positions")

        print("Create small positions on BTC and ETH")
        self.create_small_btc_long_position()
        self.create_small_eth_long_position()

        print("Get positions")
        positions = self.exchange.get_positions(category=self.CATEGORY, settleCoin="USDT")
        print(positions)

        self.assertEqual(positions["retCode"], 0)
        self.assertEqual(positions["retMsg"], "OK")
        self.assertEqual(len(positions["result"]["list"]), 2)
        self.assertEqual(positions["result"]["list"][0]["symbol"], "BTCUSDT")
        self.assertEqual(positions["result"]["list"][1]["symbol"], "ETHUSDT")

        print("Finished test_get_open_positions")

    def test_get_pending_orders(self):
        print("Start test_get_pending_orders")

        print("Create small limit orders on BTC and ETH")
        # buy limit btc on 20 000 USD
        # buy limit eth on 1500 USD
        self.create_small_btc_long_position("Limit", 20000)
        self.create_small_eth_long_position("Limit", 1500)

        print("Get pending orders")
        pending_orders = self.exchange.get_open_orders(category=self.CATEGORY, settleCoin="USDT")
        print("Pending orders: {}".format(pending_orders))

        self.assertEqual(pending_orders["retCode"], 0)
        self.assertEqual(pending_orders["retMsg"], "OK")
        self.assertEqual(len(pending_orders["result"]["list"]), 2)
        self.assertEqual(pending_orders["result"]["list"][1]["symbol"], "BTCUSDT")
        self.assertEqual(pending_orders["result"]["list"][0]["symbol"], "ETHUSDT")

        print("Finished test_get_pending_orders")

    def test_cancel_all_pending_orders(self):
        print("Start test_cancel_all_pending_orders")

        print("Create small limit orders on BTC and ETH")
        # buy limit btc on 20 000 USD
        # buy limit eth on 1500 USD
        self.create_small_btc_long_position("Limit", 20000)
        self.create_small_eth_long_position("Limit", 1500)

        print("Get pending orders")
        pending_orders = self.exchange.get_open_orders(category=self.CATEGORY, settleCoin="USDT")
        print("Pending response orders: {}".format(pending_orders))

        self.assertEqual(pending_orders["retCode"], 0)
        self.assertEqual(pending_orders["retMsg"], "OK")
        self.assertEqual(len(pending_orders["result"]["list"]), 2)
        self.assertEqual(pending_orders["result"]["list"][1]["symbol"], "BTCUSDT")
        self.assertEqual(pending_orders["result"]["list"][0]["symbol"], "ETHUSDT")

        print("Cancel all pending orders")
        cancel_orders_response = self.exchange.cancel_all_orders(category=self.CATEGORY, settleCoin="USDT")
        print("Cancel orders response: {}".format(cancel_orders_response))

        print("Get pending orders")
        pending_orders_response = self.exchange.get_open_orders(category=self.CATEGORY, settleCoin="USDT")
        print("Pending orders response: {}".format(pending_orders_response))

        self.assertEqual(len(pending_orders_response["result"]["list"]), 0)

        print("Finished test_cancel_all_pending_orders")

    def test_cancel_all_positions(self):
        print("Start test_cancel_all_positions")

        print("Create small positions on BTC and ETH")
        self.create_small_btc_long_position()
        self.create_small_eth_long_position()

        print("Get positions")
        positions = self.exchange.get_positions(category=self.CATEGORY, settleCoin="USDT")
        print("Positions: {}".format(positions))

        self.assertEqual(positions["retCode"], 0)
        self.assertEqual(positions["retMsg"], "OK")
        self.assertEqual(len(positions["result"]["list"]), 2)
        self.assertEqual(positions["result"]["list"][0]["symbol"], "BTCUSDT")
        self.assertEqual(positions["result"]["list"][1]["symbol"], "ETHUSDT")

        print("Cancel all positions")
        for position in positions["result"]["list"]:
            self.exchange.place_order(
                category=self.CATEGORY,
                symbol=position["symbol"],
                orderType="Market",
                side="Sell" if position["side"] == "Buy" else "Buy",
                qty=position["size"],
                positionIdx=position["positionIdx"],
                reduceOnly=True)

        print("Get positions")
        positions = self.exchange.get_positions(category=self.CATEGORY, settleCoin="USDT")
        print("Positions: {}".format(positions))

        self.assertEqual(positions["retCode"], 0)
        self.assertEqual(positions["retMsg"], "OK")
        self.assertEqual(len(positions["result"]["list"]), 0)

        print("Finished test_cancel_all_positions")

    def test_set_hedge_mode(self):
        print("Start test_set_hedge_mode")
        response = self.exchange.switch_position_mode(category=self.CATEGORY, coin="USDT", mode=3)
        print("Response {}".format(response))

        self.assertEqual(response["retCode"], 0)
        self.assertEqual(response["retMsg"], "OK")
        print("Finished test_set_hedge_mode")

    def test_change_margin_mode_to_cross(self):
        print("Start test_change_margin_mode")
        try:
            response = self.exchange.switch_margin_mode(
                category=self.CATEGORY,
                symbol="ETHUSDT",
                tradeMode=0,
                buyLeverage="1",
                sellLeverage="1"
                )
            print("Response: {}".format(response))

            self.assertEqual(response["retCode"], 0)
            self.assertEqual(response["retMsg"], "OK")
        except Exception as e:
            if "Isolated not modified" not in str(e):
                raise e

        print("Finished test_change_margin_mode")

    def test_change_leverage(self):
        print("Start test_change_leverage")
        try:
            response = self.exchange.set_leverage(
                category=self.CATEGORY,
                buyLeverage="30",
                sellLeverage="30",
                symbol="DOGEUSDT")
            print("Response: {}".format(response))

            self.assertEqual(response["retCode"], 0)
            self.assertEqual(response["retMsg"], "OK")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
        print("Finished test_change_leverage")

    def test_change_buy_and_sell_leverage_in_hedge_mode(self):
        print("Start test_change_buy_and_sell_leverage_in_hedge_mode")
        try:
            self.exchange.switch_position_mode(category=self.CATEGORY, coin="USDT", mode=3)
            response = self.exchange.set_leverage(
                category=self.CATEGORY,
                buyLeverage="30",
                sellLeverage="20",
                symbol="ETHUSDT")
            print("Response: {}".format(response))

            self.assertEqual(response["retCode"], 0)
            self.assertEqual(response["retMsg"], "OK")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
        print("Finished Start test_change_buy_and_sell_leverage_in_hedge_mode")

    def create_small_btc_long_position(self, type_of_order="Market", limit_price=None):
        return self.exchange.place_order(
            category=self.CATEGORY,
            symbol="BTCUSDT",
            orderType=type_of_order,
            side="Buy",
            qty=0.001,
            price=limit_price,
            positionIdx=0
        )

    def create_small_eth_long_position(self, type_of_order="Market", limit_price=None):
        return self.exchange.place_order(
            category=self.CATEGORY,
            symbol="ETHUSDT",
            orderType=type_of_order,
            side="Buy",
            qty=0.01,
            price=limit_price,
            positionIdx=0
        )

    def set_default_setting(self):
        print("Set one-way trading mode")
        self.exchange.switch_position_mode(category=self.CATEGORY, coin="USDT", mode=0)

        print("Set isolated margin mode on BTC and default leverage")
        try:
            self.exchange.switch_margin_mode(
                category=self.CATEGORY,
                symbol="BTCUSDT",
                tradeMode=1,
                buyLeverage="1",
                sellLeverage="1"
                )
        except Exception as e:
            if "Cross/isolated margin mode is not modified" not in str(e):
                raise e

        print("Set isolated margin mode on ETH and default leverage")
        try:
            self.exchange.switch_margin_mode(
                category=self.CATEGORY,
                symbol="ETHUSDT",
                tradeMode=1,
                buyLeverage="1",
                sellLeverage="1"
                )
        except Exception as e:
            if "Cross/isolated margin mode is not modified" not in str(e):
                raise e

        print("Set default leverage for BTC")
        try:
            self.exchange.set_leverage(
                category=self.CATEGORY,
                buyLeverage="20",
                sellLeverage="20",
                symbol="BTCUSDT")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e

        print("Set default leverage for ETH")
        try:
            self.exchange.set_leverage(
                category=self.CATEGORY,
                buyLeverage="20",
                sellLeverage="20",
                symbol="ETHUSDT")
        except Exception as e:
            if "leverage not modified" not in str(e):
                raise e
