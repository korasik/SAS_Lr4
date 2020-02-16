# распознавание лица

BUTTON_PIN = 16
LED_PIN = 18

import numpy as np
import cv2
import sys
import RPi.GPIO as GPIO
from time import sleep

def on_off_ident(channel):
    global on_off_id
    if on_off_id == 0:
        print('Identification ON')
        on_off_id = 1
    else:
        print('Identification OFF')
        on_off_id = 0

on_off_id = 0

prev_x = 320

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(LED_PIN, GPIO.OUT)

    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, bouncetime=300)
    GPIO.add_event_callback(BUTTON_PIN, on_off_ident)
    
    faceCascade = cv2.CascadeClassifier('/home/pi/opencv-4.1.2/data/haarcascades/haarcascade_frontalface_alt.xml')
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    while True:
        ret, img = cap.read()
        if on_off_id == 1:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,     
                scaleFactor=1.2,
                minNeighbors=5,     
                minSize=(20, 20)
            )
            if len(faces) > 0:
                GPIO.output(LED_PIN, True)
            else:
                GPIO.output(LED_PIN, False)

            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                if x + (w / 2) < prev_x - 40:
                    print('Turn LEFT')
                    prev_x = x + (w / 2)
                if x + (w / 2) > prev_x + 40:
                    print('Turn RIGHT')
                    prev_x = x + (w / 2)
            
            cv2.putText(img, str('Detection ON'), (5,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            GPIO.output(LED_PIN, False)
            cv2.putText(img, str('Detection OFF'), (5,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            
        cv2.imshow('video',img)

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break

    cap.release()
    cv2.destroyAllWindows()
        
except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
