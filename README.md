The clouds project is utilized to scrape data from api endpoints to simulate streaming

## Build
```
docker build -t cloud .
```

## Broker Options
The project can submit data to both kafka or redis topics. The broker is set in the docker compose environment variable for BROKER
