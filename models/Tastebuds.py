import asyncio
from abc import ABC, abstractmethod

class Tastebuds(ABC):
  """
    Represents a CrawlerSnake's tastebuds. Applies a restriction to what urls a CrawlerSnake will eat (crawl).

    This class can be extended to implement specific tastes.

    Provides the following interface:
    >>> def is_tasty(page_url: str, **kwargs) -> bool: # return true if the given url tastes good and could be crawled.
  """
  def __init__(self):
    super().__init__()

  @abstractmethod
  def is_tasty(self, page_url: str, **kwargs) -> bool:
    pass