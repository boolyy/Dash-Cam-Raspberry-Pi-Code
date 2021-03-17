import os
# comment out below line to enable tensorflow logging outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import datetime
import sys
import tensorflow as tf

#from absl import app, flags, logging
#from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from core.config import cfg
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession


# deep sort imports
from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
import lanes as lane_detect
from threading import Thread
sys.path.append('../')
PROJECT_DIR = os.getcwd()
#train_imageswin = 'C:\Users\NC\Pictures\datasetyolo\coco\images\val2017'
#train_images = os.path.join(PROJECT_DIR, 'YoloV4', 'data', 'dataset', 'val2017.txt')           
#converts YoloV4 model to a tflite supported model (comment out when necessary)
#def representative_data_gen():
 #   for input_value in tf.data.Dataset.from_tensor_slices(train_images).batch(1).take(100):
  #      yield[input_value]

#converter = tf.lite.TFLiteConverter.from_saved_model(os.path.join(PROJECT_DIR, 'YoloV4', 'checkpoints', 'yolov4-tiny-416'))
#converter.optimizations = [tf.lite.Optimize.DEFAULT]
#converter.target_spec.supported_ops = [tf.uint8]
#converter.representative_dataset = representative_data_gen
#Ensure that if any ops can't be quantized, the converter throws an error
#converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
#Set the input and output tensors to uint8 (for version 2.3.0)
#converter.inference_input_type = tf.uint8
#converter.inference_output_type = tf.uint8

#tflite_model = converter.convert()
#with open(os.path.join(PROJECT_DIR, 'YoloV4', 'checkpoints', 'yolov4quant3.tflite') , 'wb') as f:
 #   f.write(tflite_model)



# Define VideoThread class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
test_drive = os.path.join(PROJECT_DIR, 'YoloV4', 'outputs', 'testDriveS8.mp4')
class VideoThread:
    def __init__ (self, resolution=(640,480), framerate=30):
        #Initialize Camera
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'XVID'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        #Read First frame from the stream
        self.grabbed, self.frame = self.stream.read()

        #Variable to control when the camera is stopped
        self.stopped = False
    
    def start(self):
        #Start the thread that reads frames from the video stream
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        #Loops until thread is stopped
        while True:
            if self.stopped: self.stream.release()
            return

            self.grabbed, self.frame = self.stream.read()
    
    #Returns the most recent frame
    def read(self):
        return self.stream.read()
    
    def stop(self):
        self.stopped = True

#initialize deep sort (increases frame rate with Yolo V4)
model_path = os.path.join(PROJECT_DIR, 'YoloV4', 'model_data', 'mars-small128.pb')
encoder = gdet.create_box_encoder(model_path, batch_size=1)

#calculate cosine distance metric and initialize tracker
max_cosine_distance = 0.4
nn_budget = None
nms_max_overlap = 1.0
cosine_metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
tracker = Tracker(cosine_metric)

#load config for object detection
#config = ConfigProto()
#config.gpu_options.allow_growth = True
#session = InteractiveSession(config=config)
#STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
input_size = 416

#Establish a tflite model framework for the Tensorflow Interpreter

#Change use_TPU to True when using the Coral USB Accelerator
import tflite_runtime.interpreter as tflite
use_TPU = False
if use_TPU:
    interpreter = tflite.Interpreter(model_path= os.path.join(PROJECT_DIR, 'YoloV4', 'checkpoints', 'yolov4-tinync-416_edgetpu.tflite'),
                                      experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
else:
    interpreter = tflite.Interpreter(model_path= os.path.join(PROJECT_DIR, 'YoloV4', 'checkpoints', 'yolov4-tiny-416.tflite'))

#os.path.join(PROJECT_DIR, 'tfModels', 'GoogleSample', 'detect.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
#print(output_details)

floating_model = (input_details[0]['dtype'] == np.float32)
#print(input_details)



def startRecording_YOLO():
    date_and_time = time.strftime("%Y%m%d-%H-%M-%S") #Stores current date and time in YYYY-MM-DD-HH:MM format
    vid_out_path = os.path.join(PROJECT_DIR, 'YoloV4', 'outputs', date_and_time + '.avi')
    
    
    #vid = cv2.VideoCapture(test_drive) #0 for webcam/Raspberry Pi Cam
    videothread = VideoThread(resolution=(640,480), framerate=30).start()

    width = int(videothread.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(videothread.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(videothread.stream.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter(vid_out_path, codec, fps, (width,height))
    
    #width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    #height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #fps = int(vid.get(cv2.CAP_PROP_FPS))
    #codec = cv2.VideoWriter_fourcc(*'XVID')
    #output_video = cv2.VideoWriter(vid_out_path, codec, fps, (width,height))
    frame_number = 0
    freq = cv2.getTickFrequency()
    avg_fps = 0

    #while video is running/recording
    while True:
        return_val, frame = videothread.read()
        #return_val, frame = vid.read()
        
        if return_val:
            #frame = cv2.flip(frame, -1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
        else:
            print('Video error, try another format')
            break
        
        frame_number += 1
        #print('Frame #: ', frame_number)
        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data/ 255.
        #mage_data = np.expand_dims(frame_resized, axis = 0)

        #if floating_model:
         #   image_data = (np.float32(image_data) - 127.5)/127.5
        image_data = image_data[np.newaxis, ...].astype(np.float32) #Converts image data to a float32 type
        start_time = time.time()

        #TFLite Detections
        interpreter.set_tensor(input_details[0]['index'], image_data)
        interpreter.invoke()
        prediction = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
        #box = interpreter.get_tensor(output_details[0]['index'])[0]
        #scores = interpreter.get_tensor(output_details[2]['index'])[0]
        boxes, prediction_conf = filter_boxes(prediction[0], prediction[1], score_threshold=0.4, input_shape=tf.constant([input_size, input_size]))

        #Reshape = returns a new tensor that has the same values as tensor in the same order, but with a new shape given by shape
        #Shape = returns a 1-D integer tensor, represents the shape of the input 
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes = tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores = tf.reshape(prediction_conf, (tf.shape(prediction_conf)[0], -1, tf.shape(prediction_conf)[-1])),
            max_output_size_per_class = 50,
            max_total_size = 50,
            iou_threshold = 0.45,
            score_threshold = 0.5
        )

        #convert the received data into numpy arrays, then slice out unused elements
        number_of_objects = valid_detections.numpy()[0]
        bboxes = boxes.numpy()[0]
        bboxes = bboxes[0 : int(number_of_objects)]
        scores = scores.numpy()[0]
        scores = scores[0 : int(number_of_objects)]
        classes = classes.numpy()[0]
        classes = classes[0 : int(number_of_objects)]

        #format bounding boxes with normalized minimums and maximums of x and y
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(bboxes, original_h, original_w)

        prediction_bbox = [bboxes, scores, classes, number_of_objects]

        #Read in all the class names from config and only allow certain ones to be detected (eases computation power)
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)
        allowed_classes = ['traffic light', 'person', 'car', 'stop sign']

        #loop through objects and get classification name, using only the ones allows in allowed_classes
        names = []
        deleted_indx = []
        for i in range(number_of_objects):
            classification_index = int(classes[i])
            class_name = class_names[classification_index]
            if class_name not in allowed_classes: deleted_indx.append(i)
            else: names.append(class_name)
        names = np.array(names)
        count = len(names)

        #delete irrelevant detections (not in allowed_classes)
        bboxes = np.delete(bboxes, deleted_indx, axis = 0)
        scores = np.delete(scores, deleted_indx, axis = 0)

        #Feed tracker with encoded yolo detections
        detections_features = encoder(frame, bboxes)
        detections = [Detection(bbox, score, class_name, detection_feature) for bbox, score, class_name, detection_feature in zip(bboxes, scores, names, detections_features)]

        #initialize color map
        cmap = plt.get_cmap('tab20b')
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

        #run non-maxima supression (reduces amount of detected entities to as little as possible)
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(boxs, classes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]

        #Call tracker
        tracker.predict()
        tracker.update(detections)

        #update tracks
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1: continue
            bbox = track.to_tlbr()
            class_name = track.get_class()

            #if class_name == 'person': print('person found')

        #change frame to that which showcases the lane detection
        #frame = lane_detect.detect_edges(frame) #COMMENT OUT IF/WHEN ERROR OCCURS

        #distance approximation (barebones, needs more adjusting)
            cam_parameter = 18    #change with different cameras. Gets the detected distance closer to actual distance
            distance = (np.pi)/(bbox[2].item() + bbox[3].item()) * 1000 + cam_parameter
            det_dest = str(int(distance))
    
        #draw bounded box on screen
            color = colors[int(track.track_id) % len(colors)]
            color = [i * 255 for i in color]
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1] - 30)), (int(bbox[0]) + (len(class_name) + len(det_dest)) * 18, int(bbox[1])), color, -1)
            #cv2.putText(frame, class_name + "-" + str(track.track_id), (int(bbox[0]), int(bbox[1] - 10)), 0, 0.75, (255, 255, 255), 2)
            cv2.putText(frame, class_name + ": " + str(int(distance)), (int(bbox[0]), int(bbox[1] - 10)), 0, 0.75, (255, 255, 255), 2)
        
        #calculate fps of running detections
        fps = 1.0/ (time.time() - start_time)
        avg_fps = avg_fps + fps
        #print("FPS: %.2f" % fps)
        cv2.putText(frame, "FPS: " + str(int(fps)), (width - 100, height - 20),0, 0.75, (255,255,255),2)
        result = np.asarray(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("Output Video", result)

        output_video.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()
    print('Average FPS: ', (avg_fps/frame_number))
    print('Number of Frames: ', frame_number)
    videothread.stop()
        


startRecording_YOLO()