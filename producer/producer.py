# import logging
# logging.basicConfig(level=logging.INFO)

from kafka import KafkaProducer
from faker import Faker
from generate_data import generate_registration_data
import time
import json
import random

# Initialize Faker and KafkaProducer
fake = Faker()
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    api_version=(3, 8, 0),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Serializar a mensagem para JSON
    key_serializer=lambda k: k.encode('utf-8') # Serializar a mensagem para JSON
)

if __name__ == '__main__':
    topic = 'registration_topic'
    
    while True:
        data = generate_registration_data()
        key = data['id_matricula']  # Use the 'id_matricula' as the key
        print(data)
        producer.send(topic, key=key, value=data)  # Send both key and value
        time.sleep(1)  # Send a message every second