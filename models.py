from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


# DEO ISPITA - moze biti migracija
# postoji sql skripta da to ne moramo raditi na pocetku

# vezna tabela izmedju ove dve - kad neki kurir zapravo preuzme paket
class Delivery (database.Model):
    __tablename__ = "deliveries"

    # privremeni ugovor koji vezan za adresu
    id = database.Column(database.Integer, primary_key=True)
    contract_address = database.Column(database.String(64), nullable=True)

    # pamtimo pored ovoga i ove parametre koji su nam potrebni
    package_id = database.Column(
        database.Integer, database.ForeignKey("packages.id"), nullable=False)
    courier_id = database.Column(
        database.Integer, database.ForeignKey("couriers.id"), nullable=False)

    courier = database.relationship("Courier", back_populates="deliveries")
    package = database.relationship("Package", back_populates="delivery")

    def __init__(self, contract_address, package_id, courier_id):
        self.contract_address = contract_address
        self.package_id = package_id
        self.courier_id = courier_id

    def __repr__(self):
        return f"<Delivery id={self.id}, status={self.status}, contract_address={self.contract_address}, package_id={self.package_id}, courier_id={self.courier_id}>"


# kurir - mejl, ime i prezime
class Courier (database.Model):
    __tablename__ = "couriers"

    # kada dodajemo migracije -> bez ovoga nullable=False!
    # moze da se desi da imamo neke redove u tabeli -> ako je nullable false sta za one redove vec u bazi???
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(256), nullable=False, unique=True)
    forename = database.Column(database.String(256), nullable=False)
    surname = database.Column(database.String(256), nullable=False)
    type = database.Column(database.Integer)
    password = database.Column(database.String(256))

    # ZA MIGRACIJE - jedan fajl sa menadzerom (migrate.py -> bez one jedne dve linije iznad kreiranja migrate = ...)
    # komanda flask -app migrate:application db init -> pravljenje foldera sa migracijama
    # flask --app migrate:application db migrate -m "Added type column to couriers table."
    # flask -app migrate:application db upgrade -> sada ima ovaj tip koji moze biti null
    # PROMENA 1

    deliveries = database.relationship("Delivery", back_populates="courier")

    def __init__(self, email, forename, surname, type, password):
        self.email = email
        self.forename = forename
        self.surname = surname
        self.type = type
        self.password = password

    def __repr__(self):
        return f"<Courier id={self.id}, email={self.email} forename={self.forename} surname={self.surname} type={self.type}>"


# paket za dostavu
class Package (database.Model):
    __tablename__ = "packages"

    id = database.Column(database.Integer, primary_key=True)
    description = database.Column(database.String(256), nullable=False)
    delivery_price = database.Column(database.Integer, nullable=False)
    arrival_date = database.Column(database.DateTime, nullable=False)

    delivery = database.relationship("Delivery", back_populates="package")

    def __init__(self, description, delivery_price, arrival_date):
        self.description = description
        self.delivery_price = delivery_price
        self.arrival_date = arrival_date
