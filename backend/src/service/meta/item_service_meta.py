
from abc import ABC, abstractmethod

from src.schemas.item import Produto

class ItemServiceMeta(ABC):

    @abstractmethod
    def get_item(self, item_id: str) -> Produto:
        """Get item by id method definition"""
        pass