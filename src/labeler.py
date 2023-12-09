import argparse, cv2, torch, glob, os, time, warnings
import albumentations as A
from pathlib import Path
from tqdm import tqdm


def load_yolov5_model():
    model = torch.hub.load(
        "ultralytics/yolov5",
        "custom",
        path="../assets/best.pt",
        force_reload=True,
    )
    return model


def clean_dataset(dataset_path: str):
    dataset_path = Path(dataset_path)

    images_folder = dataset_path / "images"
    labels_folder = dataset_path / "labels"

    image_files = set([img.stem for img in images_folder.glob("*")])
    label_files = set([label.stem for label in labels_folder.glob("*")])

    deleted_labels = 0
    deleted_images = 0
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

    print(
        f"Removed {deleted_labels} label files and {deleted_images} images in {time.time()-st}"
    )


def evaluate_model(model, img_rgb):
    return model(img_rgb).xyxy[0][:, 4].sum()


def generate_yolo_labels(
    model,
    images_folder: str,
    output_dataset_path: Path,
    conf_threshold: float = 0.70,
    augment: bool = False,
    num_variations: int = 1,
):
    images_folder = Path(images_folder)
    output_images_path = output_dataset_path / "images"
    output_labels_path = output_dataset_path / "labels"

    output_images_path.mkdir(
        parents=True,
        exist_ok=True,
    )
    output_labels_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    image_paths = glob.glob(str(images_folder / "*.jpg")) + glob.glob(
        str(images_folder / "*.png")
    )

    transform = A.Compose(
        [
            A.Blur(
                blur_limit=(
                    3,
                    7,
                ),
                p=0.2,
            ),
            A.GaussNoise(
                var_limit=(
                    10,
                    50,
                ),
                p=0.2,
            ),
            A.HorizontalFlip(
                p=0.2,
            ),
            A.Rotate(
                limit=(
                    -45,
                    45,
                ),
                p=0.2,
            ),
            A.RandomBrightnessContrast(
                p=0.2,
            ),
            A.RandomGamma(
                p=0.2,
            ),
            A.HueSaturationValue(
                hue_shift_limit=20,
                sat_shift_limit=30,
                val_shift_limit=20,
                p=0.2,
            ),
            A.RandomBrightness(
                limit=0.2,
                p=0.2,
            ),
        ]
    )

    for image_path in tqdm(image_paths, desc="Processing Images"):
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        original_image_path = output_images_path / (Path(image_path).name)
        cv2.imwrite(str(original_image_path), img_rgb)

        original_evaluation = evaluate_model(model, img_rgb)

        for variation in range(num_variations):
            if augment:
                augmented = transform(image=img_rgb)
                augmented_img_rgb = augmented["image"]

                augmented_image_path = output_images_path / (
                    f"augmented_{variation}_{Path(image_path).name}"
                )

                cv2.imwrite(str(augmented_image_path), augmented_img_rgb)
                variation_evaluation = evaluate_model(model, augmented_img_rgb)

                if variation_evaluation > original_evaluation:
                    img_rgb = augmented_img_rgb
                else:
                    (augmented_image_path).unlink()

            results = model(img_rgb)
            detections = results.xyxy[0].cpu().numpy()

            valid_detections = [det for det in detections if det[4] > conf_threshold]

            if valid_detections:
                label_content = ""
                for det in valid_detections:
                    _, _, _, _, conf, cls = det
                    label_content += f"{int(cls)} {((det[0]+det[2])/2)/img.shape[1]} {((det[1]+det[3])/2)/img.shape[0]} {abs(det[2]-det[0])/img.shape[1]} {abs(det[3]-det[1])/img.shape[0]}\n"

                label_file_path = output_labels_path / (
                    f"augmented_{variation}_{Path(image_path).stem}.txt"
                )
                
                with open(label_file_path, "w") as label_file:
                    label_file.write(label_content)


if __name__ == "__main__":
    os.system("cls||clear")
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
    )

    print(
        """
  ___               _         _         _         
 |   \ ___ ___ _ __| |   __ _| |__  ___| |___ _ _ 
 | |) / -_) -_) '_ \ |__/ _` | '_ \/ -_) / -_) '_|
 |___/\___\___| .__/____\__,_|_.__/\___|_\___|_|  
              |_|                                 
"""
    )

    parser = argparse.ArgumentParser(
        description="Build YOLOv5 dataset using collected data from aimbot."
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to the YOLOv5 dataset folder.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean the dataset by removing orphaned label files.",
    )
    parser.add_argument(
        "--conf_threshold",
        type=float,
        default=0.70,
        help="Minimum confidence threshold for bounding boxes.",
    )
    parser.add_argument(
        "--augment",
        action="store_true",
        help="Apply data augmentation (blur, noise, flip) to the images.",
    )
    parser.add_argument(
        "--num_variations",
        type=int,
        default=1,
        help="Number of variations to create for each image.",
    )

    args = parser.parse_args()

    if args.clean:
        clean_dataset(args.dataset)
    else:
        generate_yolo_labels(
            load_yolov5_model(),
            "../assets/collected",
            Path(args.dataset),
            conf_threshold=args.conf_threshold,
            augment=args.augment,
            num_variations=args.num_variations,
        )
