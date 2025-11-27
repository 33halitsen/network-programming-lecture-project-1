class EchoServer:
    def handle_client(self, client_socket, data):
        """
        Handle an echo request from the client.
        Sends back the received message for basic connection testing.
        """
        try:
            # Extract message from the data string
            if "DATA=" in data:
                message = data.split("DATA=")[1]
            else:
                message = "No DATA provided"

            print(f"[ECHO] Client says: {message}")

            # Prepare and send response
            response = f"ECHO_RESPONSE:{message}"
            client_socket.sendall(response.encode())

        except Exception as e:
            # Send error back to client if exception occurs
            client_socket.sendall(f"ECHO_ERROR:{e}".encode())