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


def get_response(payload, session: requests.Session):
    urls = ["https://api.hive-engine.com/rpc/contracts"]
    for url in urls:
        response = session.post(url, json=payload)

        if response.status_code != 200:
            continue

        result = response.json()#.get("result", [])
        print(result)
        if result:
            return result

        print(f"Error: Status Code: {response.status_code}")


def create_payload(receiver, symbol, session: requests.Session):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "find",
        "params": {
            "contract": "tokens",
            "table": "transfer",
            "query": {
                "from": receiver
            },
            "limit": 100,
            "offset": 0,
            "indexes": []
        }
    }

    result = get_response(payload, session)
    return result


def check_earning(receiver, symbol, session: requests.Session):
    result = create_payload(receiver, symbol, session)
    print(len(result))
    for r in result:
        print(r)
        break


def main():
    sender = "golem.overlord"
    receiver = "arc7icwolf"
    symbol = "SWAP.HIVE"
    try:
        with requests.Session() as session:
            check_earning(receiver, symbol, session)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"JSON decode error or missing key: {e}")
    # except Exception as e:
    #    logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
