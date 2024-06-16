import os

from flask import Flask
from flask import jsonify

from models import database
from models import Package
from models import Delivery

from configuration import Configuration


import utilities

application = Flask(__name__)
application.config.from_object(Configuration)

database.init_app(application)


# kreira transakciju koja ce da izvrsi pay metodu ugovora
# ta transakcija se vraca kao povr. vrednost


# BTINO - Adminer opcija (database je server)
# brinski da ispraznimo bazu - selektujemo sve tebele - pritisnemo truncate (resetuje bazu) - rucno ovo ili svaki put novi kontejner
# ostalo ok sto se tice aplikacija - ne treba kontejner za ovo

@application.route("/create_pay_invoice/<int:delivery_id>/<customer_address>", methods=["GET"])
def create_pay_invoice(delivery_id, customer_address):
    delivery = Delivery.query.filter(Delivery.id == delivery_id).one()

    if (not delivery):
        return ("Invalid delivery id!", 400)

    package = Package.query.join(Package.delivery).filter(
        Delivery.id == delivery_id).one()

    web3 = utilities.get_web3()

    abi = utilities.read_file("./output/Delivery.abi")

    contract = web3.eth.contract(address=delivery.contract_address, abi=abi)

    transaction = contract.functions.pay().build_transaction({
        "from": customer_address,
        "value": package.delivery_price,
        "nonce": web3.eth.get_transaction_count(customer_address),
        "gasPrice": 1
    })

    return jsonify(transaction=transaction)


# ovde samo potvrda dostave
# ne bi trebali da dostavljamo privatni kljuc - pa vraca transakciju da ga kupac potpise i uradi sta treba
@application.route("/create_confirm_delivery_invoice/<int:delivery_id>/<customer_address>", methods=["GET"])
def create_confirm_delivery_invoice(delivery_id, customer_address):
    delivery = Delivery.query.filter(Delivery.id == delivery_id).one()

    if (not delivery):
        return ("Invalid delivery id!", 400)

    abi = utilities.read_file("./output/Delivery.abi")

    web3 = utilities.get_web3()

    contract = web3.eth.contract(address=delivery.contract_address, abi=abi)

    # i to bi bilo to - npr. jedna stavka
    # pored toga - doraditi scenarijo
    # predajemo - ceo projekat bez venv
    # poene - iskljucivo na promenama
    transaction = contract.functions.confirm_delivery(delivery.courier.type).build_transaction({
        "from": customer_address,
        "nonce": web3.eth.get_transaction_count(customer_address),
        "gasPrice": 1
    })

    return jsonify(transaction=transaction)


if (__name__ == "__main__"):
    PORT = os.environ["PORT"] if ("PORT" in os.environ) else "5000"
    HOST = "0.0.0.0" if ("PRODUCTION" in os.environ) else "localhost"

    application.run(debug=True, port=PORT, host=HOST)
