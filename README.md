# MQTT Lab – Multi-Agent Systems

## Overview

This repository contains the implementation of an **MQTT based multi-agent system**.

The lab explores the **publish/subscribe paradigm** using MQTT and progressively builds more advanced distributed systems:

- Basic MQTT communication  
- Bidirectional client interaction (Ping–Pong)  
- Sensor network with data aggregation  
- Anomaly detection and recovery  
- Contract Net Protocol for decentralized job allocation  


---

## Technologies

- **Language:** Python  
- **MQTT Library:** Eclipse Paho MQTT  
- **Broker:** shiftr.io (local broker)  
- **OS:** Windows  
- **Automation:** PowerShell

---

##  Repository Structure

```text
.
├── 2 client/
│   ├── client_publish.py
│   └── client_subscribe.py
│
├── Ping pong/
│   ├── ping_pong.py
│   └── run_ping_pong.ps1
│
│
├── SensorNetwork/
│   ├── sensor.py
│   ├── average.py
│   ├── interface.py
│   └── run_all.ps1
│
├── Anomaly detection/
│   ├── sensor.py
│   ├── average.py
│   ├── detection_agent.py
│   ├── identification_agent.py
│   ├── interface.py
│   └── run_all.ps1
│
├── Contract Net/
│   ├── machine_agent.py
│   ├── supervisor.py
│   └── run_all.ps1
│
└── MQTT_Lab_report.pdf
```

##  Getting Started

###  Requirements

- Python 3.x  
- MQTT Broker (shiftr.io or equivalent)

### Install dependencies

```bash
pip install paho-mqtt
```
##  Experiments

## I. MQTT Basics

### 🔹 First Contact

- Simple publisher/subscriber communication  
- Periodic message publication on a topic (`Hello`)  
- Validation of broker connectivity and subscriptions  

### 🔹 Two Clients Interaction (Ping–Pong)

- Two clients exchanging messages on `ping` and `pong` topics  
- Each client acts as both publisher and subscriber  
- Automated startup using scripts  

---

## II. Sensor Network

### 🔹 Sensor Agents

- Simulate temperature sensors in a `living_room` zone  
- Publish sinusoidal measurements  
- Topic format:
/living_room/temperature/{sensor_id}

### 🔹 Averaging Agent

- Subscribes using wildcards:
```text
/living_room/temperature/+
```
- Computes and publishes average values:
```text
/living_room/temperature/average
```
### 🔹 Interface Agent

- Displays aggregated values  
- Subscribes to:
```text
/+/+/average
```
---

## III. Anomaly Detection

### 🔹 Detection Agent

- Monitors sensor readings in real time  
- Detects anomalies using mean ± 2× standard deviation  
- Publishes alerts on:
```text
/living_room/temperature/alert
```
### 🔹 Identification Agent

- Subscribes to alert topic  
- Sends reset commands to faulty sensors:
```text
/{sensor_id}/reset
```

### 🔹 Sensor Recovery

- Sensors listen to reset topics  
- Internal state is reinitialized upon reset  

---

## IV. Contract Net Protocol

### 🔹 Machine Agents

- Autonomous agents with job capabilities and execution times  
- Respond to CFP messages:
```text
/cnp/cfp
```
- Send bids on:
```text
/cnp/bid/{machine_id}
```
- Receive assignments on:
```text
/cnp/assign/{machine_id}
```
### 🔹 Supervisor Agent

- Generates jobs  
- Collects bids using wildcard subscriptions  
- Selects the fastest machine  
- Assigns jobs using targeted messages  

- Machines execute only one job at a time  
- Fully decentralized coordination  

---

##  Observations  
- Wildcards are important for dynamic agent discovery  
- The Contract Net Protocol is effectively implemented using asynchronous messaging  

---

##  Report

A detailed report including architecture explanations, execution logs, and design decisions is available in:

```text
MQTT_Lab_report.pdf
```
## Authors
- BENABDALLAH Redouane
- AL ABOUDI Imane
