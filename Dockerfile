FROM python:3.7.3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /usr/src/app
ENV FLASK_ENV=development
CMD flask run --host=0.0.0.0