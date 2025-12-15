import random
from paho.mqtt import client as mqtt_client

broker = "localhost"
port = 1883
#subscribe to all average topics from any sensor
topic = "/+/+/average"  
client_id = f"interface-{random.randint(0,1000)}"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Interface agent connected")
        else:
            print("Connection failed")

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        client_id
    )
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_message(client, userdata, msg):
    #extract zone and measurement from topic
    _, zone, measurement, _ = msg.topic.split("/")
    #get the average value
    value = msg.payload.decode()
     #display
    print(f"[{zone.upper()}] {measurement} average = {value}")


def run():
    client = connect_mqtt()
    #listen to all average messages
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()


if __name__ == "__main__":
    run()
