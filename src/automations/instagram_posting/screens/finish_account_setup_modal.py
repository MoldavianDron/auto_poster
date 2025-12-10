import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from project_root import PROJECT_ROOT

from automations.Screen import Screen
from .screen_names import InstagramPostingScreenNames

class FinishAccountSetupModal(Screen):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        super().__init__(registered_screens, device_manager)
        self.templates_path = os.path.join(PROJECT_ROOT, "automations", "instagram_posting", "templates")
        self.logger = logging.getLogger(self.device_manager.get_device_serial())

    def get_name(self):
        return InstagramPostingScreenNames.FINISH_ACCOUNT_SETUP_MODAL.value
    
    def is_current_screen(self):
        header_template_path = os.path.join(self.templates_path, "finish_account_setup_header.png")

        matching_templates = find_all(Template(header_template_path))
        if matching_templates == None:
            return False

    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")
        not_now_btn_template_path = os.path.join(self.templates_path, "finish_account_setup_not_now.png")

        touch(Template(not_now_btn_template_path))

        next_screen = self.wait_screen_from_list(
            screen_names=[
                InstagramPostingScreenNames.HOME
            ]
        )

        if next_screen == None:
            return self.detect_next_screen()

        return next_screen