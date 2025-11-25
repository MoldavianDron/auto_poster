from airtest.core.api import connect_device
import subprocess
from typing import Optional


class DeviceManager:
    def __init__(self, serial_number: str, connection_type: str, device_ip: Optional[str] = None):
        self.serial_number = serial_number
        self.connection_type = connection_type
        self.device_ip = device_ip
        self.device = None

    def get_device_serial_number(self) -> str:
        return self.serial_number

    def _enable_tcpip(self):
        """
        Enable TCP/IP mode for the device via adb.
        """
        subprocess.run(["adb", "-s", self.serial_number, "tcpip", "5555"], check=True)

    def connect(self):
        """
        Connect device via Airtest.
        - USB: connect_device(f"Android:///{serial_number}")
        - TCP: enables TCP mode then connects via device_ip
        """
        if self.connection_type == "usb":
            # Connect via USB
            self.device = connect_device(f"Android:///{self.serial_number}")
        elif self.connection_type == "tcp" and self.device_ip:
            # Enable TCP mode first
            self._enable_tcpip()
            # Then connect via TCP
            self.device = connect_device(f"Android://127.0.0.1:5037/{self.device_ip}:5555")
        else:
            raise ValueError(f"Invalid connection config for device {self.serial_number}")

        return self.device
