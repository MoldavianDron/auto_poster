import time
import os
import logging
from device_manager import DeviceManager
from project_root import PROJECT_ROOT
from airtest.core.api import *

templates_path = os.path.join(PROJECT_ROOT, "automations", "socks_tun_proxy", "templates")

def ensure_proxy_disabled(device_manager: DeviceManager):
    enable_proxy_btn_template_path = os.path.join(templates_path, "enable_socks_tun.png")
    template_matches = find_all(Template(enable_proxy_btn_template_path))
    if template_matches is None:
        raise TargetNotFoundError("Proxy is not disabled")
    logging.getLogger(device_manager.get_device_serial()).info("Proxy disabled")

def ensure_proxy_enabled(device_manager: DeviceManager):
    disable_proxy_btn_template_path = os.path.join(templates_path, "disable_socks_tun.png")
    template_matches = find_all(Template(disable_proxy_btn_template_path))
    if template_matches is None:
        raise TargetNotFoundError("Proxy is not enabled")
    logging.getLogger(device_manager.get_device_serial()).info("Proxy enabled")

def is_proxy_enabled(device_manager: DeviceManager):
    disable_proxy_btn_template_path = os.path.join(templates_path, "disable_socks_tun.png")
    template_matches = find_all(Template(disable_proxy_btn_template_path))
    if template_matches is None:
        return False
    return any(m["confidence"] > 0.9 for m in template_matches)
    
def is_proxy_disabled(device_manager: DeviceManager):
    enable_proxy_btn_template_path = os.path.join(templates_path, "enable_socks_tun.png")
    template_matches = find_all(Template(enable_proxy_btn_template_path))
    if template_matches is None:
        return False
    return any(m["confidence"] > 0.9 for m in template_matches)
    
def disable_socks_tun_proxy(device_manager: DeviceManager):
    start_app("hev.sockstun")
    time.sleep(3)
    if is_proxy_disabled(device_manager):
        print(f"✅ Proxy already disabled")
        return
    disable_proxy_btn_template_path = os.path.join(templates_path, "disable_socks_tun.png")
    touch(Template(disable_proxy_btn_template_path))
    time.sleep(1)
    ensure_proxy_disabled(device_manager)

def enable_socks_tun_proxy(device_manager: DeviceManager):
    start_app("hev.sockstun")
    time.sleep(3)
    if is_proxy_enabled(device_manager):
        print(f"✅ Proxy already enabled")
        return
    enable_proxy_btn_template_path = os.path.join(templates_path, "enable_socks_tun.png")
    touch(Template(enable_proxy_btn_template_path))
    time.sleep(1)
    ensure_proxy_enabled(device_manager)