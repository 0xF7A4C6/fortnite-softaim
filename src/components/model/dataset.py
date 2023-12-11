import albumentations as A
from loguru import logger
from pathlib import Path
from tqdm import tqdm
from enum import Enum
import time
import glob
import cv2

from components.model.model import Model


class Dataset:
    def __init__(self, path: Path, model: Model) -> None:
        self.path = path
        self.model = model

    @logger.catch
    def __install(self) -> None:
        """
        Create dataset base folders tree
        """

        for folders in (
            "images",
            "labels",
            "input",
        ):
            folder_path = self.path / folders

            if folder_path.exists():
                continue

            folder_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            logger.debug(f"created folder: {folder_path.absolute()}")

        logger.info(f"Dataset initialized in {self.path.absolute()}.")

    @logger.catch
    def check(self) -> tuple[Path, Path, Path]:
        """
        Check Dataset folder integrity, create one if not found.
        """

        images_folder = self.path / "images"
        labels_folder = self.path / "labels"
        input_folder = self.path / "input"

        if (
            not images_folder.exists()
            or not labels_folder.exists()
            or not input_folder.exists()
        ):
            logger.info(
                "Dataset folders not found. Initializing dataset installation..."
            )
            self.__install()

        logger.info(
            f"Dataset found! ({images_folder}, {labels_folder}, {input_folder})"
        )
        return (images_folder, labels_folder, input_folder)

    @logger.catch
    def clean(self) -> None:
        """
        Clean the dataset by removing orphaned label files.
        """

        (images_folder, labels_folder, _) = self.check()

        image_files = set([img.stem for img in images_folder.glob("*")])
        label_files = set([label.stem for label in labels_folder.glob("*")])

        deleted_labels, deleted_images = 0, 0
        st = time.time()

        for image_file in tqdm(image_files, desc="Cleaning Dataset (Images)"):
            label_path = labels_folder / (image_file + ".txt")

            if not label_path.exists():
                (images_folder / (image_file + ".jpg")).unlink()
                deleted_images += 1

        for label_file in tqdm(label_files, desc="Cleaning Dataset (Labels)"):
            image_path = images_folder / (label_file + ".jpg")

            if not image_path.exists():
                (labels_folder / (label_file + ".txt")).unlink()
                deleted_labels += 1

        logger.info(
            f"Removed {deleted_labels} label files and {deleted_images} images in {time.time()-st}"
        )

    @logger.catch
    def labelise(
        self,
        augment: bool = False,
        num_variations: int = 1,
        conf_threshold: float = 0.75,
    ) -> None:
        (output_images_path, output_labels_path, input_folder) = self.check()

        self.model.output_labels_path = output_labels_path
        self.model.conf_threshold = conf_threshold

        image_paths = glob.glob(str(input_folder / "*.jpg")) + glob.glob(
            str(input_folder / "*.png")
        )

        # todo: add as params?
        variation_chance = 0.3

        transform = A.Compose(
            [
                A.Blur(
                    blur_limit=(3, 7),
                    p=variation_chance,
                ),
                A.GaussNoise(
                    var_limit=(10, 50),
                    p=variation_chance,
                ),
                A.HorizontalFlip(
                    p=variation_chance,
                ),
                A.RandomBrightnessContrast(
                    p=variation_chance,
                ),
                A.RandomGamma(
                    p=0.3,
                ),
                A.HueSaturationValue(
                    hue_shift_limit=20,
                    sat_shift_limit=30,
                    val_shift_limit=20,
                    p=variation_chance,
                ),
                A.RandomBrightness(
                    limit=0.2,
                    p=variation_chance,
                ),
            ]
        )

        for image_path in tqdm(image_paths, desc="Processing Images"):
            img = cv2.imread(image_path)

            # eval original image
            self.model.evaluate(img)

            if augment:
                for _ in range(num_variations):
                    augmented = transform(image=img)
                    augmented_img_rgb = augmented["image"]

                    self.model.evaluate(augmented_img_rgb)
