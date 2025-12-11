from typing import Optional

from config import ContentInfo

content_info_global = None

def get_content_info() -> Optional[ContentInfo]:
    return content_info_global

def set_content_info(post_info: Optional[ContentInfo]) -> None:
    global content_info_global
    content_info_global = post_info