# python 3.11
import random
from paho.mqtt import client as mqtt_client

broker = "localhost"
port = 1883

zone = "living_room"
#topic where alerts from the detection agent will be received
alert_topic = f"/{zone}/temperature/alert"

client_id = f"id-agent-{random.randint(0,1000)}"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Identification agent connected")
        else:
            print("Connection failed")
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
#callback when an alert message is received
def on_message(client, userdata, msg):
    alert_msg = msg.payload.decode()
    print(f"Received alert: {alert_msg}")

    #extract suspected sensors from the alert
    if "sensors" in alert_msg or "sensors" in alert_msg.lower():
        import ast
        suspects = ast.literal_eval(alert_msg.split("sensors")[-1].strip())
        #send a reset message to each suspicious sensor
        for sensor_id in suspects:
            reset_topic = f"/{sensor_id}/reset"
            client.publish(reset_topic, "RESET")
            print(f"Sent reset to {sensor_id}")

def run():
    client = connect_mqtt()
    client.subscribe(alert_topic)
    client.on_message = on_message
    client.loop_forever()

if __name__ == "__main__":
    run()
