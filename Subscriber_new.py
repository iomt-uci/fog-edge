import redis

host_name = "127.0.0.1"

subscriber = redis.Redis(host = host_name, port = 6379)

s = subscriber.pubsub()
s.subscribe("heart-rate")

while True:
    message = s.get_message()
    if message and message['data'] != 1:
        message = message['data'].decode('utf-8')
        print(message)

