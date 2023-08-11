# cryptocurrency-trading-bot-on-Django
Automated trading bot for working with cryptocurrency futures on the Binance exchange via API.
Multi-cryptocurrency trading bot trades futures on the Binance exchange with major high-capitalization instruments such as Bitcoin, Ethereum, BNB, and others. 

# Features:

- Balance inquiry
- Query of current positions
- Lot calculation for positions
- Adjustment of leverage
- Opening positions
- Condition-based position closure
- Selective position closure
- Addition to open position
- Profit and loss calculation for selective position
- Profit and loss calculation for selective combinations of positions
- Calculation of average statistical profit and loss sizes for strategy
- Calculation of maximum profit and loss sizes for strategy
- Balance inquiry, open positions, unrealized profit query through Telegram bot
- Receipt of notifications through Telegram bot on deal openings, closures, and various bot statuses

# Strategy
A risk hedging and dual-direction trading strategy is applied, enabling both long and short positions simultaneously. This ensures independence from the price movement direction. Stop-loss and take-profit are not set as static values; their calculation and adjustment are continuous.

# Settings
To connect to your account, you need to enter your API keys in the services/api_keys.py file.
To connect the Telegram bot, you need to enter your Telegram user_id and your Telegram bot's token in the views/tg_token.py file.
