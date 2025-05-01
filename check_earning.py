import requests
import json
import logging


# logger
def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("check_earning.log", mode="a")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = get_logger()


def fetch_history(account, symbol, session: requests.Session):
    all_history = []
    limit = 1000
    offset = 0

    while True:
        url = "https://history.hive-engine.com/accountHistory"
        params = {
            "account": account,
            "symbol": symbol,
            "limit": limit,
            "offset": offset
        }
        response = session.get(url, params=params)
        if response.status_code != 200:
            continue

        data = response.json()

        if not data:
            break # all history fetched

        all_history.extend(data)
        offset += limit
        
    return all_history
    

def check_earning(account, symbol, session: requests.Session):
    total_hive = 0
    
    history = fetch_history(account, symbol, session)

    for h in history:
        if h.get('from', []) == "golem.market" and symbol == "SWAP.HIVE": # Get SWAP.HIVE withdrawal
            total_hive += float(h['quantity'])

        if h.get('operation', []) == "market_sell":
            if h.get('symbol', []) == "ANIMA" or h.get('symbol', []) == "SHARD": # Get ANIMA and SHARD sold on the market
                total_hive += float(h['quantityHive'])

    print(round(total_hive, 2), symbol)
    



def main():
    account = "arc7icwolf"
    symbols = ["SWAP.HIVE", "SHARD", "ANIMA"]
    for symbol in symbols:
        try:
            with requests.Session() as session:
                check_earning(account, symbol, session)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"JSON decode error or missing key: {e}")
        # except Exception as e:
        #    logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
