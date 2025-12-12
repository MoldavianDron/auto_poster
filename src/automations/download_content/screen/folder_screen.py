import os
from typing import List
import logging

from airtest.core.api import *

from device_manager import DeviceManager
from project_root import PROJECT_ROOT

from automations.instagram_posting.post_info import get_instagram_post_info
from automations.Screen import Screen
from .screen_names import DownloadContentScreenNames

class FolderScreen(Screen):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        super().__init__(registered_screens, device_manager)
        self.templates_path = os.path.join(PROJECT_ROOT, "automations", "download_content", "templates")
        self.logger = logging.getLogger(self.device_manager.get_device_serial())

    def get_name(self):
        return DownloadContentScreenNames.FOLDER_SCREEN.value
    
    def is_current_screen(self):
        asset_icon_template_path = os.path.join(self.templates_path, "folder_screen_asset_icon.png")
        all_asset_icon_matches = self.get_all_templates_matches([ asset_icon_template_path])
        if all_asset_icon_matches == None:
            return False

        return (
            any(m["confidence"] > 0.9 for m in all_asset_icon_matches)
        )

    def handle_screen(self):
        self.logger.debug(f"{self.get_name()}: Handling screen")
        asset_icon_template_path = os.path.join(self.templates_path, "folder_screen_asset_icon.png")
        all_asset_icon_matches = self.get_all_templates_matches([ asset_icon_template_path])

        for match in all_asset_icon_matches:
            x, y = match['result']
            self.logger.debug(f"{match}")
            self.logger.debug(f"{x}, {y}, match result")
            touch((x + 200, y - 200), duration=1)

            download_image_template_path = self.wait_for_template(
                template_path=os.path.join(self.templates_path, "folder_screen_download_image.png"),
                timeout=2
            )
            touch(Template(download_image_template_path))

            download_btn_template_path = self.wait_for_template(
                template_path=os.path.join(self.templates_path, "folder_screen_download.png"),
                timeout=5
            )
            touch(Template(download_btn_template_path))

            downloaded_mark_template_path = self.wait_for_template(
                template_path=os.path.join(self.templates_path, "folder_screen_downloaded_mark.png"),
                timeout=20
            )
        self.logger.debug("Content has been downloaded")

        return None