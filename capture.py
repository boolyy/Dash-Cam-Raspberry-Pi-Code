#Very barebones camera script.

import cv2, time

#creates video object, 0 for external camera
video = cv2.VideoCapture(0)

#time variable
a = 0
while True:
    a = a + 1

    check, frame = video.read() #creates a frame object

    print(check)

    # Prints matrix representation of the image
    print(frame)

    #Shows the frame
    cv2.imshow("Capturing", frame)

    key = cv2.waitKey(1)

    #breaks streaming when q is pressed. Change key when necessary
    if key == ord('q'):
        break

#prints streaming time (ms)
print(a)

#Shuts down camera
video.release()
cv2.destroyAllWindows()