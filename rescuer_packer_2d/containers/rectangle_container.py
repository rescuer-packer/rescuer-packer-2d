from enum import Enum
from typing import List

from rescuer_geocore_2d.cropped_polygon.cropped_polygon import CroppedPolygon
from rescuer_task.task import Inequality

from rescuer_packer_2d.builder.rescuer_task_builder import RescuerTaskBuilder
from rescuer_packer_2d.containers.interface import Container


class RectangleContainerTaskType(Enum):
    FIXED_HEIGHT = 1
    FIXED_WIDTH = 2
    ASPECT_RATIO = 3


class RectangleContainer(Container):
    def __init__(self, task_type: RectangleContainerTaskType, value: float, max_score: float | None):
        self.task_type = task_type
        self.value = value
        self.max_score = max_score

    def build(self, builder: RescuerTaskBuilder):
        if self.max_score is not None:
            builder.task.cont_bounds[0][1] = self.max_score

        min_x, min_y, max_x, max_y = _build_min_max_x_y(builder)
        if self.task_type == RectangleContainerTaskType.FIXED_HEIGHT:
            builder.task.inequalities.append(Inequality(
                {max_x: 1, min_x: -1, 0: -1},
                0, 0, []
            ))
            builder.task.inequalities.append(Inequality(
                {max_y: 1, min_y: -1},
                -self.value, 0, []
            ))
            return

        if self.task_type == RectangleContainerTaskType.FIXED_WIDTH:
            builder.task.inequalities.append(Inequality(
                {max_y: 1, min_y: -1, 0: -1},
                0, 0, []
            ))
            builder.task.inequalities.append(Inequality(
                {max_x: 1, min_x: -1},
                -self.value, 0, []
            ))
            return
        if self.task_type == RectangleContainerTaskType.ASPECT_RATIO:
            builder.task.inequalities.append(Inequality(
                {max_x: 1, min_x: -1, 0: -1},
                0, 0, []
            ))
            builder.task.inequalities.append(Inequality(
                {max_y: 1, min_y: -1, 0: -self.value},
                0, 0, []
            ))
            return

        raise ValueError("Unknown task type")


def _build_min_max_x_y(builder: RescuerTaskBuilder) -> tuple[int, int, int, int]:
    min_x_pos = len(builder.task.cont_bounds)
    builder.task.cont_bounds.append(
        [
            _bound(builder.polys, min, min, 0) - builder.step,
            _bound(builder.polys, min, max, 0) + builder.step,
        ]
    )
    max_x_pos = len(builder.task.cont_bounds)
    builder.task.cont_bounds.append(
        [
            _bound(builder.polys, max, min, 2) - builder.step,
            _bound(builder.polys, max, max, 2) + builder.step,
        ]
    )
    min_y_pos = len(builder.task.cont_bounds)
    builder.task.cont_bounds.append(
        [
            _bound(builder.polys, min, min, 1) - builder.step,
            _bound(builder.polys, min, max, 1) + builder.step,
        ]
    )
    max_y_pos = len(builder.task.cont_bounds)
    builder.task.cont_bounds.append(
        [
            _bound(builder.polys, max, min, 3) - builder.step,
            _bound(builder.polys, max, max, 3) + builder.step,
        ]
    )

    cb = builder.task.cont_bounds
    for i in range(len(builder.polys)):
        ls = builder.polys[i]
        m = len(ls)
        for j in range(m):
            rs = []
            if builder.key[i][2] != -1:
                rs.append(builder.key[i][2] + j)

            #  min_x <= bounds[i][j][0] + x[i]
            #  min_x - x[i] - bounds[i][j][0] <= 0
            up_val = cb[min_x_pos][1] + builder.step - ls[j].convex.bounds[0]
            if up_val > 0:
                builder.task.inequalities.append(
                    Inequality(
                        {
                            min_x_pos: 1,
                            builder.x[i]: -1
                        },
                        - ls[j].convex.bounds[0], up_val, rs
                    )
                )

            #  min_y <= bounds[i][j][1] + y[i]
            #  min_y - y[i] - bounds[i][j][1] <= 0
            up_val = cb[min_y_pos][1] + builder.step - ls[j].convex.bounds[1]
            if up_val > 0:
                builder.task.inequalities.append(
                    Inequality(
                        {
                            min_y_pos: 1,
                            builder.y[i]: -1
                        },
                        - ls[j].convex.bounds[1], up_val, rs
                    )
                )
            #  max_x >= bounds[i][j][2] + x[i]
            #  bounds[i][j][2] + x[i] - max_x <= 0
            up_val = builder.step + ls[j].convex.bounds[2] - cb[max_x_pos][0]
            if up_val > 0:
                builder.task.inequalities.append(
                    Inequality(
                        {
                            max_x_pos: -1,
                            builder.x[i]: 1
                        },
                        ls[j].convex.bounds[2], up_val, rs
                    )
                )
                #  max_y >= bounds[i][j][3] + y[i]
                #  bounds[i][j][3] + y[i] - max_y <= 0
                up_val = builder.step + ls[j].convex.bounds[3] - cb[max_y_pos][0]
                if up_val > 0:
                    builder.task.inequalities.append(
                        Inequality(
                            {
                                max_y_pos: -1,
                                builder.y[i]: 1
                            },
                            ls[j].convex.bounds[3], up_val, rs
                        )
                    )

    return min_x_pos, min_y_pos, max_x_pos, max_y_pos


def _bound(t: List[List[CroppedPolygon]], f, g, i) -> float:
    return f(_in_poly(elem, g, i) for elem in t)


def _in_poly(t: List[CroppedPolygon], f, i) -> float:
    return f(elem.convex.bounds[i] for elem in t)
