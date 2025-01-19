FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY main.py .
COPY run.sh .

RUN chmod +x run.sh
EXPOSE $APP_PORT

CMD ["./run.sh"]
