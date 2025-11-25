import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from project_root import PROJECT_ROOT

from automations.Screen import Screen
from .screen_names import InstagramPostingScreenNames

class OnMakeStory(Screen):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        super().__init__(registered_screens, device_manager)
        self.templates_path = os.path.join(PROJECT_ROOT, "automations", "instagram_posting", "templates")
        self.logger = logging.getLogger(self.device_manager.get_device_serial_number())

    def get_name(self):
        return InstagramPostingScreenNames.ON_MAKE_STORY.value
    
    def is_current_screen(self):
        story_btn_template_path = os.path.join(self.templates_path, "on_make_story_story.png")
        story_btn_matches = find_all(Template(story_btn_template_path))
        if story_btn_matches == None:
            return False
        
        add_media_btn_template_path = os.path.join(self.templates_path, "on_make_story_media.png")
        add_media_btn_matches = find_all(Template(add_media_btn_template_path))
        if add_media_btn_matches == None:
            return False
        
        print(story_btn_matches, add_media_btn_matches)
        return (
            any(m["confidence"] > 0.9 for m in story_btn_matches) and
            any(m["confidence"] > 0.9 for m in add_media_btn_matches)
        )
    
    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")

        post_btn_template_path = os.path.join(self.templates_path, "on_make_story_post_btn.png")
        touch(Template(post_btn_template_path))
        self.logger.debug(f"{self.get_name()}: Make post btn has been clicked")

        next_screen = self.wait_screen_from_list(
            screen_names=[
                InstagramPostingScreenNames.ON_MAKE_POST,
            ]
        )

        if next_screen == None:
            return self.detect_next_screen()
    
