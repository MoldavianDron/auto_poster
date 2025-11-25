import json
from pathlib import Path
from typing import TypedDict, List, Literal, Optional

class ConnectionConfig(TypedDict):
    type: Literal["usb", "tcp"]
    device_ip: str


class InstagramPostInfo(TypedDict):
    profile_name: str
    folder_url: str
    photos_amount: int
    audio_url: str
    use_audio: bool
    caption: str
    use_caption: bool


class InstagramAutomation(TypedDict):
    skip: bool
    post_info: List[InstagramPostInfo]


class Automations(TypedDict, total=False):
    INSTAGRAM: InstagramAutomation


class DeviceConfig(TypedDict):
    serial_number: str
    connection: ConnectionConfig
    automations: Automations


class Config(TypedDict):
    devices: List[DeviceConfig]


def get_config() -> Config:
    """
    Load and return the project config from `config.json`.
    """
    config_path = Path(__file__).parent.parent.parent / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    return config_data

def find_device_config(serial_number: str, config: Config) -> Optional[DeviceConfig]:
    """
    Find and return a DeviceConfig by its serial number.
    Returns None if not found.
    """
    for device in config.get("devices", []):
        if device.get("serial_number") == serial_number:
            return device
    return None
