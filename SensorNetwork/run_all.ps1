# start the first sensor
Start-Process -FilePath "python" -ArgumentList "sensor.py", "STM_1"
Start-Sleep -Milliseconds 500  # wait a bit before starting the next sensor

# start the second sensor
Start-Process -FilePath "python" -ArgumentList "sensor.py", "STM_2"
Start-Sleep -Milliseconds 500  # small delay to avoid startup conflicts

# start the averaging agent
Start-Process -FilePath "python" -ArgumentList "average.py"
Start-Sleep -Milliseconds 500  # give it time to connect

# start the interface agent
Start-Process -FilePath "python" -ArgumentList "interface.py"
