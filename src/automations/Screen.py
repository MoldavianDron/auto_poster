from __future__ import annotations
import time
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
import logging

from airtest.core.api import *

from device_manager import DeviceManager

ScreenNameT = TypeVar("ScreenNameT")

class Screen(ABC, Generic[ScreenNameT]):
    def __init__(self, registered_screens: List[Screen], device_manager: DeviceManager):
        self.registered_screens = registered_screens
        self.device_manager = device_manager
        self.logger = logging.getLogger(device_manager.get_device_serial_number())

    def get_name(self) -> ScreenNameT:
        raise NotImplementedError
    
    def handle_screen(self) -> Optional[Screen]:
        raise NotImplementedError
    
    def is_current_screen(self) -> bool:
        raise NotImplementedError

    def wait_screen_from_list(self, screen_names: List[ScreenNameT], timeout: float = 10) -> Optional[Screen]:
        self.logger.debug(f"Waiting for one of the screens from screens list: {str(screen_names)}")
        start = time.time()
        found_screen = None
        while time.time() - start < timeout:
            if found_screen != None:
                break
            for ScreenClass in self.registered_screens:
                screen = ScreenClass(self.registered_screens, self.device_manager)
                if any(screen_name == screen.get_name() for screen_name in screen_names):
                    self.logger.debug(f"Checking if is current screen: {screen.get_name()}")
                    if screen.is_current_screen():
                        found_screen = screen
                        break
            time.sleep(1)
        self.logger.debug(f"Found screen {'None' if found_screen is None else found_screen.get_name() }")
        return found_screen
    
    def detect_next_screen(self) -> Optional[Screen]:
        self.logger.debug(f"Detecting next screen...")
        for ScreenClass in self.registered_screens:
            screen = ScreenClass(self.registered_screens, self.device_manager)
            self.logger.debug(f"Checking if is current screen: {screen.get_name()}")
            if screen.is_current_screen():
                return screen
        self.logger.debug("Unknown screen")
        return None
    
    def wait_for_template(self, template_path: str, timeout: int = 10) -> str:
        start = time.time()
        template_matches = find_all(Template(template_path))
        is_template_present = template_matches != None

        while time.time() - start < timeout:
            if is_template_present:
                if any(m["confidence"] > 0.9 for m in template_matches):
                    break
            time.sleep(0.5)
            template_matches = find_all(Template(template_path))
            is_template_present = any(m["confidence"] > 0.9 for m in template_matches)
        
        if is_template_present:
            return template_path
        
        raise TargetNotFoundError


            
