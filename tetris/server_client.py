
import socket
import threading
import json
from time import sleep
import leaderboard

sock: socket.socket

def send(data, _sock=None):
    global sock
    if not _sock:
        _sock = sock
    # Converts the data to a json string before sending it.
    json_string = json.dumps(data) + "\n"

    _sock.sendall(json_string.encode('utf-8'))


def receive(socket, signal: bool):
    while signal:
        try:
            # Actually receives the data
            data = socket.recv(1024).decode('utf-8')
            print(f"Received data: {data}")
            # Converts the received data back into a .json file
            # updating the scoreboard.
            lines = data.split('\n')
            for line in lines:
                if line.strip():
                    try:
                        json_data = json.loads(line.strip())
                        print(f"Received .json file: {json_data}")
                        leaderboard.receive_new_top_scores(json_data)
                    
                    except json.JSONDecodeError:
                        print(f"Error decoding .json file: {line.strip()}")
        except:
            print("Client has disconnected from the server.")
            signal = False
            break

def initialise_server_connection(host, port):
    global sock

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("Connected to server")
    except:
        print("Could not make a connection to the server")
        sleep(2)
    
    receive_thread = threading.Thread(target=receive, args=(sock, True))
    receive_thread.start()

def end_server_connection():
    global sock
    sock.close()
    print("Connection to server ended\n")
