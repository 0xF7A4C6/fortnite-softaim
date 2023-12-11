from threading import Thread
from functools import wraps
from loguru import logger
from torch import Tensor
from pathlib import Path
import numpy as np
import uuid
import cv2

from components.model.dataset import DatasetFolders


class Labeler:
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            Thread(
                target=self.process,
                args=(result,),
                daemon=True,
            ).start()

            return result

        return wrapper

    @logger.catch
    def process(self, input: tuple[Tensor, np.ndarray, float, Path]) -> None:
        """
        Process a image after being recognized.

        params: input[ai_result, img_array, treshold, output_labels_path]
        """

        detections = input[0].cpu().numpy()
        valid_detections = [det for det in detections if det[4] > input[2]]

        if valid_detections:
            label_content = ""
            for det in valid_detections:
                _, _, _, _, conf, cls = det
                label_content += f"{int(cls)} {((det[0]+det[2])/2)/input[1].shape[1]} {((det[1]+det[3])/2)/input[1].shape[0]} {abs(det[2]-det[0])/input[1].shape[1]} {abs(det[3]-det[1])/input[1].shape[0]}\n"

            label_file_path = input[3] / (f"{uuid.uuid4()}.txt")

            with open(label_file_path, "w") as label_file:
                label_file.write(label_content)

            img_path = (
                str(label_file_path.absolute()).replace(
                    DatasetFolders.LabelFolder, DatasetFolders.ImageFolder
                )
            ).replace("txt", "jpg")

            cv2.imwrite(img_path, input[1])
