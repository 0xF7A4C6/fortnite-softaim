# fortnite-cheat
AI powered fortnite cheat.

## Build a new model from YAML and start training from scratch
`yolo detect train data=coco128.yaml model=yolov8n.yaml epochs=10 imgsz=416`

## Start training from a pretrained *.pt model
`yolo detect train data=coco128.yaml model=yolov8n.pt epochs=100 imgsz=640`

## Build a new model from YAML, transfer pretrained weights to it and start training
`yolo detect train data=coco128.yaml model=yolov8n.yaml pretrained=yolov8n.pt epochs=100 imgsz=640`