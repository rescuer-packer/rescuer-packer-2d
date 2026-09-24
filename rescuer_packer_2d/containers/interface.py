from abc import ABC, abstractmethod

from rescuer_packer_2d.builder.rescuer_task_builder import RescuerTaskBuilder


class Container(ABC):
    @abstractmethod
    def build(self, builder: RescuerTaskBuilder):
        pass