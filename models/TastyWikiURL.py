import re
from models.Tastebuds import Tastebuds

REGEX = "^/wiki/\w+$"

class TastyWikiURL(Tastebuds):
  def is_tasty(self, page_url: str, **kwargs) -> bool:
    return re.search(REGEX, page_url)