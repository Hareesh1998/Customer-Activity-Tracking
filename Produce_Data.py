from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

events = ["click", "view"]
for _ in range(1000):
    message = {
        "user_id": random.randint(1, 50),
        "timestamp": time.time(),
        "event_type": random.choice(events),
        "product_id": random.randint(100, 110),
        "device_type": random.choice(["web", "mobile"])
    }
    producer.send("user_activity", value=message)
    time.sleep(0.5)
