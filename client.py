import socket
import threading
import webbrowser
from datetime import datetime
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
def receive():    
    data = client.recv(4096).decode('utf-8')
    data = eval(data)
    print(''.join(data))
    while True:
        try:
            updates = client.recv(4096).decode('utf-8')
            updates = eval(updates)
            print("MODIFIED:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(''.join(updates))      
        except Exception as e:
            print("An error occurred", e)
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()



