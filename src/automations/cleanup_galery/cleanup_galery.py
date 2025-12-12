from device_manager import DeviceManager
import time
import logging
import os

from project_root import PROJECT_ROOT
from airtest.core.api import *

templates_path = os.path.join(PROJECT_ROOT, "automations", "cleanup_galery", "templates")

def cleanup_gallery_fn(device_manager: DeviceManager):
    start_app("com.android.documentsui")
    time.sleep(3)

    logger = logging.getLogger(device_manager.get_device_serial())
    logger.info("Gallery cleanup started")

    no_items_template_path = os.path.join(templates_path, "downloads_no_item.png")
    no_items_matches = find_all(Template(no_items_template_path))
    if no_items_matches is not None and any(m["confidence"] > 0.9 for m in no_items_matches):
        logger.debug("Gallery is already empty")
        return

    downloads_menu_template_path = os.path.join(templates_path, "downloads_menu.png")
    touch(Template(downloads_menu_template_path))
    time.sleep(1)

    select_all_template_path = os.path.join(templates_path, "downloads_select_all.png")
    touch(Template(select_all_template_path))
    time.sleep(1)

    delete_template_path = os.path.join(templates_path, "downloads_delete_icon.png")
    touch(Template(delete_template_path))
    time.sleep(1)

    ok_template_path = os.path.join(templates_path, "downloads_ok.png")
    touch(Template(ok_template_path))
    time.sleep(1)