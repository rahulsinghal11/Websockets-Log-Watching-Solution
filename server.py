import socket
import threading
import logging
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()

clients = []

fname = "/Users/rahul/Desktop/browserstack/log/test.log"
a_file = open(fname, "r")

def broadcast(message):
    for client in clients:
        client.send(message.encode(FORMAT))

# def lastLines():
#     bufsize = 8192
#     fsize = os.stat(fname).st_size

#     i = 0

#     with open(fname) as f:
#         p = f.tell()
#         if bufsize>fsize:
#             bufsize = fsize-1
#             fetched_lines = []

#             while True:
#                 i+=1
#                 try:
#                     f.seek(fsize-bufsize * i)
#                 except:
#                     broadcast(str(fetched_lines[-10:]))
#                     print(''.join(fetched_lines[-10:]))
#                     break
#                 fetched_lines.extend(f.readlines())

#                 if len(fetched_lines) >= 10 or f.tell() < 0:
#                         broadcast(str(fetched_lines[-10:]))
#                         print(''.join(fetched_lines[-10:]))
#                         break

class OnMyWatch:
    watchDirectory = "C:/Users/rahul/Desktop/browserstack/log"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def on_any_event(self, event):
        if event.is_directory:
            return None
        
        if event.event_type == 'modified':
            lines = a_file.readlines()
            last_lines = lines[-10:]
            last_lines = str(last_lines)
            print(last_lines)
            broadcast(last_lines)
            


def handle_client(client):    
    a_file = open(fname, "r")
    lines = a_file.readlines()
    last_lines = lines[-10:]
    last_lines = str(last_lines)
    client.send(last_lines.encode(FORMAT))
    while True:
        try:
            watch = OnMyWatch()
            watch.run()
        except:
            clients.remove(client)
            client.close()
            break


def start():    
    print("Listening on ", SERVER)
    while True:
        client, addr = server.accept()
        print("Connected with", addr)
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        print("[ACTIVE CONNECTIONS]", len(clients))


print("Server is starting...")
start()
