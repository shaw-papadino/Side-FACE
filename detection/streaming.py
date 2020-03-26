from abc import ABCMeta, abstractmethod

class Streaming(metaclass=ABCMeta):

    @abstractmethod
    def stream(self):
        pass
