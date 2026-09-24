from enum import Enum

from rescuer_packer_2d.builder.rescuer_task_builder import RescuerTaskBuilder
from rescuer_packer_2d.containers.interface import Container

class RectangleContainerTaskType(Enum):
    FIXED_HEIGHT = 1
    FIXED_WIDTH = 2
    ASPECT_RATIO = 3

class RectangleContainer(Container):
    def __init__(self, task_type: RectangleContainerTaskType, value: float, max_score: float | None ):
        self.task_type = task_type
        self.value = value
        self.max_score = max_score


    def build(self, builder: RescuerTaskBuilder):
        if self.max_score is not None:
            builder.task.cont_bounds[0][1] = self.max_score

        min_x, min_y, max_x, max_y = _build_min_max_x_y(builder)
        # TODO
        if self.task_type == RectangleContainerTaskType.FIXED_HEIGHT:
            return

        if self.task_type == RectangleContainerTaskType.FIXED_WIDTH:
            return

        if self.task_type == RectangleContainerTaskType.ASPECT_RATIO:
            return

        raise ValueError("Unknown task type")




def _build_min_max_x_y(builder: RescuerTaskBuilder) -> tuple[int, int, int, int]:
    # TODO
    pass