from kafka import KafkaProducer

from app.config import KAFKA_HOST, KAFKA_PORT

# Kafka Producer client
kafka_producer = KafkaProducer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}")
