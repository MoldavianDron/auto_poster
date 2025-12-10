import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from project_root import PROJECT_ROOT

from automations.instagram_posting.post_info import get_instagram_post_info
from automations.Screen import Screen
from .screen_names import InstagramPostingScreenNames

class SimplifiedNavigationModal(Screen):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        super().__init__(registered_screens, device_manager)
        self.templates_path = os.path.join(PROJECT_ROOT, "automations", "instagram_posting", "templates")
        self.logger = logging.getLogger(self.device_manager.get_device_serial())

    def get_name(self):
        return InstagramPostingScreenNames.SIMPLIFIED_NAVIGATION_MODAL.value
    
    def is_current_screen(self):
        title_template_path = os.path.join(self.templates_path, "simplified_navigation_modal_title.png")
        title_matches = find_all(Template(title_template_path))
        if title_matches == None:
            return False
        
        return (
            any(m["confidence"] > 0.9 for m in title_matches)
        )
    
    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")

        confirm_btn_template_path = os.path.join(self.templates_path, "simplified_navigation_modal_confirm_btn.png")
        touch(Template(confirm_btn_template_path))
        self.logger.debug(f"{self.get_name()}: Confirm button has been clicked")

        next_screen = self.wait_screen_from_list(
            screen_names=[
                InstagramPostingScreenNames.HOME
            ]
        )

        if next_screen == None:
            return self.detect_next_screen()

        return next_screen