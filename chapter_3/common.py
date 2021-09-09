#!/usr/bin/env python
# -*- encoding:UTF-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any, TypeVar


class Comparable(metaclass=ABCMeta):
    """Comparable class for type hint
    """
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        """To get current element is less than `other` or not.

        Args:
            other (Any): other element to compare,
                         type of `other` must match current element

        Returns:
            bool: True if current element < `other` else False
        """
        pass


CT = TypeVar('CT', bound=Comparable)
