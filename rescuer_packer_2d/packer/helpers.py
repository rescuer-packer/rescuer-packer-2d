import random
from typing import List

from rescuer_geocore_2d.cropped_polygon.cropped_polygon import CroppedPolygonBuilder, CroppedPolygon


def build_mutation(position: List[tuple[float, float, float]],
                   mut_prob: float,
                   angle_mut: float,
                   count: int) -> List[List[tuple[float, float, float]]]:
    ans = []
    for t in position:
        ls = [t]
        if random.uniform(0, 1) < mut_prob:
            for _ in range(count):
                ls.append((t[0], t[1], t[2] + random.uniform(-angle_mut, angle_mut)))
        ans.append(ls)
    return ans


def build_task_polys(task_it: List[List[tuple[float, float, float]]],
                     builders: List[CroppedPolygonBuilder]) -> List[List[CroppedPolygon]]:
    ans = []
    for l in range(len(task_it)):
        ls = []
        builder = builders[l]
        for i in task_it[l]:
            ls.append(builder.build(i[0], i[1], i[2]))
        ans.append(ls)
    return ans


def decode_by_key(
        task_it: List[List[tuple[float, float, float]]],
        key: List[tuple[int, int, int]],
        conts: List[float],
        rescuers: List[bool]
) -> List[tuple[float, float, float]]:
    ans = []
    for i in range(len(task_it)):
        it = None
        if key[i][2] == -1:
            it = task_it[i][0]
        else:
            for j in range(len(task_it[i])):
                if not rescuers[j + key[i][2]]:
                    it = task_it[i][j]
                    break
        if it is None:
            raise ValueError("rescuers error")
        ans.append((it[0] + conts[key[i][0]], it[1] + conts[key[i][1]], it[2]))
    return ans
