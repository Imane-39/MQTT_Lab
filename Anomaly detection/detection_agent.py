# python 3.11
import statistics
import random
from paho.mqtt import client as mqtt_client

broker = "localhost"
port = 1883

zone = "living_room"
measurement = "temperature"
#subscribe to all sensor readings
subscribe_topic = f"/{zone}/{measurement}/+"
#topic to publish alerts when anomalies are detected
alert_topic = f"/{zone}/{measurement}/alert"

client_id = f"detection-{random.randint(0,1000)}"
values = {}  # clé: sensor_id, valeur: liste de lectures

STD_THRESHOLD = 2  #number of standard deviations to detect anomalies

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Detection agent connected")
        else:
            print("Connection failed")

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
#callback when a sensor message is received
def on_message(client, userdata, msg):
    global values

    #extract sensor ID from topic
    sensor_id = msg.topic.split("/")[-1]
    value = float(msg.payload.decode())

    if sensor_id not in values:
        values[sensor_id] = []
    #store value
    values[sensor_id].append(value)

    #we check if we have enough data to compute standard deviation
    all_readings = [v for lst in values.values() for v in lst]
    if len(all_readings) >= 4:
        mean = statistics.mean(all_readings)
        std = statistics.stdev(all_readings)

        #detect suspicious sensors
        suspects = [sid for sid, lst in values.items() if any(abs(v-mean) > STD_THRESHOLD*std for v in lst)]
        if suspects:
            alert_msg = f"ALERT: suspicious sensors {suspects}"
            client.publish(alert_topic, alert_msg)
            print(alert_msg)

            #and we clear readings for suspicious sensors after alert
            for sid in suspects:
                values[sid] = []

def run():
    client = connect_mqtt()
    client.subscribe(subscribe_topic)
    client.on_message = on_message
    client.loop_forever()

if __name__ == "__main__":
    run()
