from loguru import logger
from pathlib import Path
import numpy as np
import torch
import cv2

from components.model.labeler import Labeler


class Model:
    def __init__(
        self, path: Path, output_labels_path: Path = None, conf_threshold: float = 0.75
    ) -> None:
        if not torch.cuda.is_available():
            raise SystemExit(
                "Error: CUDA is not available. The model requires a GPU with CUDA support."
            )

        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom", path=path.resolve(), verbose=False
        )

        self._conf_threshold = conf_threshold
        self._output_labels_path = output_labels_path

        logger.debug("Model initialized.")

    @property
    def conf_threshold(self) -> float:
        return self._conf_threshold

    @conf_threshold.setter
    def conf_threshold(self, value: float) -> None:
        if not 0 <= value <= 1:
            raise ValueError(
                "Invalid value for conf_threshold. It must be between 0 and 1."
            )
        self._conf_threshold = value

    @property
    def output_labels_path(self) -> float:
        return self._output_labels_path

    @output_labels_path.setter
    def output_labels_path(self, path: Path) -> None:
        self._output_labels_path = path

    def __preprocess(self, image: np.ndarray) -> np.ndarray:
        """
        Converts the input image to grayscale.
        """

        return cv2.cvtColor(np.copy((image)), cv2.COLOR_BGR2GRAY)

    @Labeler()
    def evaluate(
        self, image: np.ndarray
    ) -> tuple[torch.Tensor, np.ndarray, float, Path]:
        """
        Performs image evaluation using the YOLOv5 model on the preprocessed image.

        Return: `tuple[ai_result, img_array, threshold, output_labels_path]`
        """

        return (
            self.model(
                self.__preprocess(
                    image=image,
                )
            ).xyxy[0],
            image,
            self._conf_threshold,
            self._output_labels_path,
        )
