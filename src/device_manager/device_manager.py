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
    
    def open_url(self, url: str):
        # adb shell am start -a android.intent.action.VIEW -d https://www.instagram.com/reels/audio/2076918953126759/
        cmd = ["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return f"❌ Failed to get IP address: {result.stderr.strip()}"

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
    
    def save_screenshot(self, file_path: str) -> str:
        """
        Capture a screenshot from the connected Airtest device and save it to the provided file path.
        
        :param file_path: Full path where the screenshot will be saved.
        :return: Saved file path.
        """
        if not self.device:
            raise RuntimeError("Device is not connected. Call connect() first.")

        try:
            self.device.snapshot(filename=file_path)
            return file_path
        except Exception as e:
            raise RuntimeError(f"Failed to take screenshot: {e}")
