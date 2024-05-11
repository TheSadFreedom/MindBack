FROM python:3.10

RUN mkdir code
WORKDIR code


ADD . /code/

RUN pip install -r requirements.txt

CMD gunicorn ai_store_back.wsgi:application -b 0.0.0.0:8000
