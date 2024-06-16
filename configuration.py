import os

# vlasnik servisa
# kuriri
# ljudi koji koriste taj servis
# dostava paketa kupcu kome pripada taj paket
# kako implementirati, realizovati, itd.
# Na ispitu se ocenjuje samo nadoknada koju cemo raditi nad ovim

from datetime import timedelta

# parametri za pristup bazi
DATABASE_USERNAME = os.environ["DATABASE_USERNAME"] if (
    "DATABASE_USERNAME" in os.environ) else "root"

DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"] if (
    "DATABASE_PASSWORD" in os.environ) else "root"

DATABASE_URL = os.environ["DATABASE_URL"] if (
    "DATABASE_URL" in os.environ) else "localhost:3307"

DATABASE_NAME = os.environ["DATABASE_NAME"] if (
    "DATABASE_NAME" in os.environ) else "courier_service_database"

# ip adresa cvora pomocu kojeg pristupamo celoj mrezi
BLOCKCHAIN_URL = os.environ["BLOCKCHAIN_URL"] if (
    "DATABASE_NAME" in os.environ) else "http://127.0.0.1:8545"


# postoje neke podrazumevano vrednosti
# na ispitu da brzo pokrenemo i proverimo da li radi


class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_URL}/{DATABASE_NAME}"

    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    REDIS_HOST = os.environ["REDIS_HOST"] if (
        "REDIS_HOST" in os.environ) else "localhost"
    REDIS_PORT = int(os.environ["REDIS_PORT"]) if (
        "REDIS_PORT" in os.environ) else 6379
    REDIS_CHANNEL = os.environ["REDIS_CHANNEL"] if (
        "REDIS_CHANNEL" in os.environ) else "channel"
    REDIS_BUFFER = os.environ["REDIS_BUFFER"] if (
        "REDIS_BUFFER" in os.environ) else "banned"
