import albumentations as A
from loguru import logger
from pathlib import Path
from tqdm import tqdm
import time


class Dataset:
    def __init__(self, path: Path) -> None:
        self.path = path

    @logger.catch
    def install(self) -> None:
        images_path = self.path / "images"
        images_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        labels_path = self.path / "labels"
        labels_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    @logger.catch
    def clean(self) -> None:
        images_folder = self.path / "images"
        labels_folder = self.path / "labels"

        if not Path.exists(image_file) or not Path.exists(label_files):
            self.install()
            logger.info(
                f"Image or label files do not exist. Dataset initialized in {self.path.absolute()}."
            )

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
