from concurrent.futures import ProcessPoolExecutor
from typing import Optional, List
import os

from airtest.core.api import wake

from logger import generate_run_id, create_logs_path, init_device_logger, get_log_folder
from config import get_config, DeviceConfig, InstagramPostInfo, PostInfo
from device_manager import DeviceManager
from automations import instagram_posting, set_instagram_post_info, disable_socks_tun_proxy, enable_socks_tun_proxy, set_content_info, download_content

def find_instagram_post_info(
    posts_info: List[PostInfo],
    profile_name: str,
    post_number: int
) -> Optional[InstagramPostInfo]:
    for post in posts_info:
        if post["automation"] != "INSTAGRAM":
            continue

        if (
            post["profile_name"] == profile_name and
            post["post_number"] == post_number
        ):
            return post

    return None


def worker(device: DeviceConfig, log_dir: str):
    logger = init_device_logger(log_dir=log_dir, device_serial=device["serial_number"])
    logger.debug(f"Logger initiated")

    try:
        device_manager = DeviceManager(
            serial_number=device["serial_number"],
            connection_type=device["connection"]["type"],
            device_ip=device["connection"]["device_ip"]
        )
        logger.info("Automation started")

        device_manager.connect()
        logger.debug("Device connected")

        wake()
        logger.debug("Device unlocked")

        # enable_socks_tun_proxy(device_manager=device_manager)
        # disable_socks_tun_proxy(device_manager=device_manager)

        posts = device["automations"]["content"]
        for post in posts:
            print(post)
            set_content_info(post)
            download_content(device_manager=device_manager)
            # instagram_post_info = find_instagram_post_info(
            #     posts_info=device["automations"]["posts_info"],
            #     post_number=post["post_number"],
            #     profile_name=post["profile_name"]
            # )
            # if instagram_post_info != None:
            #     logger.debug(f"PROFILE NAME: {post['profile_name']}. POST NUMBER: {post['post_number']}")
            #     logger.debug(f"Found instagram post")
            #     set_instagram_post_info(instagram_post_info)
            #     instagram_posting(device_manager=device_manager)
            # else:
            #     logger.debug("Instagram post info not found, skip posting")
            

        logger.info("Automation finished")
    except Exception as error:
        logger.critical(f"Automation failed with exception: {str(error)}")
        device_manager.save_screenshot(os.path.join(get_log_folder(logger=logger), "screenshot.png"))

if __name__ == "__main__":
    run_id = generate_run_id()
    log_dir = create_logs_path(run_id=run_id)

    devices = get_config()["devices"]

    with ProcessPoolExecutor() as executor:
        executor.map(worker, devices, [log_dir] * len(devices))

