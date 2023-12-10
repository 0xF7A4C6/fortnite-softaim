from loguru import logger
from pathlib import Path
import numpy as np
import torch
import cv2

from .labeler import Labeler


class Model:
    def __init__(
        self, path: str, output_labels_path: Path = None, conf_threshold: float = 0.75
    ) -> None:
        if not torch.cuda.is_available():
            raise SystemExit(
                "Error: CUDA is not available. The model requires a GPU with CUDA support."
            )

        self.model = torch.hub.load("ultralytics/yolov5", "custom", path=path)
        self.conf_threshold = conf_threshold
        self.output_labels_path = output_labels_path

        logger.debug("Model initialized.")

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
        """

        return (
            self.model(
                self.__preprocess(
                    image=image,
                )
            ).xyxy[0],
            image,
            self.conf_threshold,
            self.output_labels_path,
        )
