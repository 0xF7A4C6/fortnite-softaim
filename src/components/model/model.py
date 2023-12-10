from loguru import logger
import numpy as np
import torch
import cv2

from .labeler import Labeler


class Model:
    def __init__(self, path: str) -> None:
        if not torch.cuda.is_available():
            raise SystemExit(
                "Error: CUDA is not available. The model requires a GPU with CUDA support."
            )

        self.model = torch.hub.load("ultralytics/yolov5", "custom", path=path)
        logger.debug("Model initialized.")

    def __preprocess(self, image: np.ndarray) -> np.ndarray:
        """
        Converts the input image to grayscale.
        """

        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @Labeler
    def evaluate(self, image: np.ndarray) -> torch.Tensor:
        """
        Performs image evaluation using the YOLOv5 model on the preprocessed image.
        """

        return self.model(
            self.__preprocess(
                image=image,
            )
        ).xyxy[0]
