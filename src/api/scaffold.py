from loguru import logger
from typing import Optional
from components.utils.config import Config


class Scaffold:
    @staticmethod
    @logger.catch
    def init():
        """
        Usage: python main.py init

        Create defaut files and initialise config
        """

        Config.gather()

    @staticmethod
    @logger.catch
    def labelise(
        dataset: str,
        clean: Optional[bool] = False,
        augment: Optional[bool] = False,
        num_variations: Optional[int] = 1,
        conf_threshold: Optional[float] = 0.70,
    ):
        """
        Build YOLOv5 dataset using collected data

        Usage: python main.py labelise --dataset=path/to/dataset
        or: python main.py labelise --dataset=path/to/dataset
        or: python main.py labelise --dataset=path/to/dataset --augment

        Args:
            dataset (str): Path to the YOLOv5 dataset folder.
            clean (bool, optional): Clean the dataset by removing orphaned label files. Defaults to False.
            augment (bool, optional): Apply data augmentation (blur, noise, flip) to the images. Defaults to False.
            num_variations (int, optional): Number of variations to create for each image. Defaults to 1.
            conf_threshold (float, optional): Minimum confidence threshold for bounding boxes. Defaults to 0.70.
        """

        __config__ = Config.gather()

        print(dataset)