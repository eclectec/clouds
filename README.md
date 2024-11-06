The clouds project is utilized to scrape data from api endpoints to simulate streaming

## Build
```
docker build -t cloud .
```

## Run
To run puddle with cloud stream source and a broker
```
docker compose up -d

## Broker Options
The project can submit data to both kafka or redis topics. The broker is set in the docker compose environment variable for BROKER

For Kafka, set cloud && puddle environment to the following in docker-compose.yml:
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
