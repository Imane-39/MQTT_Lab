# python 3.11

import time
import math
import random
import threading
from paho.mqtt import client as mqtt_client


broker = "localhost"
port = 1883

zone = "living_room"
measurement = "temperature"

publish_interval = 1

# we initialiwe the 2 sensors
sensors = ["STM_1", "STM_2"]



def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"{client_id} connected")
        else:
            print("Connection failed")

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        client_id
    )
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

 # we used sine wave to simulate the temperature values
def generate_value(t, phase):
    return round(20 + 5 * math.sin(t + phase), 2)   # 't' is the time variable, 'phase' shifts the wave for each sensor

# This function runs in a loop to simulate a sensor
def sensor_loop(sensor_id, phase):
    topic = f"/{zone}/{measurement}/{sensor_id}"
    client_id = f"sensor-{sensor_id}-{random.randint(0,1000)}"

    client = connect_mqtt(client_id)
    client.loop_start()#Start MQTT network loop in a separate thread

    t = 0
    while True:
        value = generate_value(t, phase)#Generate a new simulated temperature
        #publish the value to MQTT
        client.publish(topic, value)
        print(f"{sensor_id} -> {topic}: {value}")
        # Wait before next reading
        time.sleep(publish_interval)
        #increment time for the sine wave
        t += 0.2 


def run():
     #we start a thread for each sensor
    threads = []

    for i, sensor_id in enumerate(sensors):
        thread = threading.Thread(
            target=sensor_loop,
            args=(sensor_id, i)
        )
        thread.start() #start the sensor loop in a separate thread
        threads.append(thread)
    #wait for all threads to finish but they never will in this infinite loop
    for t in threads:
        t.join()


if __name__ == "__main__":
    run()
