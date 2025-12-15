import random
from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883

#the topic to subscribe to
topic = "Hello"

#to generate a unique client id for the subscriber
client_id = f'subscribe-{random.randint(0, 100)}'

#Creating and connecting an MQTT subscriber client
def connect_mqtt() -> mqtt_client:
    #callback executed when the client connects to the broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    #we create MQTT client
    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        client_id
    )


    client.on_connect = on_connect

    #connect to the broker
    client.connect(broker, port)
    return client

#Subscribes to the topic and defines how incoming messages are handled
def subscribe(client: mqtt_client):
    #callback executed when a message is received
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    #subscribe to the topic
    client.subscribe(topic)

    client.on_message = on_message


def run():
    client = connect_mqtt()
    #subscribe to the topic
    subscribe(client)

    #start listening indefinitely for incoming messages
    client.loop_forever()


if __name__ == '__main__':
    run()
