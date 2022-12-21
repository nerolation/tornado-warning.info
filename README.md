# eth-tornado-warning

This project used different tools to deliver the final information to [tornado-warning.info](https://tornado-warning.info/):
* [Ethereum-datafarm](https://github.com/Nerolation/ethereum-datafarm) for collecting transactions with Events from the Tornado Cash contracts.
* [Relay Data API](https://flashbots.notion.site/Relay-API-Spec-5fb0819366954962bc02e81cb33840f5) for collecting information about relayed/mev-boosted blocks.
* Web3.py + Infura

---

### Code 

The scripts in [this repo](https://github.com/Nerolation/mevboost.pics) have the following purpose:
* parse_data_api.py - For parsing the Relay Data API.
* enrich_data.py - For adding information (block number, fee_recipient, #txs) to the parsed blocks.
* tornado_data_prep.py - For creating a table with mev-boosted blocks that contain Tornado Cash transactions.
* tornadomap.py - For creating the map and the final html file, ready to be deployed.
