import socket
import os
from .sntp_client import SNTPClient

class ErrorManager:
    def __init__(self, sock, log_dir="client/error_logs"):
        """
        Initialize ErrorManager:
        - sock: the socket object to manage
        - log_dir: directory to store error logs
        """
        sntp = SNTPClient()
        self.sock = sock
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(
            log_dir, f"error_manager_{sntp.get_time_str()}.txt"
        )

    def log(self, message):
        """Log message to console and file."""
        print(f"[ERROR MANAGER] {message}")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def show_current_settings(self):
        """Display current socket settings."""
        try:
            timeout = self.sock.gettimeout()
            send_buf = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            recv_buf = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
            blocking = self.sock.getblocking()

            self.log("Current Socket Settings:")
            self.log(f"   Timeout: {timeout}")
            self.log(f"   Send Buffer: {send_buf} bytes")
            self.log(f"   Receive Buffer: {recv_buf} bytes")
            self.log(f"   Mode: {'Blocking' if blocking else 'Non-blocking'}")
        except Exception as e:
            self.log(f"Error reading socket settings: {e}")

    def set_timeout(self):
        """Set socket timeout value."""
        try:
            value = float(input("Enter new timeout value in seconds (0 for no timeout): "))
            if value == 0:
                self.sock.settimeout(None)
                self.log("Timeout disabled (no timeout).")
            else:
                self.sock.settimeout(value)
                self.log(f"Timeout set to {value} seconds.")
        except ValueError:
            self.log("Invalid value. Please enter a number.")
        except Exception as e:
            self.log(f"Error setting timeout: {e}")

    def set_buffers(self):
        """Set send and receive buffer sizes for the socket."""
        try:
            send_buf = int(input("Enter new SEND buffer size (bytes): "))
            recv_buf = int(input("Enter new RECEIVE buffer size (bytes): "))
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buf)
            self.log(f"Send buffer set to {send_buf} bytes.")
            self.log(f"Receive buffer set to {recv_buf} bytes.")
        except ValueError:
            self.log("Invalid value. Please enter integers only.")
        except Exception as e:
            self.log(f"Error setting buffer sizes: {e}")

    def toggle_blocking_mode(self):
        """Switch between blocking and non-blocking mode."""
        try:
            current = self.sock.getblocking()
            new_mode = not current
            self.sock.setblocking(new_mode)
            self.log(f"Blocking mode changed to: {'Blocking' if new_mode else 'Non-blocking'}")
        except Exception as e:
            self.log(f"Error toggling blocking mode: {e}")

    def simulate_timeout(self):
        """Simulate a timeout exception for testing purposes."""
        try:
            self.sock.settimeout(1)
            self.log("Simulating timeout with 1 second setting...")
            self.sock.recv(1024)  # Expected: timeout exception
        except socket.timeout:
            self.log("Timeout occurred as expected.")
        except Exception as e:
            self.log(f"Error during timeout simulation: {e}")
        finally:
            self.sock.settimeout(None)

    def interactive_menu(self):
        """Display interactive menu to manage socket settings and errors."""
        while True:
            print("\n=== ERROR MANAGEMENT & SETTINGS ===")
            print("1. Show Current Socket Settings")
            print("2. Set Timeout")
            print("3. Set Buffer Sizes")
            print("4. Toggle Blocking / Non-Blocking Mode")
            print("5. Simulate Timeout Error")
            print("0. Return to Main Menu")
            choice = input("Select an option: ")

            if choice == "1":
                self.show_current_settings()
            elif choice == "2":
                self.set_timeout()
            elif choice == "3":
                self.set_buffers()
            elif choice == "4":
                self.toggle_blocking_mode()
            elif choice == "5":
                self.simulate_timeout()
            elif choice == "0":
                self.log("Returning to main menu...")
                break
            else:
                print("Invalid choice, please try again.")