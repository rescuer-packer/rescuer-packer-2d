from typing import List

from rescuer_geocore_2d.cropped_polygon.cropped_polygon import CroppedPolygon
from rescuer_task.task import RescuerTask


class RescuerTaskBuilder:
    def __init__(self, polys: List[List[CroppedPolygon]], step: float):
        self.polys = polys
        self.step = step
        self.task = RescuerTask()
        self.task.cont_bounds.append([0, None])
        self.x = []
        self.y = []
        self.key = []
        self.rcount = 0
        for i in range(len(polys)):
            self.x.append(1 + 2*i)
            self.y.append(2 + 2*i)
            self.task.cont_bounds.append([-self.step, self.step])
            t = len(polys[i])
            if t > 1:
                self.task.rescuer_groups.append(t)
                self.key.append((1+2*i, 2+2*i, self.rcount))
                self.rcount += t
            else:
                self.key.append((1+2*i, 2+2*i, -1))


