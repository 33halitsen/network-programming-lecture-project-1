import socket
from .set_server_address import SetServerAddress

class EchoClient:
    def __init__(self, client_socket):
        # Store the client socket for communication
        self.client_socket = client_socket

    def start(self, message="Hello from client!"):
        """
        Start the echo test by sending a message to the server
        and verifying that the server responds with the same message.
        """
        try:
            # Prepare a module request indicating this is the Echo Test
            module_request = f"MODULE:ECHO;DATA={message}"
            self.client_socket.sendall(module_request.encode())
            print(f"Sent: {message}")  # Display the sent message

            # Receive the echoed response from the server
            data = self.client_socket.recv(1024)
            received = data.decode()
            print(f"Received: {received}")  # Display the received message

            # Compare sent and received data to verify connection
            if received == f"ECHO_RESPONSE:{message}":
                print("Connection successful, data matches.")
            else:
                print("Data mismatch.")

        except Exception as e:
            # Catch and display any errors encountered during communication
            print(f"Client Error: {e}")