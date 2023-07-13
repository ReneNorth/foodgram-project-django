FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt --no-cache-dir

COPY foodgram/ .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:9000" ] 