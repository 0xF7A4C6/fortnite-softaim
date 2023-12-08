
# YOLOv5 Dataset Management Script

This script provides functionality for managing datasets for YOLOv5, including cleaning orphaned label files and generating YOLO labels for new images.

## Prerequisites

- Python 3.6 or later
- Install required Python packages using the following command:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

```bash
python script_name.py --dataset path/to/dataset --clean
```

```
--dataset: Path to the YOLOv5 dataset folder.
--num_variations: Number of variations to create for each image.
--augment: Apply data augmentation (blur, noise, flip...) to the images.
--conf_threshold: Minimum confidence threshold for bounding boxes. Default is set to 0.70.
--clean: Clean the dataset by removing orphaned label/img file, If not provided, the script generates YOLO labels for new images.
```

## Directory Structure

The script expects the following directory structure:

```
/path/to/dataset/
|-- images/
|   |-- image1.jpg
|   |-- image2.jpg
|   |-- ...
|-- labels/
|   |-- image1.txt
|   |-- image2.txt
|   |-- ...
```

## Example

```bash
# Clean the dataset
python script_name.py --dataset path/to/dataset --clean

# Generate YOLO labels for new images
python script_name.py --dataset path/to/dataset
```