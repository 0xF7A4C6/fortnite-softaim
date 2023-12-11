from threading import Thread
from loguru import logger
from math import hypot
import numpy as np
import ctypes
import mss

from components.cheat.algorithms import Algorithms
from components.model.dataset import Dataset
from components.utils.config import Config
from components.cheat.driver import Driver
from components.model.model import Model


class Kernel(Thread):
    def __init__(
        self,
        model_instance: Model,
        dataset_instance: Dataset,
        config_instance: Config,
        driver_instance: Driver,
    ) -> None:
        """
        Initialize the Kernel.

        Args:
                model_instance (Model): An instance of the Model class.
                dataset_instance (Dataset): An instance of the Dataset class.
                config_instance (Config): An instance of the Config class.
        """

        self._driver = driver_instance
        self._model = model_instance
        self._config = config_instance.gather()
        self._dataset = dataset_instance

        # states
        self._runing = True

        self._screensize = {
            "X": ctypes.windll.user32.GetSystemMetrics(0),
            "Y": ctypes.windll.user32.GetSystemMetrics(1),
        }

        self._screen_x = int(self._screensize["X"] / 2)
        self._screen_y = int(self._screensize["Y"] / 2)

        self._screen = mss.mss()

        Thread.__init__(self)
        logger.info("Kernel initialized")

    def __is_target_locked(self, threshold: int, x: int, y: int) -> None:
        some_scaling_factor = 0.5
        ref_point = (self._screen_x, self._screen_y)

        distance = hypot(x - ref_point[0], y - ref_point[1])
        scale_threshold = threshold + int(distance * some_scaling_factor)

        if scale_threshold > 15:
            scale_threshold = 15

        return (
            True
            if ref_point[0] - scale_threshold <= x <= ref_point[0] + scale_threshold
            and ref_point[1] - scale_threshold <= y <= ref_point[1] + scale_threshold
            else False
        )

    @logger.catch
    def run(self):
        fov = 350

        detection_box = {
            "left": int((self._screensize["X"] / 2) - (fov // 2)),
            "top": int((self._screensize["Y"] / 2) - (fov // 2)),
            "width": fov,
            "height": fov,
        }

        logger.debug(detection_box)

        # temp dpg
        triggerbot_enabled = False
        aimbot_enabled = True
        aimbot_pos = 20
        threshold_trigger = 7

        while self._runing:
            frame = np.array(self._screen.grab(detection_box))

            result, _, threshold, _ = self._model.evaluate(frame)
            if len(result) == 0:
                continue

            least_crosshair_dist = False
            closest_detection = False

            for *box, conf, _ in result:
                if conf < threshold:
                    logger.debug(f"bellow threshold {conf * 100}")
                    continue

                (
                    crosshair_dist,
                    head_x,
                    head_y,
                    own_player,
                    x1y1,
                    x2y2,
                ) = Algorithms.box_to_pos(
                    conf=conf,
                    box=box,
                    fov=fov,
                    aimbot_pos=aimbot_pos,
                )

                if not crosshair_dist:
                    least_crosshair_dist = crosshair_dist

                if crosshair_dist <= least_crosshair_dist and not own_player:
                    least_crosshair_dist = crosshair_dist
                    closest_detection = {
                        "x1y1": x1y1,
                        "x2y2": x2y2,
                        "relative_head_X": head_x,
                        "relative_head_Y": head_y,
                        "conf": conf,
                    }

            if not closest_detection:
                continue

            absolute_head_X, absolute_head_Y = (
                closest_detection["relative_head_X"] + detection_box["left"],
                closest_detection["relative_head_Y"] + detection_box["top"],
            )

            locked = self.__is_target_locked(
                threshold=threshold_trigger,
                x=absolute_head_X,
                y=absolute_head_Y,
            )

            if triggerbot_enabled and locked:
                self._driver.left_click()

            if aimbot_enabled and not locked:
                self._driver.move_crosshair(
                    scale=self._config["sensitivity"].get("targeting_scale"),
                    target_x=absolute_head_X,
                    target_y=absolute_head_Y,
                )
