from concurrent.futures import ProcessPoolExecutor

from airtest.core.api import wake

from logger import generate_run_id, create_logs_path, init_device_logger
from config import get_config, DeviceConfig
from device_manager import DeviceManager
from automations import instagram_posting, set_post_info

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
        
        posts_info = device["automations"]["INSTAGRAM"]["post_info"]
        for post_info in posts_info:
            set_post_info(post_info=post_info)
            instagram_posting(device_manager=device_manager)

        logger.info("Automation finished")
    except Exception as error:
        logger.critical(f"Automation failed with exception: {str(error)}")

if __name__ == "__main__":
    run_id = generate_run_id()
    log_dir = create_logs_path(run_id=run_id)

    devices = get_config()["devices"]

    with ProcessPoolExecutor() as executor:
        executor.map(worker, devices, [log_dir] * len(devices))

