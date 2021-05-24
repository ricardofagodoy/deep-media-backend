# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

RUN pip install gunicorn

# copy project
COPY src/ /usr/src/app/

CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:app"]