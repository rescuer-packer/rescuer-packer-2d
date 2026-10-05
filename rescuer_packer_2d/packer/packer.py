from typing import List

from rescuer_geocore_2d.cropped_polygon.cropped_polygon import CroppedPolygon
from rescuer_task.task import RescuerTask

from rescuer_packer_2d.builder.intersection_checks_builder import build_intersection_checks
from rescuer_packer_2d.builder.rescuer_task_builder import RescuerTaskBuilder
from rescuer_packer_2d.containers.interface import Container


def build_rescuer_task(polys: List[List[CroppedPolygon]], step: float, container: Container) -> tuple[
    RescuerTask, List[tuple[int, int, int]]]:
    builder = RescuerTaskBuilder(polys, step)
    build_intersection_checks(builder)
    container.build(builder)
    return builder.task, builder.key

