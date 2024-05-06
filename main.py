import socket
import threading
import rsa
import tkinter as tk

public_key, private_key = rsa.newkeys(1024)
public_partner = None
sock = None

def sending_messages():
    global sock, public_partner
    message = message_entry.get()
    if message:
        if public_partner is not None:
            encrypted_message = rsa.encrypt(message.encode(), public_partner)
            sock.send(encrypted_message)
            chat_text.insert(tk.END, "You: " + message + "\n", "sent")
            message_entry.delete(0, tk.END)
        else:
            chat_text.insert(tk.END, "Waiting for public key...\n", "system")
    else:
        chat_text.insert(tk.END, "Message cannot be empty!\n", "system")

def receiving_messages():
    global public_partner
    while True:
        encrypted_message = sock.recv(1024)
        if public_partner is not None:
            decrypted_message = rsa.decrypt(encrypted_message, private_key)
            chat_text.insert(tk.END, "Partner: " + decrypted_message.decode() + "\n", "received")
        else:
            received_public_key = rsa.PublicKey.load_pkcs1(encrypted_message)
            public_partner = received_public_key
            chat_text.insert(tk.END, "Public key received!\n", "system")

def start_server():
    global sock
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.6", 9997))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    sock = client

    threading.Thread(target=receiving_messages).start()
    chat_text.insert(tk.END, "Connected to client\n", "system")

def start_client():
    global sock, public_partner
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("192.168.1.6", 9997))
    server.send(public_key.save_pkcs1("PEM"))
    sock = server

    threading.Thread(target=receiving_messages).start()
    chat_text.insert(tk.END, "Connected to server\n", "system")

def handle_choice():
    choice = choice_var.get()
    if choice == "1":
        threading.Thread(target=start_server).start()
    elif choice == "2":
        threading.Thread(target=start_client).start()
    else:
        print("Invalid choice")

# GUI setup
root = tk.Tk()
root.title("E2EE Chat")
root.configure(bg="#e0e0e0")

choice_var = tk.StringVar()
choice_label = tk.Label(root, text="Choose Hosting or Connecting:", bg="#e0e0e0")
choice_label.pack()

host_radio = tk.Radiobutton(root, text="Host", variable=choice_var, value="1", bg="#e0e0e0")
host_radio.pack()

connect_radio = tk.Radiobutton(root, text="Connect", variable=choice_var, value="2", bg="#e0e0e0")
connect_radio.pack()

start_button = tk.Button(root, text="Start", command=handle_choice, bg="#4caf50", fg="white")
start_button.pack()

chat_text = tk.Text(root, width=50, height=20, bg="white", fg="black")
chat_text.pack()

message_entry = tk.Entry(root, width=50, bg="white", fg="black")
message_entry.pack()

send_button = tk.Button(root, text="Send", command=sending_messages, bg="#2196f3", fg="white")
send_button.pack()

# Define tags for text color
chat_text.tag_config("sent", foreground="#4caf50")
chat_text.tag_config("received", foreground="#2196f3")
chat_text.tag_config("system", foreground="#757575")

root.mainloop()
