from typing import List
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class TextSelectorStrategy(ABC):
  @abstractmethod
  def get_text(self, soup: BeautifulSoup) -> str:
    pass