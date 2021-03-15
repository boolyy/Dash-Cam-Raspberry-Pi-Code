from yolov4.tf import YOLOv4, YOLODataset, save_as_tflite
import os
PATH_DIR = os.getcwd()
yolo = YOLOv4()
cfgnames = os.path.join(PATH_DIR, 'data', 'classes', 'coco.names')
cfgpath = os.path.join(PATH_DIR, 'checkpoints', 'yolov4-tiny-relu-tpu.cfg')
yolo.config.parse_names('./data/classes/coco.names')
yolo.config.parse_cfg('./checkpoints/yolov4-tiny-relu-tpu.cfg')

yolo.make_model()
yolo.load_weights(
    './checkpoints/yolov4-tiny.weights', weights_type="yolo"
)

dataset = YOLODataset(
    config=yolo.config,
    dataset_list='./data/dataset/val2017hnn.txt',
    #image_path_prefix='/media/user/Source/Data/coco_dataset/coco/images/val2017',
    training=False,
)

save_as_tflite(
    model=yolo.model,
    tflite_path="yolov4-tiny-relu-int8.tflite",
    quantization="full_int8",
    dataset=dataset,
)