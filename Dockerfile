FROM python:3.10

ADD requirements.txt requirements.txt

<<<<<<< HEAD
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
=======
RUN pip install --no-cache-dir --upgrade -r requirements.txt
>>>>>>> f5b45a8ae22ca4151f47c7c5d1a9fa48ac8ff52a

RUN mkdir secrets

RUN ssh-keygen -t rsa -b 4096 -m PEM -E SHA512 -f secrets/PRIVATE_KEY

RUN openssl rsa -in secrets/PRIVATE_KEY -pubout -outform PEM -out secrets/PUBLIC_KEY

<<<<<<< HEAD
CMD python main.py
=======
EXPOSE 6082

COPY . .

CMD python3 main.py
>>>>>>> f5b45a8ae22ca4151f47c7c5d1a9fa48ac8ff52a
