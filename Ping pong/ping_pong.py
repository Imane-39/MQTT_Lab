import random
import time
from paho.mqtt import client as mqtt_client
#global variable to store received messages
msg = ""  
broker = 'localhost'  
port = 1883 

#we used two topics
topic_pong = "pong"  
topic_ping = "ping"  

client_id = f'publish-{random.randint(0, 1000)}'

#function to connect to the MQTT broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Create an MQTT client instance with the specified callback API version
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect  # we assign the connection callback
    client.connect(broker, port)    #Connect to the broker
    return client


def publish(client, topic):
    result = client.publish(topic, topic)  # Send the topic name as the message
    status = result[0]  # Check the result status
    if status == 0:
        print(f"Send `{topic}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client, topic):
    def on_message(c, u, message):
        #Callback when a message is received
        global msg
        msg = message.payload.decode()  #Decode the message payload
        print(f"Received `{msg}` from `{message.topic}` topic")

    client.subscribe(topic)      #Subscribe to the given topic
    client.on_message = on_message  


def run():
    global msg

    #we ask the user which role this client will take
    print("ping or pong ?:")  
    first = input().strip() 

    #Connect to the MQTT broker
    client1 = connect_mqtt() 
    #Start the network loop in a separate thread 
    client1.loop_start()       

    if first == "ping":
        subscribe(client1, topic_pong)  # Listen for pong messages
        publish(client1, topic_ping)    # Send the first ping

        while True:
            time.sleep(5)  # Wait before checking for responses
            if msg == "pong":  # If pong is received
                msg = ""       # Reset the message variable
                publish(client1, topic_ping)  # Send another ping

    else:  # pong role
        subscribe(client1, topic_ping)  # Listen for ping messages

        while True:
            time.sleep(1)  # Shorter delay to respond faster
            if msg == "ping":  # If ping is received
                msg = ""       # Reset the message variable
                publish(client1, topic_pong)  # Send a pong response


if __name__ == '__main__':
    run()  
