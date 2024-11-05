FROM python:3.11

RUN apt-get -y update

WORKDIR /opt
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

CMD ["python", "main.py"]

