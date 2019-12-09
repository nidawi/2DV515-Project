from abc import ABC, abstractmethod

class DepthObserver(ABC):
  @abstractmethod
  def _get_current_depth(self) -> int:
    pass
  
  @abstractmethod
  def _update_depth(self, amount: int) -> None:
    pass
