from typing import Optional
from loguru import logger
from pathlib import Path
import warnings
import logging
import os

from components.model.dataset import Dataset
from components.utils.config import Config
from components.cheat.kernel import Kernel
from components.cheat.driver import Driver
from components.model.model import Model


def initialise():
    os.system("cls||clear")
    warnings.filterwarnings("ignore", category=FutureWarning, module="albumentations")
    logging.getLogger("yolov5").setLevel(logging.WARNING)


class Scaffold:
    @staticmethod
    @logger.catch
    def init():
        """
        Usage: python main.py init

        Create defaut files and initialise config
        """

        initialise()
        Config.gather()

    @staticmethod
    @logger.catch
    def labelise(
        dataset: str,
        pt_file: str = "../assets/best.pt",
        clean: Optional[bool] = True,
        label: Optional[bool] = True,
        augment: Optional[bool] = False,
        num_variations: Optional[int] = 1,
        conf_threshold: Optional[float] = 0.75,
    ):
        """
        Build YOLOv5 dataset using collected data

        Usage: python main.py labelise --dataset=path/to/dataset
        or: python main.py labelise --dataset=dataset_test --label --clean --augment --num_variations=5 --conf_threshold=0.50

        Args:
            dataset (str): Path to the YOLOv5 dataset folder.
            pt_file (str): best.pt path.
            clean (bool, optional): Clean the dataset by removing orphaned label files. Defaults to False.
            augment (bool, optional): Apply data augmentation (blur, noise, flip) to the images. Defaults to False.
            num_variations (int, optional): Number of variations to create for each image. Defaults to 1.
            conf_threshold (float, optional): Minimum confidence threshold for bounding boxes. Defaults to 0.70.
        """

        initialise()

        model = Model(
            path=Path(pt_file),
        )

        data = Dataset(
            path=Path(dataset),
            model=model,
        )

        if label:
            data.labelise(
                augment=augment,
                conf_threshold=conf_threshold,
                num_variations=num_variations,
            )

        if clean:
            data.clean()
            return

    @staticmethod
    @logger.catch
    def aimbot(
        dataset: str,
        pt_file: str = "../assets/best.pt",
        confidence: float = 0.70,
    ):
        """
        Start the aimbot

        Usage: python main.py aimbot --dataset=path/to/dataset --confidence=0.75

        Args:
            dataset (str): Path to the YOLOv5 dataset folder.
            pt_file (str): best.pt path.
        """

        initialise()

        driver = Driver()
        config = Config()

        data = Dataset(
            path=Path(dataset),
            model=None,
        )

        _, output_labels_path, _ = data.check()
        data.model = Model(
            path=Path(pt_file),
            output_labels_path=output_labels_path,
            conf_threshold=confidence,
        )

        Kernel(
            model_instance=data.model,
            dataset_instance=data,
            config_instance=config,
            driver_instance=driver,
        ).run()
