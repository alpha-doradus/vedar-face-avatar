import numpy as np
import cv2


def display_icon(icon_file):
    # Background color
    bb = np.zeros((icon_height, icon_width, 3), np.uint8)
    bb[:] = [blue, green, red]

    icon = cv2.imread(icon_file)
    icon = cv2.resize(icon, (icon_width, icon_height))
    icon = cv2.addWeighted(icon, 0.7, bb, 0.3, 0)

    # Replace hand icon in image [y:y+h, x:x+w]
    icon_img[0:icon_height, 0:icon_width] = icon


sleep_frames = 0
slp = False
fist_frames = 0
no_fist_frames = 0
palm_frames = 0
no_palm_frames = 0
smile_frames = 0
no_smile_frames = 0
wait_frames = 12

icon_width = 85
icon_height = 75
sleep = 'sleep.png'
hand = 'hand.png'
thumbUp = 'thumb-up.png'
thumbDown = 'thumb-down.png'

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
open_palm_cascade = cv2.CascadeClassifier('open_palm.xml')
closed_palm_cascade = cv2.CascadeClassifier('closed_palm.xml')

# Capture video of webcam
capture = cv2.VideoCapture(0)

# Icon image
icon_img = cv2.imread('animal-icon-cat.jpg')
img = cv2.imread('animal-icon-cat.jpg')
blue = icon_img[0, 0, 0]
green = icon_img[0, 0, 1]
red = icon_img[0, 0, 2]

while capture.isOpened():
    ret, frame = capture.read()

    # Convert to frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Palm Detection (image, scale factor how much to reduce, min neighbours to retain)
    palms = open_palm_cascade.detectMultiScale(gray, 1.1, 12)
    if len(palms) > 0:
        palm_frames += 1
        if palm_frames == wait_frames:
            palm_frames = 0
            display_icon(hand)
            cv2.imshow('Icon', icon_img)
        for (x, y, w, h) in palms:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 3)
    else:
        no_palm_frames += 1
        if no_palm_frames == wait_frames:
            palm_frames = 0
            no_palm_frames = 0

    # Fist Detection (image, scale factor how much to reduce, min neighbours to retain)
    fists = closed_palm_cascade.detectMultiScale(gray, 1.1, 10)
    if len(fists) > 0:
        fist_frames += 1
        if fist_frames == wait_frames:
            fist_frames = 0
            display_icon(thumbDown)
            cv2.imshow('Icon', icon_img)
        for (x, y, w, h) in fists:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3)
    else:
        no_fist_frames += 1
        if no_fist_frames == wait_frames:
            fist_frames = 0
            no_fist_frames = 0

    # Face Detection (image, scale factor how much to reduce, min neighbours to retain
    faces = face_cascade.detectMultiScale(gray, 1.1, 10)
    if len(faces) > 0:
        sleep_frames = 0
        if slp:
            icon_img = img
            cv2.imshow('Icon', icon_img)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            # Region of Interests
            roi_gray = gray[y:y + h, x:x + w]

            # Smile Detections in the face region
            smiles = smile_cascade.detectMultiScale(roi_gray, 3.5, 20)
            if len(smiles) > 0:
                smile_frames += 1
                if smile_frames == wait_frames:
                    smile_frames = 0
                    display_icon(thumbUp)
                    cv2.imshow('Icon', icon_img)
                # Iterate through smiles
                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(frame, (x+sx, y+sy), (x+sx + sw, y+sy + sh), (0, 0, 255), 3)
                else:
                    no_smile_frames += 1
                    if no_smile_frames == wait_frames:
                        smile_frames = 0
                        no_smile_frames = 0
        cv2.imshow('Icon', icon_img)
    else:
        sleep_frames += 1
        print(sleep_frames)
        if sleep_frames == 100:
            slp = True
            display_icon(sleep)
            cv2.imshow('Icon', icon_img)

    # Display the frame
    cv2.imshow('Webcam Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


capture.release()
cv2.destroyAllWindows()
