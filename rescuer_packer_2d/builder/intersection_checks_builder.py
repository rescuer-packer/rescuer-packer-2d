from rescuer_geocore_2d.intersection_candidates.moved_polygons_intersection import moved_polygons_intersection
from rescuer_geocore_2d.separating_line.tools import by_all_borders
from rescuer_task.task import Inequality
from shapely import Polygon

from rescuer_packer_2d.builder.rescuer_task_builder import RescuerTaskBuilder





def build_intersection_checks(builder: RescuerTaskBuilder):
    linearize_polygons = []
    linearize_numbers = []
    for i in range(len(builder.polys)):
        m = len(builder.polys[i])
        for j in range(m):
            n = len(builder.polys[i][j].crops)
            for k in range(n):
                linearize_polygons.append((builder.polys[i][j].crops[k], i))
                linearize_numbers.append((k, j))

    blocks = {}

    def callback(pos1, pos2):
        #polygon
        p1 = linearize_polygons[pos1][1]
        p2 = linearize_polygons[pos2][1]

        #crop
        cr1 = linearize_numbers[pos1][0]
        cr2 = linearize_numbers[pos2][0]

        #rotation
        r1 = linearize_numbers[pos1][1]
        r2 = linearize_numbers[pos2][1]

        if p1 == p2:
            return
        constraints = _build_pair_constraints(linearize_polygons[pos1][0], linearize_polygons[pos2][0], builder.step)
        if len(constraints) == 0:
            return

        outer_key = (p1,cr1, p2, cr2)
        if outer_key not in blocks:
            blocks[outer_key] = {}
        inner = blocks[outer_key]
        inner_key = (r1, r2)
        inner[inner_key] = constraints

    moved_polygons_intersection(linearize_polygons, builder.step, callback)

    for k, v in blocks.items():
        p1 = k[0]
        p2 = k[2]

        cr1 = k[1]
        cr2 = k[3]

        v_complex = {}
        max_len = 0
        for k1, v1 in v.items():
            if len(v1) == 1 and v1[0] is None:
                rls = []
                if builder.key[p1][2] != -1:
                    rls.append(builder.key[p1][2] + k1[0])
                if builder.key[p2][2] != -1:
                    rls.append(builder.key[p2][2] + k1[1])
                if len(rls) == 0:
                    raise ValueError("Fast exit - polygons must intersects")
                builder.task.inequalities.append(
                    Inequality({}, 1,1, rls)
                )
            else:
                v_complex[k1] = v1
                if len(v1) > max_len:
                    max_len = len(v1)


        for k1, v1 in v_complex.items():
            while len(v1) < max_len:
                v1.append(None)

        if max_len == 1:
            pass

        if max_len > 1:
            pass



def _build_pair_constraints(poly1: Polygon, poly2: Polygon, step: float):
    unbounded_constraints = by_all_borders(poly1, poly2)
    has_unsatisfied = False

    ans = []
    for cr in unbounded_constraints:
        mod = abs(cr.kx) + abs(cr.ky)
        min_val = cr.c - 2*step * mod
        if min_val > 0:
            has_unsatisfied = True
            continue
        max_val = cr.c + 2*step * mod
        if max_val <= 0:
            return []
        ans.append((cr.kx, cr.ky, cr.c, max_val))

    if len(ans) == 0 and has_unsatisfied:
        return [None]
    return ans