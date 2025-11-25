from typing import Optional

from config import InstagramPostInfo

post_info_global = None

def get_post_info() -> Optional[InstagramPostInfo]:
    return post_info_global

def set_post_info(post_info: Optional[InstagramPostInfo]) -> None:
    global post_info_global
    print(post_info)
    post_info_global = post_info