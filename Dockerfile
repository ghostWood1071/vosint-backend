FROM python:3.10

ADD requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir secrets

RUN ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f secrets/PRIVATE_KEY

RUN openssl rsa -in secrets/PRIVATE_KEY -pubout -outform PEM -out secrets/PUBLIC_KEY

CMD python main.py
