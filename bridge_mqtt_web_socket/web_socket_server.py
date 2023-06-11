import asyncio
import websockets
import sys


log_file = open("log_server.txt", "a")
sys.stdout = log_file
sys.stderr = log_file

# WebSocket server configuration
websocket_host = "0.0.0.0"
websocket_port = 8765

# Store connected clients
connected_clients = set()

# WebSocket server handler
async def websocket_handler(websocket, path):
    # Add the client to the connected_clients set
    connected_clients.add(websocket)
    print("New client connected")

    try:
        while True:
            message = await websocket.recv()
            # Process the received message here
            print(f"Received message from client: {message}")

            for client in connected_clients:
                await client.send(message)

    except websockets.exceptions.ConnectionClosedError:
        # Handle the connection closed by the client
        print("Client disconnected")

    finally:
        # Remove the client from the connected_clients set
        connected_clients.remove(websocket)

# Start the WebSocket server
start_server = websockets.serve(websocket_handler, websocket_host, websocket_port)

try:
    print(f"WebSocket server started at ws://{websocket_host}:{websocket_port}")
# Run the event loop
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
finally:
    log_file.close()
