#!/bin/bash

echo "pong" | python3 ping_pong.py &
echo "ping" | python3 ping_pong.py &

sleep 10


