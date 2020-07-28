# import the necessary packages
import cv2
import numpy as np
# defining face detector
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
open_palm_cascade = cv2.CascadeClassifier('open_palm.xml')
closed_palm_cascade = cv2.CascadeClassifier('closed_palm.xml')

ds_factor = 0.6


icon_width = 85
icon_height = 75
sleep = 'sleep.png'
hand = 'hand.png'
thumbUp = 'thumb-up.png'
thumbDown = 'thumb-down.png'


def display_icon(icon_file):
    # Background color
    bb = np.zeros((icon_height, icon_width, 3), np.uint8)
    bb[:] = [blue, green, red]

    if icon_file is None:
        icon_img[0:icon_height, 0:icon_width] = bb
    else:
        icon = cv2.imread(icon_file)
        icon = cv2.resize(icon, (icon_width, icon_height))
        icon = cv2.addWeighted(icon, 0.7, bb, 0.3, 0)
        # Replace hand icon in image [y:y+h, x:x+w]
        icon_img[0:icon_height, 0:icon_width] = icon

    return icon_img


# Icon image
icon_img = cv2.imread('animal-icon-cat.jpg')
img = cv2.imread('animal-icon-cat.jpg')
blue = icon_img[0, 0, 0]
green = icon_img[0, 0, 1]
red = icon_img[0, 0, 2]


class VideoCamera(object):
    def __init__(self):
       #capturing video
        self.video = cv2.VideoCapture(0)

        self.sleep_frames = 0
        self.slp = False
        self.fist_frames = 0
        self.no_fist_frames = 0
        self.palm_frames = 0
        self.no_palm_frames = 0
        self.smile_frames = 0
        self.no_smile_frames = 0
        self.wait_frames = 15

    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self):
       #extracting frames
        ret, frame = self.video.read()
        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor,
        interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        avatar = icon_img

        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        if len(faces) > 0:
            self.sleep_frames = 0
            if self.slp:
                self.slp = False
                avatar = display_icon(None)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Region of Interests
                roi_gray = gray[y:y + h, x:x + w]

                # Smile Detections in the face region
                smiles = smile_cascade.detectMultiScale(roi_gray, 3.5, 20)
                if len(smiles) > 0:
                    for (sx, sy, sw, sh) in smiles:
                        cv2.rectangle(frame, (x + sx, y + sy), (x + sx + sw, y + sy + sh), (0, 0, 255), 3)
                        self.smile_frames += 1
                        if self.smile_frames == self.wait_frames:
                            self.smile_frames = 0
                            avatar = display_icon(thumbUp)
                        break
                else:
                    self.no_smile_frames += 1
                    if self.no_smile_frames == self.wait_frames:
                        self.smile_frames = 0
                        self.no_smile_frames = 0
                break
        else:
            self.sleep_frames += 1
            print(self.sleep_frames)
            if self.sleep_frames == 150:
                self.slp = True
                avatar = display_icon(sleep)

        palms = open_palm_cascade.detectMultiScale(gray, 1.1, 12)
        if len(palms) > 0:
            for (x, y, w, h) in palms:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 3)
                self.palm_frames += 1
                if self.palm_frames == self.wait_frames:
                    self.palm_frames = 0
                    avatar = display_icon(hand)
                break
        else:
            self.no_palm_frames += 1
            if self.no_palm_frames == self.wait_frames:
                self.palm_frames = 0
                self.no_palm_frames = 0

        fists = closed_palm_cascade.detectMultiScale(gray, 1.1, 10)
        if len(fists) > 0:
            for (x, y, w, h) in fists:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3)
                self.fist_frames += 1
                if self.fist_frames == self.wait_frames:
                    self.fist_frames = 0
                    avatar = display_icon(thumbDown)
                break
        else:
            self.no_fist_frames += 1
            if self.no_fist_frames == self.wait_frames:
                self.fist_frames = 0
                self.no_fist_frames = 0


        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        if avatar is not None:
            ret2, ava = cv2.imencode('.jpg', avatar)
        else:
            ret2, ava = cv2.imencode('.jpg', img)
        return jpeg.tobytes(), ava.tobytes()
