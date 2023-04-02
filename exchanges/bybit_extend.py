from typing import Optional

from ccxt import bybit, NotSupported


class BybitExtend(bybit):

    def set_buy_and_sell_leverage(self, buyLeverage: float, sellLeverage: float, symbol: Optional[str] = None,
                                  params={}):
        """
        set the level of buy and sell leverage for a market
        :param float buyLeverage: the rate of buy leverage
        :param: float sellLeverage: the rate of sell leverage
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the bybit api endpoint
        :returns dict: response from the exchange
        """
        self.check_required_symbol('setLeverage', symbol)
        self.load_markets()
        market = self.market(symbol)
        # WARNING: THIS WILL INCREASE LIQUIDATION PRICE FOR OPEN ISOLATED LONG POSITIONS
        # AND DECREASE LIQUIDATION PRICE FOR OPEN ISOLATED SHORT POSITIONS
        isUsdcSettled = market['settle'] == 'USDC'
        enableUnifiedMargin, enableUnifiedAccount = self.is_unified_enabled()
        # engage in leverage setting
        # we reuse the code here instead of having two methods
        buyLeverage = self.number_to_string(buyLeverage)
        sellLeverage = self.number_to_string(sellLeverage)
        method = None
        request = None
        if enableUnifiedMargin or enableUnifiedAccount or not isUsdcSettled:
            request = {
                'symbol': market['id'],
                'buyLeverage': buyLeverage,
                'sellLeverage': sellLeverage,
            }
            if enableUnifiedAccount:
                if market['linear']:
                    request['category'] = 'linear'
                else:
                    raise NotSupported(
                        self.id + ' setUnifiedMarginLeverage() leverage doesn\'t support inverse and option market in unified account')
                method = 'privatePostV5PositionSetLeverage'
            elif enableUnifiedMargin:
                if market['option']:
                    request['category'] = 'option'
                elif market['linear']:
                    request['category'] = 'linear'
                else:
                    raise NotSupported(
                        self.id + ' setUnifiedMarginLeverage() leverage doesn\'t support inverse market in unified margin')
                method = 'privatePostUnifiedV3PrivatePositionSetLeverage'
            else:
                method = 'privatePostContractV3PrivatePositionSetLeverage'
        else:
            request = {
                'symbol': market['id'],
                'leverage': leverage,
            }
            method = 'privatePostPerpetualUsdcOpenapiPrivateV1PositionLeverageSave'
        return getattr(self, method)(self.extend(request, params))
