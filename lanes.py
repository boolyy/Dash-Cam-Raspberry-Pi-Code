import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def make_coords(image, line_params):
    try:
        slope, intercept = line_params
    except TypeError:
        slope,intercept = 1,0

    y1 = image.shape[0]
    y2 = int(y1 *(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    # for line in lines:
    #     x1, y1, x2, y2 = line.reshape(4)
    #     parameters = np.polyfit((x1,x2), (y1,y2), 1) #returns vector of coeff. with slope/intercepts
    #     slope = parameters[0]
    #     intercept = parameters[1]
    #     if slope < 0: 
    #         left_fit.append((slope, intercept))
    #     else:
    #         right_fit.append((slope, intercept))
    # left_fit_avg = np.average(left_fit, axis=0)
    # right_fit_avg = np.average(right_fit, axis=0)
    # left_line = make_coords(image, left_fit_avg)
    # right_line = make_coords(image, right_fit_avg)
    # return np.array([left_line, right_line])

    height, width, _ = image.shape
    bounds = 1/3
    left_bounds = width * (1-bounds)
    right_bounds = width * bounds
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2: 
                print('Skipping vertical line segment: ' + line)
                continue
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                if x1 < left_bounds and x2 < left_bounds: left_fit.append((slope, intercept))
            else:
                if x1 > right_bounds and x2 > right_bounds: right_fit.append((slope, intercept))
    left_fit_avg = np.average(left_fit, axis=0)
    right_fit_avg = np.average(right_fit, axis=0)
    left_line = make_coords(image, left_fit_avg)
    right_line = make_coords(image, right_fit_avg)
    return np.array([left_line, right_line])


def canny(image):
    hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    low_yellow = np.array([15, 40, 40])     
    upper_yellow = np.array([30, 255, 30])          ##Color Value
    yellow_mask = cv2.inRange(hsl, low_yellow, upper_yellow)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  #converts current frame to a grayscale image
    combined_mask = cv2.addWeighted(yellow_mask, 1, gray, 1, 1)
    blur = cv2.GaussianBlur(combined_mask, (1,1), 0)         #reduces noise from the current frame
    canny = cv2.Canny(blur, 50, 150)                #makes a gradient image showing outlines of lanes (higher intensities)
    
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            #draws lines with color blue and thickness 10
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

#makes a mask image with a black background
#Applies triangle over the mask and makes the region white
#masked_image =  canny image to show r.o.i traced by polygon contour of the mask
def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]]
        )
    mask = np.zeros_like(image)                    
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask) 
    return masked_image

def detect_edges(frame):
    lane_image = np.copy(frame)
    canny_image = canny(lane_image)
    cropped_image = region_of_interest(canny_image)

    lines = cv2.HoughLinesP(cropped_image, 1, np.pi/180, 100, np.array([]), minLineLength=8, maxLineGap=1)
    avg_lines = average_slope_intercept(lane_image, lines)
    line_image = display_lines(lane_image ,avg_lines)
    combined_image = cv2.addWeighted(lane_image, 1, line_image, 1, 1)
    return combined_image

def test_code():
    test_vod_path = os.path.join(os.getcwd(), 'YoloV4', 'outputs', '20210313-18-41-09.avi')
    cap_test = cv2.VideoCapture(test_vod_path)
    while(cap_test.isOpened()):
        a, frame = cap_test.read()
        combo_test = detect_edges(frame)
        cv2.imshow("test", combo_test)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap_test.release()
    cv2.destroyAllWindows()

#test_code()