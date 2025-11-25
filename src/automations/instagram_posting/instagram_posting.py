import time
import logging

from airtest.core.api import *

from device_manager import DeviceManager

from ..Screen import Screen
from .screens.registered_screens import REGISTERED_SCREENS
from .screens.screen_names import InstagramPostingScreenNames

def instagram_posting(device_manager: DeviceManager):
    logger = logging.getLogger(device_manager.get_device_serial_number())
    logger.info("Instagram posting started")

    stop_app("com.instagram.android")
    logger.debug("Stopped app")
    time.sleep(2)

    clear_app("com.instagram.android")
    logger.debug("Cleaned up app from memory")

    start_app("com.instagram.android")
    time.sleep(2)
    logger.debug("Started app")

    screen = Screen(
        registered_screens=REGISTERED_SCREENS,
        device_manager=device_manager
    )

    logger.debug("Waiting for any modal or popup appears")
    current_screen = screen.wait_screen_from_list(
        screen_names=[
            InstagramPostingScreenNames.FINISH_ACCOUNT_SETUP_MODAL
        ],
        timeout=5
    )

    if current_screen is None:
        logger.debug("Waiting for any screen")
        current_screen = screen.wait_screen_from_list(
            screen_names=[
                InstagramPostingScreenNames.FINISH_ACCOUNT_SETUP_MODAL,
                InstagramPostingScreenNames.HOME,
                InstagramPostingScreenNames.ON_MAKE_POST,
                InstagramPostingScreenNames.ON_MAKE_STORY
            ],
            timeout=5
        )

    if current_screen is None:
        current_screen = screen.detect_next_screen()

    while current_screen is not None:
        current_screen = current_screen.handle_screen()

    logger.info("Instagram posting finished")