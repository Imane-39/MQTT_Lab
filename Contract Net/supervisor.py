import json
import time
import random
from paho.mqtt import client as mqtt_client

broker = "localhost"
port = 1883

client_id = f"supervisor-{random.randint(0,1000)}"
deadline = 3  #seconds to wait for bids
bids = {} #so we store bids from machines

#list of jobs to assign
jobs = [
    {"job_id": "JOB_1", "job_type": "drilling"},
    {"job_id": "JOB_2", "job_type": "painting"},
    {"job_id": "JOB_3", "job_type": "cutting"}
]

def connect():
    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1,
        client_id
    )
    client.connect(broker, port)
    return client

#handle bid messages from machines
def on_bid(client, userdata, msg):
    machine_id = msg.topic.split("/")[-1]
    data = json.loads(msg.payload.decode())
    job_id = data["job_id"]

    if "time" in data:
        bids[machine_id] = data["time"] # store bid
        print(f"[SUP] BID from {machine_id}: {data['time']}s")
    else:
        print(f"[SUP] REJECT from {machine_id}") # machine cannot do job


def run():
    client = connect()
    client.subscribe("/cnp/bid/+")#listen to all bids
    client.on_message = on_bid
    client.loop_start() #start network loop

    for job in jobs:
        print(f"\n[SUP] CFP {job}") #announce new job
        bids.clear()
        client.publish("/cnp/cfp", json.dumps(job))# send CFP

        time.sleep(deadline)# wait for bids

        if not bids:
            print("[SUP] No valid bids")
            continue

        #choose machine with shortest time
        winner = min(bids, key=bids.get)
        print(f"[SUP] ACCEPT {winner}")

        #assign job to winning machine
        assign_msg = {
            "job_id": job["job_id"],
            "time": bids[winner]
        }
        client.publish(f"/cnp/assign/{winner}", json.dumps(assign_msg))
        time.sleep(1)

    client.loop_forever()


if __name__ == "__main__":
    run()
