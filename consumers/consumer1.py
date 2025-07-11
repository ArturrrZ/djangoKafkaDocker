from kafka import KafkaConsumer
import json
import time
import os
folder = '/django/newusers'
os.makedirs(folder, exist_ok=True)

while True:
    try:
        consumer = KafkaConsumer(
            "registration",
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id="my-group",
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        break
    except Exception as e:
        time.sleep(5)
try:
    print("Consumer is ready")
    for msg in consumer:
        print('New message: ', msg.value)
        user = msg.value.get('user')
        if not user:
            print("Skipped message without a user")
            continue
        email = msg.value['user']['email']
        joined = msg.value['user']['joined']
        file_path = os.path.join(folder, f'newUser_{email}.txt')
        with open(file_path, 'w') as file:
            file.write(f'Welcome {email}! You joined us at {joined}')
        print("Email has been sent")    
        consumer.commit()
except KeyboardInterrupt:
    print("Consumer stopped")
finally:
    consumer.close()
