# frod-project

## Creating virtual environment
```
python -m venv venv && \
source venv/Scripts/activate && \
pip install -r requirements.txt
```

## Docker

```
docker compose up -d
```

## Debezium 
show connectors
```
curl -H "Accept:application/json" localhost:8083/connectors/
```
send message to Kafka API to register connector
```
curl -X POST http://localhost:8083/connectors   -H "Content-Type: application/json"   -d @configs/pg_connector.json
```
