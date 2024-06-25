import cv2
import urllib.request
import numpy as np
import time
pulse_ms = 30
centerpoint = {}
centerpoint_x = {}
centerpoint_y = {} 
# Replace the URL with the IP camera's stream URL
url = 'http://172.20.10.2/cam-lo.jpg'
cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)
 
 
# Create a VideoCapture object
cap = cv2.VideoCapture(url)
 
# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()
 
# Read and display video frames
while True:
    # Read a frame from the video stream
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    #ret, frame = cap.read()
    im = cv2.imdecode(imgnp,-1)
    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # Preprocessing: Apply Gaussian blur to reduce noise
    img_blurred = cv2.GaussianBlur(img, (5, 5), 0)

    # Detect circles
    circles = cv2.HoughCircles(img_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=60, param1=100, param2=35, minRadius=40, maxRadius=250)

    # Ensure circles were found
    if circles is not None:
        circles = np.uint16(np.around(circles))   # Convert coordinates to integers
        i=0
        for circle in circles[0, :]:
            center = (circle[0], circle[1])  # Center coordinates
            radius = circle[2]  # Radius
            # Draw circle outline
            cv2.circle(img, center, radius, (0, 0, 255), 3)
            # Draw circle center
            cv2.circle(img, center, 2, (0, 0, 0), 6)
            centerpoint[i] = center
            centerpoint_x[i] = circle[0]
            centerpoint_y[i] = circle[1]
            i+=1
    #移動中心點(160,120)
        if centerpoint_x[0]<159.9:
            print('a') #要向左
        elif centerpoint_x[0]>160.1:
            print('b') #要向右
        
        if centerpoint_y[0]<119.9:
            print('c') #要向上
        elif centerpoint_y[0]>120.1:
            print('d') #要向下

        if centerpoint_x[0] < 160.1 and centerpoint_x[0] < 159.9 and centerpoint_y[0]<120.1 and centerpoint_y[0]>119.9:
            print ('e') #結束動作
            time.sleep(10)

    cv2.imshow('live Cam Testing',img)
    print(centerpoint)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
    
 
cap.release()
cv2.destroyAllWindows()