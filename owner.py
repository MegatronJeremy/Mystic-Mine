import os

import datetime

from flask import Flask
from flask import request
from flask import jsonify

from configuration import Configuration

from models import database
from models import Package
from models import Courier

from redis import Redis

application = Flask(__name__)
application.config.from_object(Configuration)

database.init_app(app=application)


# dodaje paket - iz tela zahteva

@application.route("/add_package", methods=["POST"])
def add_package():
    description = request.json["description"]
    delivery_price = int(request.json["delivery_price"])
    arrival_date = datetime.datetime.now()

    new_package = Package(
        description=description,
        delivery_price=delivery_price,
        arrival_date=arrival_date,
    )

    database.session.add(new_package)
    database.session.commit()

    return jsonify(id=new_package.id)


# dodaj kurira u ceo sistem
@application.route("/add_courier", methods=["POST"])
def add_courier():
    email = request.json["email"]
    forename = request.json["forename"]
    surname = request.json["surname"]
    type = int(request.json["type"])
    password = request.json["password"]

    new_courier = Courier(
        email=email,
        forename=forename,
        surname=surname,
        type=type,
        password=password
    )

    database.session.add(new_courier)
    database.session.commit()

    return jsonify(id=new_courier.id)


@application.route("/get_couriers", methods=["GET"])
def get_couriers():
    return [str(courier) for courier in Courier.query.all()]


redis_client = Redis(host=Configuration.REDIS_HOST, port=Configuration.REDIS_PORT, db=0)


def ban_username(username):
    redis_client.sadd('banned_usernames', username)
    print(f'Username "{username}" has been banned.')


@application.route("/remove_courier", methods=["GET"])
def remove_courier():
    id = request.args.get("id")

    user = Courier.query.filter(Courier.id == id).first()

    username = user.email

    database.session.delete(user)
    database.session.commit()

    ban_username(username)

    return "OK"

    # deo za pokretanje - imamo podrazumevani port i host


if (__name__ == "__main__"):
    PORT = os.environ["PORT"] if ("PORT" in os.environ) else "5000"
    HOST = "0.0.0.0" if ("PRODUCTION" in os.environ) else "localhost"

    application.run(debug=True, port=PORT, host=HOST)
