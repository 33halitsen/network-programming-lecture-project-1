import threading
import os
from datetime import datetime

class ChatServer:
    def handle_client(self, client_socket):
        """
        Handle a chat session for a connected client.
        Determines roles and starts sending/receiving threads.
        """
        # Ensure log directory exists
        if not os.path.exists("server/chat_logs"):
            os.makedirs("server/chat_logs")

        # Open a log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join("server/chat_logs", f"chat_server_{timestamp}.txt")
        self.chat_log_file = open(log_path, "a", encoding="utf-8")

        # Receive initial data to determine remote role
        initial_data = client_socket.recv(1024).decode()
        role = "CLIENT"
        if "CHAT_ROLE:SERVER" in initial_data:
            role = "CLIENT"
        elif "CHAT_ROLE:CLIENT" in initial_data:
            role = "SERVER"

        # Set display name based on role
        if role == "SERVER":
            self.display_name = "Client"
        else:
            self.display_name = "Server"

        print(f"[CHAT SERVER] Remote selected role: {role}")
        print(f"[CHAT SERVER] You are chatting as '{self.display_name}'.")

        # Start separate threads for sending and receiving messages
        threading.Thread(target=self.receive_messages, args=(client_socket,), daemon=True).start()
        self.send_messages(client_socket)

        # Close the log file when session ends
        self.chat_log_file.close()

    def log_message(self, sender, message):
        """Append a message to the chat log file."""
        if self.chat_log_file:
            self.chat_log_file.write(f"{sender}: {message}\n")
            self.chat_log_file.flush()  

    def receive_messages(self, client_socket):
        """
        Continuously receive messages from the client.
        Exit when client disconnects or sends 'exit'.
        """
        while True:
            try:
                msg = client_socket.recv(1024).decode()
                if not msg or msg.lower() == "exit":
                    print(f"\n[{self._get_other_name()}] Remote left the chat.", flush=True)
                    self.log_message(self._get_other_name(), "Left the chat")
                    break
                print(f"\n{self._get_other_name()}: {msg}", flush=True)
                self.log_message(self._get_other_name(), msg)
            except Exception as e:
                print(f"[CHAT SERVER] Error receiving message: {e}", flush=True)
                break

    def send_messages(self, client_socket):
        """
        Continuously send messages to the client.
        Exit when user types 'exit'.
        """
        try:
            while True:
                msg = input(f"{self.display_name}: ")
                if msg.lower() == "exit":
                    client_socket.sendall(msg.encode())
                    self.log_message(self.display_name, "Left the chat")
                    break
                client_socket.sendall(msg.encode())
                self.log_message(self.display_name, msg)
        except Exception as e:
            print(f"[CHAT SERVER] Error sending message: {e}")
        finally:
            print("[CHAT SERVER] Chat session ended.")

    def _get_other_name(self):
        """
        Determine the label of the remote side.
        This reverses the local display name for proper chat labeling.
        """
        return "Client" if self.display_name == "Server" else "Server"