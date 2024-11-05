The clouds project is utilized to scrape data from api endpoints to simulate streaming

## Build
```
docker build -t cloud .
```

## Broker Options
The project can submit data to both kafka or redis topics. The broker is set in the docker compose environment variable for BROKER

For Kafka, clouds environment to the following:
```
    environment:
      BROKER: kafka
      PORT: 9093
      TOPIC: traffic
```
For Redis, set the following variables:
```
    environment:
      BROKER: redis
      PORT: 6379
      TOPIC: traffic
```
