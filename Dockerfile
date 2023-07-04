FROM python:3.10

ADD requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir secrets

RUN ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f secrets/PRIVATE_KEY

RUN openssl rsa -in secrets/PRIVATE_KEY -pubout -outform PEM -out secrets/PUBLIC_KEY

EXPOSE 6082

COPY . .

CMD python3 main.py