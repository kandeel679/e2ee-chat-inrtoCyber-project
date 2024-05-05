import socket
import threading

def sending_messages(sock):
    while True:
        message = input("")
        sock.send(message.encode())
        print("You: " + message)

def receiving_messages(sock):
    while True:
        print("Partner: " + sock.recv(1024).decode())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.6", 9999))
    server.listen()

    client, _ = server.accept()
    print("Connected to client")

    threading.Thread(target=sending_messages, args=(client,)).start()
    threading.Thread(target=receiving_messages, args=(client,)).start()

def start_client():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("192.168.1.6", 9999))
    print("Connected to server")

    threading.Thread(target=sending_messages, args=(server,)).start()
    threading.Thread(target=receiving_messages, args=(server,)).start()

choice = input("Enter 1 to host or 2 to connect: ")

if choice == "1":
    start_server()
elif choice == "2":
    start_client()
else:
    print("Invalid choice")
