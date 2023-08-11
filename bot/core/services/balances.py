import json

from core.services.base import um_futures_client


def total_balance():
    response = um_futures_client.account(recvWindow=50000)
    with open('my_txt/balance.txt', 'w') as fw:
        pass
    total_balance = float(response['totalWalletBalance'])
    with open('my_txt/balance.txt', 'w') as fw:
        json.dump(f"{total_balance:.{2}f}", fw)
    return total_balance

def balance():
    response = um_futures_client.account(recvWindow=50000)
    balance = float(response['totalMarginBalance'])
    return balance
