import ntplib
from datetime import datetime

class SNTPClient:
    def __init__(self, server="pool.ntp.org"):
        # Default NTP server to synchronize with
        self.server = server

    def get_network_time(self, verbose=False):
        """
        Retrieve current time from the NTP server.
        verbose=True will display detailed information on the console.
        """
        if verbose:
            print(f"[SNTP] Connecting to {self.server} ...")

        try:
            client = ntplib.NTPClient()
            response = client.request(self.server, version=3)
            network_time = datetime.fromtimestamp(response.tx_time)
            local_time = datetime.now()
            time_difference = (network_time - local_time).total_seconds()

            if verbose:
                # Show synchronization details
                print("\n--- SNTP Time Synchronization ---")
                print(f"NTP Server   : {self.server}")
                print(f"Network Time : {network_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Local Time   : {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Time Offset  : {time_difference:.3f} seconds")
                print("---------------------------------\n")

            return network_time

        except Exception as e:
            if verbose:
                print(f"[SNTP] Error: {e}")
                print("[SNTP] Falling back to local system time.")
            return datetime.now()

    def get_time_str(self, fmt="%Y%m%d_%H%M%S"):
        """
        Return current network or local time as a formatted string.
        This is used for log file naming or timestamping.
        """
        current_time = self.get_network_time(verbose=False)
        return current_time.strftime(fmt)

    def show_sync(self):
        """
        Function called when user selects SNTP module from the main menu.
        Displays time synchronization information.
        """
        print("\n[SNTP MODULE] Time Synchronization Started...")
        self.get_network_time(verbose=True)