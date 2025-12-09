import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from logger import get_log_path
from project_root import PROJECT_ROOT

from automations.instagram_posting.post_info import get_instagram_post_info
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
        all_home_btn_matches = self.get_all_templates_matches([active_home_btn_template_path])
        if all_home_btn_matches == None:
            return False
        
        your_story_template_path = os.path.join(self.templates_path, "home_your_story.png")
        your_story_matches = find_all(Template(your_story_template_path))
        if your_story_matches == None:
            return False
        
        return (
            any(m["confidence"] > 0.9 for m in all_home_btn_matches) and
            any(m["confidence"] > 0.9 for m in your_story_matches)
        )

    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")
        post_info = get_instagram_post_info()

        if post_info["use_audio"]:
            self.device_manager.open_url(post_info["audio_url"])
            self.logger.debug(f"{self.get_name()}: Opened post with needed audio")

            song_btn_template_path = self.wait_for_template(
                template_path=os.path.join(self.templates_path, "home_song_btn.png")
            )
            touch(Template(song_btn_template_path))
            self.logger.debug(f"{self.get_name()}: Song btn has been clicked")

            use_audio_btn_template_path = self.wait_for_template(
                template_path=os.path.join(self.templates_path, "home_use_audio_btn.png")
            )
            touch(Template(use_audio_btn_template_path))
            self.logger.debug(f"{self.get_name()}: Use audio btn has been clicked")
        else:
            make_post_btn_template_path = os.path.join(self.templates_path, "home_make_post_btn.png")
            make_post_btn_second_template_path = os.path.join(self.templates_path, "home_make_post_btn_second.png")

            make_post_btn_any_template = self.wait_for_any_template([make_post_btn_template_path, make_post_btn_second_template_path])
            touch(Template(make_post_btn_any_template))
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