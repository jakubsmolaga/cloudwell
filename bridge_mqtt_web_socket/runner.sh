#!/bin/bash

# Start the primary process in the background
python /app/web_socket_server.py &

# Wait for 4 seconds
sleep 4

# Start the helper process
python /app/client.py

# Both processes are running concurrently after a 3-second delay

# Optionally, you can add a wait command to wait for the main process to finish
# wait

# The script will continue executing after both processes have finished
