from netmiko import ConnectHandler

class NetworkConfigManager:
    def __init__(self):
        self.device = {
            "device_type": "linux",
            "ip": "127.0.0.1",
            "username": "admin",
            "password": "password",
            "port": 2222,
        }
        self.net_connect = None

    def connect(self) -> None:
        """Etablera SSH-anslutning."""
        self.net_connect = ConnectHandler(**self.device)
        print("Connected to device.")

    def disconnect(self) -> None:
        """Stäng anslutningen."""
        if self.net_connect:
            self.net_connect.disconnect()
            print("Disconnected from device.")

    def show_hostname(self) -> str:
        """Returnera nuvarande hostname från konfigurationsfilen."""
        command = "cat /etc/config/hostname/config.txt"
        output = self.net_connect.send_command(command)
        return output.strip()

    def show_response_prefix(self) -> str:
        """Returnera nuvarande response prefix från konfigurationsfilen."""
        command = "cat /etc/config/response/config.txt"
        output = self.net_connect.send_command(command)
        return output.strip()

    def show_interface_state(self) -> str:
        """Returnera nuvarande interface state från konfigurationsfilen."""
        command = "cat /etc/config/interface/config.txt"
        output = self.net_connect.send_command(command)
        return output.strip()

    def update_hostname(self, new_value: str) -> None:
        """Uppdatera hostname-konfigurationen."""
        command = f"bash -c \"echo 'hostname: {new_value}' > /etc/config/hostname/config.txt\""
        self.net_connect.send_command(command)
        print(f"Hostname updated to: {new_value}")

    def update_response_prefix(self, new_value: str) -> None:
        """Uppdatera response prefix-konfigurationen."""
        command = f"bash -c \"echo 'response_prefix: {new_value}' > /etc/config/response/config.txt\""
        self.net_connect.send_command(command)
        print(f"Response prefix updated to: {new_value}")

    def update_interface_state(self, new_value: str) -> None:
        """Uppdatera interface state-konfigurationen."""
        if new_value not in ["up", "down"]:
            raise ValueError("Invalid value! Interface state must be 'up' or 'down'.")
        command = f"bash -c \"echo 'interface_state: {new_value}' > /etc/config/interface/config.txt\""
        self.net_connect.send_command(command)
        print(f"Interface state updated to: {new_value}")

if __name__ == "__main__":
    manager = NetworkConfigManager()
    manager.connect()
    print(manager.show_hostname())
    manager.disconnect()

    # Exempel: Uppdatera konfigurationerna
    # manager.update_hostname("RouterX")
    # manager.update_response_prefix("CustomPrefix:")
    
    # try:
    #     # Försök med ett ogiltigt värde för att utlösa exception
    #     manager.update_interface_state("upwards")
    # except ValueError as e:
    #     print(e)
        
    # # Använd ett giltigt värde
    # manager.update_interface_state("up")

    # # Hämta och visa de aktuella konfigurationsvärdena
    # hostname = manager.show_hostname()
    # response_prefix = manager.show_response_prefix()
    # interface_state = manager.show_interface_state()

    # print(f"Current Hostname: {hostname}")
    # print(f"Current Response Prefix: {response_prefix}")
    # print(f"Current Interface State: {interface_state}")

    # manager.disconnect()