"""
識別するクラス
"""
from abc import ABCMeta, abstractmethod

class Recognizer(metaclass=ABCMeta):

    @abstractmethod
    def recognize(self,img):
        pass
