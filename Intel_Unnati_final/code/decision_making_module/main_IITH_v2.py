import os
import cv2
import ultralytics
from ultralytics import YOLO
from time import sleep
from random import randint
import numpy as np
import thingspeak

# Define the model
model_path = r"C:\Users\Kumar\Desktop\runs\weights\best.pt"
video_path = r"F:\0000000_V1.mp4"
model = YOLO(model_path)

#Define Thingspeak credentials.


# Capture video from webcam
video = cv2.VideoCapture(video_path)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('F:/output.mp4', fourcc, 20.0, (640, 480))

# Defining color palette for the segmentation (80 classes)
colors = [(0, 0, 255), (141, 118, 52), (108, 56, 59), (109, 156, 118), (227, 79, 50), (180, 186, 238), (157, 31, 160),
          (78, 236, 182), (201, 230, 218), (122, 145, 159), (148, 138, 172), (104, 207, 1), (178, 189, 51), (14, 163, 70),
          (161, 188, 61), (193, 224, 147), (46, 165, 146), (23, 53, 231), (253, 156, 73), (231, 253, 31), (89, 131, 60),
          (161, 211, 216), (243, 35, 30), (211, 96, 25), (4, 170, 6), (211, 53, 197), (159, 197, 10), (153, 140, 3),
          (80, 45, 252), (87, 243, 127), (137, 200, 234), (124, 104, 116), (133, 239, 188), (103, 228, 57), (115, 159, 58),
          (65, 133, 84), (199, 67, 84), (143, 0, 155), (65, 91, 92), (130, 31, 232), (9, 39, 199), (238, 204, 183),
          (17, 140, 193), (184, 83, 231), (254, 203, 114), (180, 102, 239), (199, 22, 98), (192, 150, 109), (124, 132, 12),
          (132, 249, 226), (93, 25, 71), (251, 254, 130), (35, 55, 125), (13, 179, 253), (253, 95, 16), (174, 18, 189),
          (21, 85, 58), (172, 170, 101), (101, 168, 228), (43, 209, 188), (154, 165, 95), (190, 145, 253), (120, 63, 135),
          (44, 49, 49), (183, 141, 178), (127, 224, 10), (56, 220, 12), (129, 27, 169), (217, 218, 10), (155, 92, 205),
          (208, 101, 0), (74, 29, 107), (25, 157, 192), (110, 131, 8), (210, 150, 226), (221, 110, 197), (85, 132, 136),
          (114, 39, 77), (190, 123, 46), (124, 97, 22)]

classes_needed = [0, 2, 3, 4, 6, 9, 10, 11, 12, 13, 14, 15, 19, 27, 28, 29, 31, 33]

if video.isOpened():
    speed = 100  # Default speed
    while True:
        fps = str(video.get(cv2.CAP_PROP_FPS))
        ret, frame = video.read()
        if ret:
            results = model.predict(frame, stream=True)
            h, w, c = frame.shape
            for r in results:
                boxes = r.boxes
                probs = r.probs
                masks = r.masks
            classes = boxes.cls.cpu().numpy()

            if masks is not None:
                for i in range(len(masks.xyn)):
                    masks.xyn[i] *= [w, h]
                    cv2.polylines(frame, [masks.xyn[i].astype('int')], True, colors[classes[i].astype('int')], 2)


            if 0 in classes:
                cv2.putText(frame, "Road Detected", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # Blue
            if 2 in classes:
                cv2.putText(frame, "Drivable Detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (108, 56, 59), 2)  # Red
            if 4 in classes:
                cv2.putText(frame, "Non-Drivable Detected", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (227, 79, 50), 2)  # Green

            if any(item in classes_needed for item in classes):
                
                if 0 in classes:#ROAD
                    speed = 80
                    
                    if 6 in classes: #person
                        speed= 20
                        
                    if 9 or 10 or 11 or 12 or 13 or 14 or 15: #all vehicles
                        speed= 60
                        

                    if 6 and (9 or 10 or 11 or 12 or 13 or 14 or 15) in classes:
                        speed= 30
                        
                    #if 19 or 27 or 29 or 31 or 3 or 29 in classes: # wall/obs/bridge/vegetation/sidewalk/building
                     #   speed= 10
                       
                elif 2 in classes: #DRIVABLE FALLBACK
                    speed = 55 
                    if 6 in classes: #person
                        speed= 10
                        
                    if 9 or 10 or 11 or 12 or 13 or 14 or 15: #all vehicles
                        speed= 40
                        

                    if 6 and (9 or 10 or 11 or 12 or 13 or 14 or 15) in classes:
                        speed= 15
                        
                    #if 19 or 27 or 29 or 31 or 3 or 29 in classes: # wall/obs/bridge/vegetation/sidewalk/building
                     #   speed= 5
                
                elif 2 and 4 in classes:#BOTH DRIVABLE AND NON DRIVABLE
                    speed= 30
                    
                elif 4 in classes:#NON DRIVABLE FALLBACK
                    speed = 0
                    

                disp_text = f"Speed will be {speed}"
            else:
                disp_text = "Speed will be 100"

            cv2.putText(frame, fps, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, 4)
            cv2.putText(frame, disp_text, (300, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, 4)
            cv2.imshow("Frame", frame)
             
            #out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            sleep(0.005)
        else:
            print("Error: Failed to capture frame")
else:
    print("Cannot open camera")

cv2.destroyAllWindows()