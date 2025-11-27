from modules import EchoServer, ChatServer
import socket
import threading

class CentralServer:
    def __init__(self, host='0.0.0.0', port=5050):
        """
        Initialize the central server with a listening socket.
        Also initialize Echo and Chat sub-modules.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[MAIN] Server running on {self.host}:{self.port}")

        # Initialize individual modules for handling specific tasks
        self.echo_server = EchoServer()
        self.chat_server = ChatServer()

    def start(self):
        """
        Start accepting client connections indefinitely.
        Each client connection is handled in a separate thread.
        """
        print("[MAIN] Server ready to accept connections...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"[MAIN] Connected by {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        """
        Handle the initial client request to route it to the correct module.
        """
        try:
            data = client_socket.recv(1024).decode().strip()
            print(f"[MAIN] Received from client: {data}")

            if data.startswith("MODULE:ECHO"):
                # Route to EchoServer module
                self.echo_server.handle_client(client_socket, data)
            elif data.startswith("MODULE:CHAT"):
                # Route to ChatServer module
                self.chat_server.handle_client(client_socket)
            else:
                # Unknown module request
                client_socket.sendall("Unknown module request.".encode())
                client_socket.close()

        except Exception as e:
            # Handle unexpected errors gracefully
            client_socket.sendall(f"Error: {e}".encode())
            client_socket.close()


if __name__ == "__main__":
    # Start the central server on the default port
    server = CentralServer(port=5050)
    server.start()