import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from project_root import PROJECT_ROOT

from automations.instagram_posting.post_info import get_post_info
from automations.Screen import Screen
from .screen_names import InstagramPostingScreenNames

class NewPost(Screen):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        super().__init__(registered_screens, device_manager)
        self.templates_path = os.path.join(PROJECT_ROOT, "automations", "instagram_posting", "templates")
        self.logger = logging.getLogger(self.device_manager.get_device_serial_number())

    def get_name(self):
        return InstagramPostingScreenNames.NEW_POST.value
    
    def is_current_screen(self):
        new_post_back_btn_template_path = os.path.join(self.templates_path, "new_post_back_btn.png")
        back_btn_matches = find_all(Template(new_post_back_btn_template_path))
        if back_btn_matches == None:
            return False
        
        return (
            any(m["confidence"] > 0.9 for m in back_btn_matches)
        )
    
    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")
        post_info = get_post_info()

        if post_info["use_caption"]:
            caption_placeholder_template_path = self.wait_for_template(
                template_path=os.path.join(self.templates_path, "new_post_caption_placeholder.png")
            )
            touch(Template(caption_placeholder_template_path))
            self.logger.debug(f"{self.get_name()}: Clicked on caption placeholder")
            time.sleep(2)

            text(post_info["caption"])
            self.logger.debug(f"{self.get_name()}: Typed caption")
            time.sleep(2)

            ok_btn_template_path = self.wait_for_template(
                template_path=os.path.join(self.templates_path, "new_post_ok_btn.png")
            )
            touch(Template(ok_btn_template_path))
            self.logger.debug(f"{self.get_name()}: Clicked ok btn")
            time.sleep(2)

        share_btn_template_path = self.wait_for_template(
            template_path=os.path.join(self.templates_path, "new_post_share_btn.png")
        )
        touch(Template(share_btn_template_path))
        self.logger.debug(f"{self.get_name()}: Share btn has been clicked")
        time.sleep(20)

        self.logger.info(f"{self.get_name()}: Assuming post has been made")
        return None



