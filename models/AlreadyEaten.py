from models.Tastebuds import Tastebuds

class AlreadyEaten(Tastebuds):
  def __init__(self):
    super().__init__()
    self.__alreadyVisited = set()

  def is_tasty(self, page_url: str, **kwargs) -> bool:
    page_url = page_url.lower()

    if page_url in self.__alreadyVisited:
      return False
    else:
      self.__alreadyVisited.add(page_url)
      return True