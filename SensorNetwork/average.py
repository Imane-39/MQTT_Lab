import statistics
import random 
from paho.mqtt import client as mqtt_client


broker = "localhost"
port = 1883

zone = "living_room"
measurement = "temperature"

#nbr of samples to calculate the average
window_size = 4

#subscribe to all sensors under zone/measurement
subscribe_topic = f"/{zone}/{measurement}/+"
#publish the computed average here
publish_topic = f"/{zone}/{measurement}/average"

client_id = f"avg-agent-{random.randint(0,1000)}"
#buffer to store incoming sensor values
values_buffer = []


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Averaging agent connected")  #connection successful
        else:
            print("Connection failed")          #connection failed

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        client_id
    )
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_message(client, userdata, msg):
    global values_buffer
    #convert incoming message to float
    value = float(msg.payload.decode())
    #convert incoming message to float  
    values_buffer.append(value)          
    print(f"Received {value} from {msg.topic}")

    #calculate average if we have enough samples
    if len(values_buffer) >= window_size:
        avg = statistics.mean(values_buffer[:window_size])
        values_buffer = values_buffer[window_size:]  # remove used samples
        client.publish(publish_topic, round(avg, 2))  # publish the average
        print(f"Published average -> {publish_topic}: {round(avg,2)}")


def run():
    client = connect_mqtt()
    #listen to all sensor topics
    client.subscribe(subscribe_topic) 
    client.on_message = on_message
    client.loop_forever()  #keep running indefinitely


if __name__ == "__main__":
    run()
