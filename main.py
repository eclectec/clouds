from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
from os import getenv
import redis
import requests
import logging
import json
import time

message_broker = getenv("BROKER", "kafka")
broker_port = getenv("PORT", "9093")
topic = getenv("TOPIC", "rumble")

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logging.error('Message delivery failed: {}'.format(err))
    else:
        logging.warning('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def create_kafka_topic():
    admin_client = AdminClient({'bootstrap.servers': f'''kafka:{broker_port}'''})
    new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1)]

    fs = admin_client.create_topics(new_topics)

    # Wait for each operation to finish.
    for r_topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(r_topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(r_topic, e))


def process_opensky(data):
    plot_list = []
    plots = data["states"]
    for plot in plots:
        plot_list.append(
            {
                "hex": plot[0],
                "category": plot[17],
                "lat": plot[6],
                "lon": plot[5],
                "gs": plot[9]
            }
        )
    
    return plot_list


def main():
    time.sleep(10)
    url = getenv("URL", None)

    if url:
        broker = None
        if(message_broker == "kafka"):
            create_kafka_topic()
            broker = Producer({'bootstrap.servers': f'''kafka:{broker_port}'''})
        else:
            broker = redis.Redis(host="redis", port=broker_port, db=0)

        while True:
            air_traffic = None
            try:
                if "adsb" in url:
                    api_key = '6bbc780e-8511-4c86-8619-fdc0ab800ab4'
                    headers = {'api-auth': api_key} 
                    data = requests.get(url, headers=headers)
                    json_data = json.loads(data.text)
                    air_traffic = json_data["ac"]
                else:
                    data = requests.get(url)
                    json_data = json.loads(data.text)
                    if "airplanes" in url:
                        air_traffic = json_data["ac"]
                    elif "opensky" in url:
                        air_traffic = process_opensky(json_data)
                    elif "opendata" in url:
                        air_traffic = json_data["aircraft"]
                    else:
                        air_traffic = [{
                            "message": "hello there"
                        }]

                if air_traffic:
                    for plot in air_traffic:
                        if(message_broker == "kafka"):
                            broker.produce(topic, json.dumps(plot), callback=delivery_report)
                        else:
                            broker.publish(topic, json.dumps(plot))
            except:
                print(f"""An error occurred processing request to {url}""") 
            
            time.sleep(10)

if __name__ == "__main__":
    main()
