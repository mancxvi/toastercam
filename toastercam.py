#!/usr/bin/env python2

from __future__ import print_function
from twython import Twython
from PIL import Image
import RPi.GPIO as GPIO
import cv2
import time
import os

class ToasterCam:
    __twitter = None
    __cam = None
    
    def __init__(self):
        self.__twitter = Twython(os.environ.get('APP_KEY'),
                                os.environ.get('APP_SECRET'),
                                os.environ.get('OAUTH_TOKEN'),
                                os.environ.get('OAUTH_TOKEN_SECRET'))
        self.__cam = cv2.VideoCapture(0)

    def tweet_photo(self, message):
        s, im = self.__cam.read()
        cv2.imwrite('photo_temp.bmp', im)
        im = Image.open('photo_temp.bmp').save('photo.jpg')
        photo = open('photo.jpg', 'rb')

        response = self.__twitter.upload_media(media=photo)

        self.__twitter.update_status(status=message,
                                    media_ids=[response['media_id']])
        
def main():
    PIN = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    toastercam = ToasterCam()
    time.sleep(1)
    GPIO.add_event_detect(PIN, GPIO.FALLING, bouncetime=300)
    
    while True:
        if GPIO.event_detected(PIN):
            time.sleep(1)
            if GPIO.input(PIN):
                print("toasting")                
            else:
                print("tweeting")
                toastercam.tweet_photo("look at this #toast")

if __name__ == '__main__':
    print("blasting out")
    main()
    
