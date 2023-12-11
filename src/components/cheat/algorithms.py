import math


class Algorithms:
    @staticmethod
    def bezier_cubic(
        t: float,
        p0: float,
        p1: float,
        p2: float,
        p3: float,
    ):
        """
        Compute the cubic Bezier interpolation at parameter t.

        Args:
            t (float): Parameter value between 0 and 1.
            p0 (float): Control point P0.
            p1 (float): Control point P1.
            p2 (float): Control point P2.
            p3 (float): Control point P3.

        Returns:
            float: Interpolated value.
        """

        """
        P0 ---------- P1
           \
            \
             \
              \
               \
                P2 ---------- P3
        """

        return (
            (1 - t) ** 3 * p0
            + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t**2 * p2
            + t**3 * p3
        )

    @staticmethod
    def box_to_pos(
        conf,
        box: list,
        fov: int,
        aimbot_pos: int,
    ) -> tuple[dict, float]:
        x1y1 = [int(x.item()) for x in box[:2]]
        x2y2 = [int(x.item()) for x in box[2:]]

        x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
        height = y2 - y1

        relative_head_X, relative_head_Y = int((x1 + x2) / 2), int(
            (y1 + y2) / 2 - height / aimbot_pos
        )

        own_player = x1 < 15 or (x1 < fov / 5 and y2 > fov / 1.2)

        crosshair_dist = math.dist(
            (relative_head_X, relative_head_Y),
            (fov / 2, fov / 2),
        )

        return (
            crosshair_dist,
            relative_head_X,
            relative_head_Y,
            own_player,
            x1y1,
            x2y2,
        )

    @staticmethod
    def interpolate_coordinates_from_center_blatant(absolute_coordinates, scale):
        pixel_increment = 2

        diff_x = (absolute_coordinates[0] - 960) * scale / pixel_increment
        diff_y = (absolute_coordinates[1] - 540) * scale / pixel_increment

        length = int(math.dist((0, 0), (diff_x, diff_y)))

        if length == 0:
            return

        unit_x = (diff_x / length) * pixel_increment
        unit_y = (diff_y / length) * pixel_increment

        x = y = sum_x = sum_y = 0
        for k in range(0, length):
            sum_x += x
            sum_y += y

            x, y = round(unit_x * k - sum_x), round(unit_y * k - sum_y)
            yield x, y
