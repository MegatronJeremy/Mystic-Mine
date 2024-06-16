FROM python:3

COPY configuration.py /configuration.py
COPY models.py /models.py
COPY utilities.py /utilities.py
COPY requirements.txt /requirements.txt
COPY owner_account.json /owner_account.json
COPY output/Delivery.abi /output/Delivery.abi
COPY output/Delivery.bin /output/Delivery.bin
COPY courier.py /courier.py

RUN pip install -r ./requirements.txt

ENTRYPOINT [ "python", "courier.py" ]