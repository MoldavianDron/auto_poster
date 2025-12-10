import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from project_root import PROJECT_ROOT

from automations.Screen import Screen
from automations.instagram_posting.post_info import get_instagram_post_info
from .screen_names import InstagramPostingScreenNames

class OnMakePost(Screen):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        super().__init__(registered_screens, device_manager)
        self.templates_path = os.path.join(PROJECT_ROOT, "automations", "instagram_posting", "templates")
        self.logger = logging.getLogger(self.device_manager.get_device_serial())
        self.photo_selection_hardcoded_coordinates = {
            "1": (491, 1545),
            "2": (761, 1546),
            "3": (1031, 1544),
            "4": (225, 1813),
        }

    def get_name(self):
        return InstagramPostingScreenNames.ON_MAKE_POST.value
    
    def is_current_screen(self):
        new_post_template_path = os.path.join(self.templates_path, "on_make_post_new_post.png")
        new_post_matches = find_all(Template(new_post_template_path))
        if new_post_matches == None:
            return False
        
        return (
            any(m["confidence"] > 0.9 for m in new_post_matches)
        )
    
    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")

        select_multiple_template_path = self.wait_for_template(
            template_path=os.path.join(self.templates_path, "on_make_post_select_multiple_btn.png")
        )
        touch(Template(select_multiple_template_path))
        self.logger.debug(f"{self.get_name()}: Select multiple btn has been clicked")
        time.sleep(1)

        photos_amount = get_instagram_post_info()["photos_amount"]
        if (photos_amount == 1):
            next_btn_template_path = os.path.join(self.templates_path, "on_make_post_next_btn.png")
            touch(Template(next_btn_template_path))
            time.sleep(1)
            self.logger.debug(f"{self.get_name()}: Next btn has been clicked")

        for photo_num in range(2, photos_amount + 1):
            touch(self.photo_selection_hardcoded_coordinates[str(photo_num)])
            time.sleep(1)
        self.logger.debug(f"{self.get_name()}: Selected {str(photos_amount)} photos")

        next_btn_template_path = os.path.join(self.templates_path, "on_make_post_next_btn.png")
        touch(Template(next_btn_template_path))
        self.logger.debug(f"{self.get_name()}: Next btn has been clicked")

        preview_next_btn_template_path = self.wait_for_template(
            template_path=os.path.join(self.templates_path, "on_make_post_preview_next_btn.png")
        )
        touch(Template(preview_next_btn_template_path))
        self.logger.debug(f"{self.get_name()}: Preview next btn has been clicked")

        next_screen = self.wait_screen_from_list(
            screen_names=[
                InstagramPostingScreenNames.NEW_POST,
            ]
        )

        if next_screen == None:
            return self.detect_next_screen()

        return next_screen


