FROM python:3.9-alpine3.17

RUN apk update

WORKDIR /home/app

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
