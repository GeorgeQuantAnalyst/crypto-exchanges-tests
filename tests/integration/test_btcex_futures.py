import unittest

import ccxt

class BtcexFuturesTest(unittest.TestCase):
    # Test only public methods, because exchange not support testnet
    # Btcex exchange support buy_btc_by_stop_order_with_take_profit_and_stop_loss and place_trailing_stop by spec

    def setUp(self) -> None:
        self.exchange = ccxt.btcex()

        # NotSupported: btcex does not have a sandbox URL
        # self.exchange.set_sandbox_mode(True)
        pass

    def test_get_btc_current_price(self):
        pass

    def test_get_btc_daily_ohlc(self):
        pass

    def test_get_btcusdt_info(self):
        pass


