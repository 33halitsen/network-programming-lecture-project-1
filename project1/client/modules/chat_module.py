import socket
import threading
import os
from .sntp_client import SNTPClient

class ChatClient:
    def __init__(self, client_socket):
        # Initialize client socket and default role
        self.client_socket = client_socket
        self.chat_log_file = None
        self.role = "CLIENT"  
        self.display_name = "Client"

    def start(self):
        """
        Start the chat session:
        - Create log file with timestamp
        - Let the user choose role (Server or Client mode)
        - Notify server of module and role
        - Start threads for sending and receiving messages
        """
        print("[CHAT CLIENT] Chat session started. Type 'exit' to quit.")
        try:
            # Create chat logs directory if it does not exist
            os.makedirs("client/chat_logs", exist_ok=True)

            # Create log file using SNTP timestamp
            sntp = SNTPClient()
            timestamp = sntp.get_time_str()
            log_path = os.path.join("client/chat_logs", f"chat_{timestamp}.txt")
            self.chat_log_file = open(log_path, "a", encoding="utf-8")

            # Let user select chat role
            self.choose_role()

            # Send module and role information to the server
            self.client_socket.sendall("MODULE:CHAT".encode())
            self.client_socket.sendall(f"CHAT_ROLE:{self.role}".encode())

            # Start threads for receiving and sending messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.send_messages()

        except Exception as e:
            print(f"Client Error: {e}")

    def choose_role(self):
        """
        Let the user select chat role:
        - Server Mode (act as Server)
        - Client Mode (act as Client)
        """
        print("\n=== CHAT ROLE SELECTION ===")
        print("1. Server Mode (Act like Server)")
        print("2. Client Mode (Act like Client)")
        choice = input("Select mode: ")
        if choice == "1":
            self.role = "SERVER"
            self.display_name = "Server"
        else:
            self.role = "CLIENT"
            self.display_name = "Client"
        print(f"Chat role set to: {self.display_name}\n")

    def log_message(self, sender, message):
        """Write a message to the chat log file if logging is enabled."""
        if self.chat_log_file:
            self.chat_log_file.write(f"{sender}: {message}\n")
            self.chat_log_file.flush()

    def receive_messages(self):
        """
        Continuously listen for incoming messages from the server.
        Log messages and display them with appropriate role labels.
        """
        while True:
            try:
                msg = self.client_socket.recv(1024).decode()
                if not msg or msg.lower() == "exit":
                    print(f"\n[{self._get_other_name()}] Remote left the chat.", flush=True)
                    self.log_message(self._get_other_name(), "Left the chat")
                    break
                print(f"\n{self._get_other_name()}: {msg}", flush=True)
                self.log_message(self._get_other_name(), msg)
            except Exception as e:
                print(f"[CHAT CLIENT] Error receiving message: {e}", flush=True)
                break

    def send_messages(self):
        """
        Continuously read user input and send messages to the server.
        Log messages locally.
        """
        try:
            while True:
                msg = input(f"{self.display_name}: ")
                if msg.lower() == "exit":
                    self.client_socket.sendall(msg.encode())
                    self.log_message(self.display_name, "Left the chat")
                    break
                self.client_socket.sendall(msg.encode())
                self.log_message(self.display_name, msg)
        except Exception as e:
            print(f"[CHAT CLIENT] Error sending message: {e}")

    def _get_other_name(self):
        """Return the display name of the remote participant based on local role."""
        return "Client" if self.display_name == "Server" else "Server"