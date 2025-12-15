# python 3.11
import json
import time
import random
from paho.mqtt import client as mqtt_client

broker = "localhost"
port = 1883

machine_id = None
#indicate if machine is currently busy
busy = False

#jobs this machine can do
JOB_CAPABILITIES = {
    "drilling": random.randint(3, 6),
    "painting": random.randint(5, 9)
}

def connect():
    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        f"machine-{machine_id}"
    )
    client.connect(broker, port)
    return client

#handle CFP messages
def on_cfp(client, userdata, msg):
    global busy
    if busy:
        return #ignore if busy

    data = json.loads(msg.payload.decode())
    job_id = data["job_id"]
    job_type = data["job_type"]

    topic = f"/cnp/bid/{machine_id}"

    if job_type in JOB_CAPABILITIES:
        time_needed = JOB_CAPABILITIES[job_type]
        response = {
            "job_id": job_id,
            "time": time_needed
        }
        print(f"[{machine_id}] PROPOSAL {job_id} -> {time_needed}s")
    else:
        response = {
            "job_id": job_id,
            "reason": "cannot_do"
        }
        print(f"[{machine_id}] REJECT {job_id}")

    client.publish(topic, json.dumps(response))

#handle assignment messages
def on_assign(client, userdata, msg):
    global busy
    data = json.loads(msg.payload.decode())
    job_id = data["job_id"]
    duration = data["time"]

    busy = True
    print(f"[{machine_id}] START {job_id} ({duration}s)")
    time.sleep(duration)
    busy = False
    print(f"[{machine_id}] DONE {job_id}")


def run(mid):
    global machine_id
    machine_id = mid

    client = connect()
    #subscribe to CFP and assignment topics
    client.subscribe("/cnp/cfp")
    client.subscribe(f"/cnp/assign/{machine_id}")
    client.message_callback_add("/cnp/cfp", on_cfp)
    client.message_callback_add(f"/cnp/assign/{machine_id}", on_assign)

    client.loop_forever()


if __name__ == "__main__":
    import sys
    run(sys.argv[1])
