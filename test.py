import requests

def get_history(account, symbol, limit=10, offset=0):
    url = "https://history.hive-engine.com/accountHistory"
    params = {
        "account": account,
        "symbol": symbol,
        "limit": limit,
        "offset": offset
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Errore nella richiesta: {response.status_code}")


result = get_history("arc7icwolf", "SWAP.HIVE")

print(result)
