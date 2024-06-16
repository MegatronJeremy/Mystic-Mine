from web3 import Account
from web3 import HTTPProvider
from web3 import Web3
import secrets
import requests
OWNER_URL = "http://localhost:5000"
COURIER_URL = "http://localhost:5001"
CUSTOMER_URL = "http://localhost:5002"
BLOCKCHAIN_URL = "http://127.0.0.1:8545"

# ISTO KAO OPCIJA - da napisemo python skriptu koja simulira rad sa sistemom

# ovde gomilu poziva koji salju zahteve sistemu
# da nam da promenimo sistem na neki nacin, i da napisemo python skriptu koja ce da izvrsi simulaciju rada sa tim sistemom

# requests biblioteka - dve metode post i get -> salju post i get zahteve na adresu koju navedemo

web3 = Web3(HTTPProvider(BLOCKCHAIN_URL))


def create_and_initialize_account():
    # create account
    private_key = "0x" + secrets.token_hex(32)
    account = Account.from_key(private_key)
    address = account.address

    # send funds from account 0
    result = web3.eth.send_transaction({
        "from": web3.eth.accounts[0],
        "to": address,
        "value": web3.to_wei(2, "ether"),
        "gasPrice": 1
    })

    return (address, private_key)


def send_transaction(transaction, private_key):
    signed_transaction = web3.eth.account.sign_transaction(
        transaction, private_key)
    transaction_hash = web3.eth.send_raw_transaction(
        signed_transaction.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    return receipt


# primer slanja post zahteva
# rezultat je ono sto smo vratili od servera - opet pozivamo json (dekodovanje)

# Ova skripta: dohvata id paketa, dodaje kurira, dohvata id kurira, inic. racune kurira i kupca
# dodeljuje kuriru odredjeni paket, trazimo da se kreira transakcija koja predstavlja uplatu
# i nakon toga kreiramo trans. koja predstavlja potrebu i onda se ona izvrsava

# Pored ovoga - opcija zaglavlja moze isto (jwt token)
# Moze doci JWT tokene da ubacujemo

# dodati kurira (biciklistu)
result = requests.post(
    url=OWNER_URL + "/add_courier",
    json={
        "email": "stefan9@gmail.com",
        "forename": "Stefan",
        "surname": "Despot",
        "type": 0,
        "password": "123"
    }
)

courier_id = result.json()["id"]

# print("OK")

# ulogovati se
try:
    result = requests.post(
        url=COURIER_URL + "/login",
        json={
            "email": "stefan9@gmail.com",
            "password": "123"
        }
    )
except Exception as err:
    print(err)

print("OK2")

access_token = result.json()["access_token"]

print(access_token)

# dodati dva paketa
result = requests.post(
    url=OWNER_URL + "/add_package",
    json={
        "description": "Package0",
        "delivery_price": 100
    }
)

package1_id = result.json()["id"]

print(package1_id)

result = requests.post(
    url=OWNER_URL + "/add_package",
    json={
        "description": "Package1",
        "delivery_price": 300
    }
)

package2_id = result.json()["id"]

print(package2_id)


courier_address, courier_private_key = create_and_initialize_account()
customer_address, customer_private_key = create_and_initialize_account()

# svaki kontejner - ovu metodu jednom
# moraju imati ISTU ADRESU, PRIVATNI KLJUC VLASNIKA
# ovo se radi -> prilikom json fajla -> owner_account.json
# ovo se prekopira u root svakog kontejnera, kao i abi i bin pametnog ugovora

# kada pokrecemo vise servisa pomocu yaml fajla -> svi su obojeni nekom bojom (neka greska itd)

# preuzimanje paketa
headers = {
    "Authorization": f"Bearer {access_token}"
}

result = requests.post(
    url=COURIER_URL + "/take_package",
    json={
        "courier_id": courier_id,
        "package_id": package1_id,
        "courier_address": courier_address,
        "customer_address": customer_address
    },
    headers=headers
)

print(result)

# stanje kurira pre dostave
courier_balance = web3.eth.get_balance(courier_address)
print(f"COURIER BALANCE: {courier_balance}")

print(result.json())
delivery_id = result.json()["id"]

result = requests.get(
    url=CUSTOMER_URL + f"/create_pay_invoice/{delivery_id}/{customer_address}"
)
transaction = result.json()["transaction"]

send_transaction(transaction, customer_private_key)

result = requests.get(
    url=CUSTOMER_URL +
    f"/create_confirm_delivery_invoice/{delivery_id}/{customer_address}"
)

transaction = result.json()["transaction"]

send_transaction(transaction, customer_private_key)

# stanje nakon dostave
courier_balance = web3.eth.get_balance(courier_address)
print(f"COURIER BALANCE: {courier_balance}")

# pregled kurira
result = requests.get(
    url=OWNER_URL + "/get_couriers"
)
print(result.json())

# obrisati napravljenog kurira
result = requests.get(
    url=OWNER_URL + "/remove_courier",
    params={
        "id": courier_id
    }
)

# ponovni pregled kurira
result = requests.get(
    url=OWNER_URL + "/get_couriers"
)
print(result.json())

# obrada greske
try:
    result = requests.post(
        url=COURIER_URL + "/take_package",
        json={
            "courier_id": courier_id,
            "package_id": package2_id,
            "courier_address": courier_address,
            "customer_address": customer_address
        },
        headers=headers
    )
except Exception as err:
    print(err)
