import random
import time
from paho.mqtt import client as mqtt_client

# MQTT broker configuration
broker = 'localhost'
port = 1883

#topic initialization 
topic = "Hello"

#to generate a unique client id for the publisher
client_id = f'publish-{random.randint(0, 1000)}'

#creates and connects an MQTT client to the broker
def connect_mqtt():
    #callback executed when the client connects to the broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    #create MQTT client using Paho
    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        client_id
    )

    #to assign the connection to the callback
    client.on_connect = on_connect

    #connect to the broker
    client.connect(broker, port)
    return client

#publishes messages periodically to the MQTT topic
def publish(client):
    msg_count = 1

    while True:
        
        time.sleep(1)

        # Message payload
        msg = f"Hi: {msg_count}"

        #publish message to the topic
        result = client.publish(topic, msg)

        #result[0] indicates success 0 or failure not 0
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic `{topic}`")

        msg_count += 1

        #Stop after sending 3 messages
        if msg_count > 3:
            break

#Main execution function
def run():
    client = connect_mqtt()

    #Start network loop in a separate thread
    client.loop_start()

    #Publish messages
    publish(client)

    #Stop the network loop
    client.loop_stop()


if __name__ == '__main__':
    run()
