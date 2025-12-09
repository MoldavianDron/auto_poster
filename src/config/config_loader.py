import json
from pathlib import Path
from typing import TypedDict, List, Literal, Optional, Union


# -------------------------
# Base connection config
# -------------------------
class ConnectionConfig(TypedDict):
    type: Literal["usb", "tcp"]
    device_ip: str


# -------------------------
# content[] entry
# -------------------------
class ContentInfo(TypedDict):
    post_number: int
    profile_name: str
    folder_url: str


# -------------------------
# INSTAGRAM post_info entry
# -------------------------
class InstagramPostInfo(TypedDict):
    post_number: int
    profile_name: str
    automation: Literal["INSTAGRAM"]
    photos_amount: int
    use_audio: bool
    audio_url: str
    use_caption: bool
    caption: str
    post_photo: bool


# -------------------------
# THREADS post_info entry
# -------------------------
class ThreadsPostInfo(TypedDict):
    post_number: int
    profile_name: str
    automation: Literal["THREADS"]
    photos_amount: int
    use_caption: bool
    caption: str
    post_photo: bool


# -------------------------
# TWITTER post_info entry
# -------------------------
class TwitterPostInfo(TypedDict):
    post_number: int
    profile_name: str
    automation: Literal["TWITTER"]
    photos_amount: int
    use_caption: bool
    caption: str
    post_photo: bool


# Union of all possible post types
PostInfo = Union[InstagramPostInfo, ThreadsPostInfo, TwitterPostInfo]


# -------------------------
# automations object
# -------------------------
class Automations(TypedDict):
    content: List[ContentInfo]
    posts_info: List[PostInfo]


# -------------------------
# device entry
# -------------------------
class DeviceConfig(TypedDict):
    serial_number: str
    connection: ConnectionConfig
    automations: Automations


# -------------------------
# root config
# -------------------------
class Config(TypedDict):
    devices: List[DeviceConfig]


# -------------------------
# Functions
# -------------------------
def get_config() -> Config:
    config_path = Path(__file__).parent.parent.parent / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    return config_data


def find_device_config(serial_number: str, config: Config) -> Optional[DeviceConfig]:
    for device in config.get("devices", []):
        if device.get("serial_number") == serial_number:
            return device
    return None
