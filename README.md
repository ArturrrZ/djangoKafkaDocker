# Kafka-Django Example
This project demonstrates how to integrate Kafka with a Django backend using Docker. A separate Python consumer listens to user registration messages and creates a welcome file for each new user.

## 🔧 Stack
Kafka + Zookeeper (Confluent images)

Django (as Kafka producer)

Python KafkaConsumer (as a separate container)

Docker Compose (service orchestration)
