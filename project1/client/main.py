
import sys
from modules import MachineInfo, EchoClient, ChatClient, SNTPClient, Connection, ErrorManager

def main():
    # Instantiate machine information module (for hostname, IP, interfaces)
    machine_info = MachineInfo()  

    # Create a connection object and open client socket to the server
    connection = Connection()
    client_socket = connection.start()

    while True:
        # Main menu display for user interaction
        print("\nNetwork Diagnostic & Tool Package\n")
        print("1. Machine Information")
        print("2. Echo Test")
        print("3. SNTP Time Synchronization")
        print("4. Chat Module")
        print("5. Error Management & Socket Settings")
        print("6. set server address")
        print("0. Exit")

        choice = input("Select an option:").strip()

        match choice:
            case "1":
                # Module A: Machine Information
                # Display system hostname, IP, network interfaces
                print("Machine Information: ")
                machine_info.display_info()

            case "2":
                # Module B: Echo Test
                # Start client-side echo test with server
                print("Echo Test")
                echo_client = EchoClient(client_socket)
                echo_client.start() 

            case "3":
                # Module C: SNTP Time Synchronization
                # Retrieve network time from NTP server
                print("SNTP Time Synchronization")
                sntp = SNTPClient()
                # NOTE: SNTPClient prints output only when selected, no extra debug prints
                sntp.show_sync()

            case "4":
                # Module D: Chat Module
                # Launch chat client; user selects role within module
                print("Chat Module")
                chat = ChatClient(client_socket)
                chat.start()
                # TODO: Ensure no leftover debug prints in chat modules for final submission

            case "5":
                # Module E: Error Management & Socket Settings
                # Interactive menu for timeout, buffer sizes, blocking/non-blocking mode
                print("Error Management & Socket Settings")
                error_manager = ErrorManager(client_socket)
                error_manager.interactive_menu()
                # NOTE: No emoji prints in final version

            case "6":
                # Allow dynamic server address change
                print("Set server address")
                # Close previous socket before reinitializing connection
                connection.close()               
                connection = Connection()       # reinitialize Connection object
                client_socket = connection.start()  # reconnect to server

            case "0":
                # Exit program cleanly
                print("Exiting program...")
                sys.exit(0)

            case _:
                # Invalid menu option handler
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()