import os
import time

from flask import Flask
from flask import request
from flask import jsonify
from redis import Redis

from models import database
from models import Package
from models import Delivery
from models import Courier

from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

from configuration import Configuration

import utilities

application = Flask(__name__)
application.config.from_object(Configuration)

database.init_app(application)

# jedna funkcionalnost - preuzme neki paket, id paketa, id kurira, adrese kurira i kupca

# nadoknada: dva tipa kurira, jedni sa vozilom -> njima po potvrdi dostave dajem vise novca (naknada za gorvi), ali
# i oni meni poboljsavaju kvalitet usluge

# ideja: samo promeniti tip kurira (dodati polje)


jwt = JWTManager(application)


@application.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = Courier.query.filter(Courier.email == email,
                                Courier.password == password).first()
    if not user:
        return "User not found", 401

    access_token = create_access_token(identity=user.email)

    return jsonify(access_token=access_token)


redis_client = Redis(host=Configuration.REDIS_HOST, port=Configuration.REDIS_PORT, db=0)


def is_username_banned(username):
    print(username)
    return redis_client.sismember('banned_usernames', username)


def banned_check(function):
    @jwt_required()
    def wrapper(*args, **kwargs):
        username = get_jwt_identity()
        if not is_username_banned(username):
            print("OK")
            return function(*args, **kwargs)
        else:
            return "Invalid token"

    return wrapper


@application.route("/check", endpoint="check_route")
@banned_check
def check():
    identity = get_jwt_identity()
    claims = get_jwt()

    return f"IDENTITY: {identity}, CLAIMS: {claims}"


@application.route("/take_package", methods=["POST"], endpoint="take_package_route")
@banned_check
def take_package():
    courier_id = request.json.get("courier_id", 0)
    package_id = request.json.get("package_id", 0)
    courier_address = request.json.get("courier_address", 0)
    customer_address = request.json.get("customer_address", 0)

    # mora proveriti da li paket postoji
    package = Package.query.filter(Package.id == package_id).one()
    if not package:
        return "Invalid package id!", 400

    abi = utilities.read_file("./output/Delivery.abi")
    bytecode = utilities.read_file("./output/Delivery.bin")

    web3 = utilities.get_web3()

    contract = web3.eth.contract(bytecode=bytecode, abi=abi)

    owner_address = utilities.get_owner_account()[0]

    # napravi transakciju ugovora
    # nije trebao da se pravi novi ugovor - ali ovako najjednostavnije
    create_contract_transaction = contract.constructor(owner_address, courier_address, customer_address,
                                                       package.delivery_price).build_transaction({
        "from": owner_address,
        "nonce": web3.eth.get_transaction_count(owner_address),
        "gasPrice": 1
    })

    owner_private_key = utilities.get_owner_account()[1]

    receipt = utilities.send_transaction(
        create_contract_transaction, owner_private_key)

    contract_address = receipt["contractAddress"]

    new_delivery = Delivery(
        contract_address=contract_address,
        courier_id=courier_id,
        package_id=package_id
    )

    database.session.add(new_delivery)
    database.session.commit()

    # povr. vrednost - id nove dostave
    return jsonify(id=new_delivery.id)


if __name__ == "__main__":
    PORT = os.environ["PORT"] if ("PORT" in os.environ) else "5000"
    HOST = "0.0.0.0" if ("PRODUCTION" in os.environ) else "localhost"

    application.run(debug=True, port=PORT, host=HOST)
