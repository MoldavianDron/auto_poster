import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from project_root import PROJECT_ROOT

from automations.Screen import Screen
from .screen_names import InstagramPostingScreenNames

class Home(Screen):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        super().__init__(registered_screens, device_manager)
        self.templates_path = os.path.join(PROJECT_ROOT, "automations", "instagram_posting", "templates")
        self.logger = logging.getLogger(self.device_manager.get_device_serial_number())

    def get_name(self):
        return InstagramPostingScreenNames.HOME.value
    
    def is_current_screen(self):
        active_home_btn_template_path = os.path.join(self.templates_path, "home_active_home_btn.png")
        active_home_btn_matches = find_all(Template(active_home_btn_template_path))
        if active_home_btn_matches == None:
            return False
        
        your_story_template_path = os.path.join(self.templates_path, "home_your_story.png")
        your_story_matches = find_all(Template(your_story_template_path))
        if your_story_matches == None:
            return False
        
        return (
            any(m["confidence"] > 0.9 for m in active_home_btn_matches) and
            any(m["confidence"] > 0.9 for m in your_story_matches)
        )

    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")

        make_post_btn_template_path = os.path.join(self.templates_path, "home_make_post_btn.png")
        touch(Template(make_post_btn_template_path))
        self.logger.debug(f"{self.get_name()}: Make post btn has been clicked")

        next_screen = self.wait_screen_from_list(
            screen_names=[
                InstagramPostingScreenNames.ON_MAKE_POST,
                InstagramPostingScreenNames.ON_MAKE_STORY
            ]
        )

        if next_screen == None:
            return self.detect_next_screen()

        return next_screen