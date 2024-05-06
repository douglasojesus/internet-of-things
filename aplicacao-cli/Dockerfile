FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
COPY cli.py /app/

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "cli.py"]

