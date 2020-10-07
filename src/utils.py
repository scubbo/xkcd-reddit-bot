import re
from typing import Optional


REGEX = re.compile('(?:https?://)?(?:www.)?xkcd.com/(\d+)/?')


def xkcd_linked_in_comment(comment) -> Optional[str]:
    match = REGEX.match(comment.body)
    if not match:
        return None
    else:
        return match.group(1)
