from abc import ABC, abstractmethod

class DepthObserver(ABC):
  @abstractmethod
  def get_current_depth(self) -> int:
    pass
  
  @abstractmethod
  def update_depth(self, amount: int) -> None:
    pass
