import json

from web3 import Web3
from web3 import HTTPProvider
from web3 import Account

# 3-4 funkcije koje sluze za rad

from configuration import BLOCKCHAIN_URL


# web3 instanca - komunikacija sa blockchainom
# kontejner se pokrece pre simulatora - problem
# zato se pravi objekat ovaj po potrebi
def get_web3():
    return Web3(HTTPProvider(BLOCKCHAIN_URL))


def send_transaction(transaction, private_key):
    web3 = get_web3()

    signed_transaction = web3.eth.account.sign_transaction(
        transaction, private_key)
    transaction_hash = web3.eth.send_raw_transaction(
        signed_transaction.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    return receipt


def read_file(path):
    with open(path, "r") as file:
        return file.read()


def get_owner_account():
    web3 = get_web3()

    data = json.loads(read_file("owner_account.json"))

    address = web3.to_checksum_address(data["address"])

    # moram dekriptovati privatni kljuc - pravili json fajl pomocu etherwalleta
    private_key = Account.decrypt(data, "iepblockchain").hex()

    balance = web3.eth.get_balance(address)

    # proverava se da li postoji novac na racunu, inace se prebaci sa nultom racuna na ovaj
    if (balance <= web3.to_wei(1, "ether")):
        result = web3.eth.send_transaction({
            "from": web3.eth.accounts[0],
            "to": address,
            "value": web3.to_wei(2, "ether"),
            "gasPrice": 1
        })

    return (address, private_key)
