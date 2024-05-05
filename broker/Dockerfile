FROM python:3.10-slim

COPY requirements.txt /app/
COPY initialize.py /app/

WORKDIR /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-u", "initialize.py"]
