FROM python:3.10-slim

RUN apt-get update && apt-get install -y python3-tk

WORKDIR /app

COPY requirements.txt /app/
COPY interface.py /app/

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# Define a variável de ambiente DISPLAY
ENV DISPLAY=:0

CMD ["python3", "interface.py"]

