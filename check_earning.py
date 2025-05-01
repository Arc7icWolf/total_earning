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


def fetch_history(session: requests.Session, account, symbol):
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

        all_results.extend(data)
        offset += limit
        
    return all_results
    

def check_earning(session: requests.Session, account, symbol):
    history = fetch_history(session, account, symbol)

    for h in history:
        if h['from'] = "golem.market":
            pass
    



def main():
    account = "arc7icwolf"
    symbol = "VYB"
    try:
        with requests.Session() as session:
            check_earning(session, account, symbol)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"JSON decode error or missing key: {e}")
    # except Exception as e:
    #    logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
