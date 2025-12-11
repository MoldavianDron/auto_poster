import logging
from device_manager import DeviceManager
from ..Screen import Screen
from .content_info import get_content_info
from .screen.registered_screens import REGISTERED_SCREENS
from .screen.screen_names import DownloadContentScreenNames

def download_content(device_manager: DeviceManager):
    logger = logging.getLogger(device_manager.get_device_serial())
    logger.info("Content downloading started")

    content_url = get_content_info()['folder_url']
    device_manager.open_url(content_url)

    screen = Screen(
        registered_screens=REGISTERED_SCREENS,
        device_manager=device_manager
    )

    current_screen = screen.wait_screen_from_list(
        screen_names=[
            DownloadContentScreenNames.FOLDER_SCREEN
        ],
        timeout=20
    )

    if current_screen is None:
        raise BaseException("Screen not found")
    
    while current_screen is not None:
        current_screen = current_screen.handle_screen()

    logger.info("Content downloading finished")


