from typing import Optional
from loguru import logger
from pathlib import Path
import warnings
import os

from components.model.dataset import Dataset
from components.utils.config import Config
from components.model.model import Model


def initialise():
    os.system("cls||clear")
    warnings.filterwarnings("ignore", category=DeprecationWarning)


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
        clean: Optional[bool] = False,
        augment: Optional[bool] = False,
        num_variations: Optional[int] = 1,
        conf_threshold: Optional[float] = 0.70,
    ):
        """
        Build YOLOv5 dataset using collected data

        Usage: python main.py labelise --dataset=path/to/dataset
        or: python main.py labelise --dataset=path/to/dataset
        or: python main.py labelise --dataset=dataset_test --augment --num_variations=5 --conf_threshold=0.50

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
            path=Path(pt_file).resolve(),
        )

        data = Dataset(
            path=Path(dataset),
            model=model,
        )

        data.labelise(
            augment=augment,
            conf_threshold=conf_threshold,
            num_variations=num_variations,
        )
