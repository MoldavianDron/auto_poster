import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from project_root import PROJECT_ROOT

from automations.instagram_posting.post_info import get_instagram_post_info
from automations.Screen import Screen
from .screen_names import InstagramPostingScreenNames

class RateInstagramModal(Screen):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        super().__init__(registered_screens, device_manager)
        self.templates_path = os.path.join(PROJECT_ROOT, "automations", "instagram_posting", "templates")
        self.logger = logging.getLogger(self.device_manager.get_device_serial_number())

    def get_name(self):
        return InstagramPostingScreenNames.RATE_INSTAGRAM_MODAL.value

    def is_current_screen(self):
        title_template_path = os.path.join(self.templates_path, "rate_instagram_title.png")
        title_template_matches = self.get_all_templates_matches([title_template_path])
        if title_template_matches is None:
            return False
        
    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")

        remind_later_template_path = os.path.join(self.templates_path, "rate_instagram_remind_later.png")
        resign_template_path = os.path.join(self.templates_path, "rate_instagram_resign.png")
        
        skip_instagram_rating_template = self.wait_for_any_template([remind_later_template_path, resign_template_path])
        touch(Template(skip_instagram_rating_template))
        self.logger.debug(f"{self.get_name()}: Instagram rate has been skipped")

        next_screen = self.wait_screen_from_list(
            screen_names=[
                InstagramPostingScreenNames.HOME
            ]
        )

        if next_screen == None:
            return self.detect_next_screen()

        return next_screen


