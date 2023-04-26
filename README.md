# crypto-exchanges-tests

Integration tests for top cryptocurrency derivative exchanges.

Purpose of the project is to be able to implement a basic puzzles (operation for individual exchanges), so that we can quickly react to competitive offers (better trading fees, leverage, cheaper asset transfers, new functions of derivative exchanges).


## Exchanges

### Binance
Binance is a cryptocurrency exchange that was founded in 2017 by Changpeng Zhao. It is one of the largest and most popular cryptocurrency exchanges in the world, with a wide range of trading pairs and low trading fees. Binance offers a variety of services, including spot trading, margin trading, futures trading, and more. The exchange has its own cryptocurrency, called Binance Coin (BNB), which can be used to pay for trading fees and other services on the platform. Binance is known for its user-friendly interface, advanced trading features, and strong security measures.

* [Testnet](https://testnet.binancefuture.com/en/futures/BTCUSDT)
* [Api doc](https://www.binance.com/en-AU/binance-api)

### Bybit
Bybit is a cryptocurrency derivatives exchange that allows traders to trade perpetual contracts for several cryptocurrencies such as Bitcoin, Ethereum, Ripple, EOS, and more. It was founded in March 2018 and is registered in the British Virgin Islands. Bybit aims to provide a seamless trading experience with advanced order types, high liquidity, and high leverage. The exchange offers a range of tools and features to help traders manage their risk, including a multi-tiered liquidation system and an insurance fund. Bybit also provides a user-friendly interface with advanced charting tools and a customizable trading dashboard.

* [Testnet](https://testnet.bybit.com/en-US/)
* [Api doc](https://www.bybit.com/future-activity/en-US/developer)

### Phemex
Phemex is a cryptocurrency derivatives trading platform that was launched in 2019. The exchange is headquartered in Singapore and has a global presence, with users from over 200 countries. Phemex supports a wide range of cryptocurrencies, including Bitcoin, Ethereum, Ripple, and many others, and provides users with a secure and reliable platform for trading.

Phemex is known for its high-speed trading engine, which can process up to 300,000 transactions per second. The exchange offers a range of trading tools and features, including perpetual contracts, futures contracts, and options trading. Additionally, Phemex provides users with a mobile app for both iOS and Android, making it easy for traders to manage their portfolios on the go.

One of the unique features of Phemex is its zero-fee spot trading platform, which allows users to trade cryptocurrencies with zero trading fees. The exchange also offers a range of educational resources and trading tools to help traders improve their skills and maximize their profits. Overall, Phemex is a reputable and reliable cryptocurrency exchange that offers a range of advanced features and tools for traders of all levels.

* [Testnet](https://testnet.phemex.com/)
* [Api doc](https://phemex.com/user-guides/api-overview)

### BTCEX
BTCEX is a full-category digital asset trading platform that provides spot trading and derivative trading such as margin, quarterly contracts, perpetual contracts, and options.

The platform claims to cover both beginners and advanced users. The exchange provides hundreds of trading pairs, low trading fees, a wide array of coins, referral programs, copy trading for amateurs, fast registration process, specialized mobile applications, leveraged trading and robust security. API is available for professional traders as well.

Of the competitive advantages, a full complex of trading services, spot trading, leverage, and derivatives are available. Among the shortcomings is the lack of support for fiat currency.

* Testnet not support (verify date 26.4.2023)
* [Api doc](https://docs.btcex.com/#introduction)

## How to run
```commandline
python -m unittest discover -s tests/integration
```

## Technologies
* Python 3
* Exchanges api
* unittest