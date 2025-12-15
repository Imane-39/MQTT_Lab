Start-Process -FilePath "python" -ArgumentList "machine_agent.py", "M1"
Start-Sleep -Milliseconds 300
Start-Process -FilePath "python" -ArgumentList "machine_agent.py", "M2"
Start-Sleep -Milliseconds 300
Start-Process -FilePath "python" -ArgumentList "machine_agent.py", "M3"
Start-Sleep -Milliseconds 500
Start-Process -FilePath "python" -ArgumentList "supervisor.py"
