# crypto-exchanges-tests

Integration tests for top cryptocurrency derivative exchanges.

Purpose of the project is to be able to implement a basic puzzle (operation for individual exchanges), so that we can quickly react to competitive offers (better trading fees, leverage, cheaper asset transfers, new functions of derivative exchanges).


## Exchanges

### Binance
Binance is a cryptocurrency exchange that was founded in 2017 by Changpeng Zhao. It is one of the largest and most popular cryptocurrency exchanges in the world, with a wide range of trading pairs and low trading fees. Binance offers a variety of services, including spot trading, margin trading, futures trading, and more. The exchange has its own cryptocurrency, called Binance Coin (BNB), which can be used to pay for trading fees and other services on the platform. Binance is known for its user-friendly interface, advanced trading features, and strong security measures.

* [Testnet]()
* [Api doc]()

### Bybit
Bybit is a cryptocurrency derivatives exchange that allows traders to trade perpetual contracts for several cryptocurrencies such as Bitcoin, Ethereum, Ripple, EOS, and more. It was founded in March 2018 and is registered in the British Virgin Islands. Bybit aims to provide a seamless trading experience with advanced order types, high liquidity, and high leverage. The exchange offers a range of tools and features to help traders manage their risk, including a multi-tiered liquidation system and an insurance fund. Bybit also provides a user-friendly interface with advanced charting tools and a customizable trading dashboard.

* [Testnet]()
* [Api doc]()

### Okx
OKEx is a cryptocurrency exchange that was founded in 2017 and is based in Malta. The exchange offers a wide range of cryptocurrency trading pairs, including Bitcoin, Ethereum, Litecoin, and many others. In addition to spot trading, OKEx also offers derivatives trading, including futures and options. The exchange is known for its high trading volumes and deep liquidity, making it a popular choice for both individual and institutional traders.

OKEx offers a variety of trading tools and features to help traders manage their risk and maximize their profits. These include a margin trading system, which allows traders to borrow funds to trade with, and a stop-loss feature, which can help minimize losses in the event of a market downturn. The exchange also offers a mobile app for both iOS and Android, making it easy for traders to stay up to date on their trades while on the go.
* [Testnet]()
* [Api doc]()

### Mexc
MEXC Exchange is a cryptocurrency exchange platform that was launched in 2018. The exchange is headquartered in Singapore. MEXC Exchange supports a wide range of cryptocurrencies, including Bitcoin, Ethereum, Litecoin, and many others, and provides users with a secure and reliable platform for trading.

One of the unique features of MEXC Exchange is its "Rocket Program," which aims to support and incubate promising blockchain projects by providing them with resources and assistance in launching their tokens. The exchange also offers a wide range of trading tools and features, including a spot trading platform, margin trading, and a futures trading platform. Additionally, MEXC Exchange provides users with a mobile app for both iOS and Android, making it easy for traders to manage their portfolios on the go.

* [Testnet]()
* [Api doc]()

### Gate.io
Gate.io is a cryptocurrency exchange platform that was launched in 2017. The exchange is headquartered in the Cayman Islands and has a global presence, with offices in several countries around the world. Gate.io supports a wide range of cryptocurrencies, including Bitcoin, Ethereum, Litecoin, and many others, and provides users with a secure and reliable platform for trading.

One of the unique features of Gate.io is its user-friendly interface, which makes it easy for both novice and experienced traders to buy, sell, and trade cryptocurrencies. The exchange also offers a wide range of trading tools and features, including a spot trading platform, margin trading, and a futures trading platform. Additionally, Gate.io provides users with a mobile app for both iOS and Android, making it easy for traders to manage their portfolios on the go.

Gate.io has also implemented a number of security measures to protect users' assets, including two-factor authentication, cold storage of funds, and regular security audits. Overall, Gate.io is a reputable and reliable cryptocurrency exchange that offers a range of features and tools for traders of all levels.

* [Testnet]()
* [Api doc]()

### Phemex
Phemex is a cryptocurrency derivatives trading platform that was launched in 2019. The exchange is headquartered in Singapore and has a global presence, with users from over 200 countries. Phemex supports a wide range of cryptocurrencies, including Bitcoin, Ethereum, Ripple, and many others, and provides users with a secure and reliable platform for trading.

Phemex is known for its high-speed trading engine, which can process up to 300,000 transactions per second. The exchange offers a range of trading tools and features, including perpetual contracts, futures contracts, and options trading. Additionally, Phemex provides users with a mobile app for both iOS and Android, making it easy for traders to manage their portfolios on the go.

One of the unique features of Phemex is its zero-fee spot trading platform, which allows users to trade cryptocurrencies with zero trading fees. The exchange also offers a range of educational resources and trading tools to help traders improve their skills and maximize their profits. Overall, Phemex is a reputable and reliable cryptocurrency exchange that offers a range of advanced features and tools for traders of all levels.

* [Testnet]()
* [Api doc]()

### Dydx
dYdX is a decentralized cryptocurrency exchange that runs on the Ethereum blockchain. It was founded in 2017 and is headquartered in San Francisco, California. dYdX allows users to trade cryptocurrencies and tokens in a peer-to-peer manner, without the need for a centralized intermediary.

One of the key features of dYdX is its support for margin trading, which allows users to borrow funds to trade with. The exchange also supports perpetual contracts, which are a type of futures contract that do not have an expiry date. dYdX is known for its user-friendly interface and low fees, which make it an attractive option for both novice and experienced traders.

As a decentralized exchange, dYdX offers users a high degree of security and privacy. Trades are executed through smart contracts on the Ethereum blockchain, which ensures that users always maintain control over their funds. Additionally, dYdX supports a wide range of cryptocurrencies and tokens, including Bitcoin, Ethereum, and many others. Overall, dYdX is a reputable and reliable decentralized exchange that offers a range of advanced features and tools for traders of all levels.

* [Testnet]()
* [Api doc]()

## How to run
```commandline
python -m unittest discover -s tests/integration
```

## Technologies
* Python 3
* Exchanges api
* unittest