import numpy as np
import cv2

# Function to display the avatar with the corresponding icon
def display_icon(icon_file):
    # Background color
    bb = np.zeros((icon_height, icon_width, 3), np.uint8)
    bb[:] = [blue, green, red]

    icon = cv2.imread(icon_file)
    icon = cv2.resize(icon, (icon_width, icon_height))
    # Overlap the background with the icon
    icon = cv2.addWeighted(icon, 0.7, bb, 0.3, 0)

    # Replace icon in image [y:y+h, x:x+w]
    icon_img[0:icon_height, 0:icon_width] = icon

# Defining all variables
# Defining face, smile, palm and fist detectors
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_smile.xml')
open_palm_cascade = cv2.CascadeClassifier('haarcascades/open_palm.xml')
closed_palm_cascade = cv2.CascadeClassifier('haarcascades/closed_palm.xml')

# Count of frames with each gesture
sleep_frames = 0
slp = False
fist_frames = 0
no_fist_frames = 0
palm_frames = 0
no_palm_frames = 0
smile_frames = 0
no_smile_frames = 0
wait_frames = 12

# Defining the image variables
icon_width = 85
icon_height = 75
sleep = 'images/sleep.png'
hand = 'images/hand.png'
thumbUp = 'images/thumb-up.png'
thumbDown = 'images/thumb-down.png'

# Icon image and color streams
icon_img = cv2.imread('images/animal-icon-cat.jpg')
img = cv2.imread('images/animal-icon-cat.jpg')
blue = icon_img[0, 0, 0]
green = icon_img[0, 0, 1]
red = icon_img[0, 0, 2]

# Capture video of webcam
capture = cv2.VideoCapture(0)

while capture.isOpened():
    # Extracting frames
    ret, frame = capture.read()

    # Extracting the same frame in gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ## Detects palms in the current frame and change the state of the avatar with a raised hand
    palms = open_palm_cascade.detectMultiScale(gray, 1.1, 12)
    if len(palms) > 0:
        # Adds one to the palm frames count
        palm_frames += 1
        # If the total palm frames reaches the wait frames, display the avatar with a raised hand
        if palm_frames == wait_frames:
            palm_frames = 0
            display_icon(hand)
            cv2.imshow('Icon', icon_img)
        # For each palm detected
        for (x, y, w, h) in palms:
            # Draws a black rectangle around the palm
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 3)
    else:
        # Adds one to the no palm frames count
        no_palm_frames += 1
        # If the total no palm frames count reaches the wait frames, restores the palm counts
        if no_palm_frames == wait_frames:
            palm_frames = 0
            no_palm_frames = 0

    # Detects fists and change the state of the avatar with a thumb down
    fists = closed_palm_cascade.detectMultiScale(gray, 1.1, 10)
    if len(fists) > 0:
        # Adds one to the fist frames count
        fist_frames += 1
        # If the total fist frames reaches the wait frames, display the avatar with a thumb down
        if fist_frames == wait_frames:
            fist_frames = 0
            display_icon(thumbDown)
            cv2.imshow('Icon', icon_img)
        # For each fist detected
        for (x, y, w, h) in fists:
            # Draws a white rectangle around the fist
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3)
    else:
        # Adds one to the no fist frames count
        no_fist_frames += 1
        # If the total no fist frames count reaches the wait frames, restores the fist counts
        if no_fist_frames == wait_frames:
            fist_frames = 0
            no_fist_frames = 0

    # Detects faces in the actual frame
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    if len(faces) > 0:
        # Restores the count of sleep frames
        sleep_frames = 0
        # If the avatar was in sleep mode, shows the active avatar again
        if slp:
            icon_img = img
            cv2.imshow('Icon', icon_img)
        # For each face detected
        for (x, y, w, h) in faces:
            # Draws a blue rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            # Region of Interests
            roi_gray = gray[y:y + h, x:x + w]

            # Smile Detections in the face region
            # Detects smiles and change the state of the avatar with a thumb up
            smiles = smile_cascade.detectMultiScale(roi_gray, 3.5, 20)
            if len(smiles) > 0:
                # Adds one to the smile frames count
                smile_frames += 1
                # If the total smile frames reaches the wait frames, display the avatar with a thumb up
                if smile_frames == wait_frames:
                    smile_frames = 0
                    display_icon(thumbUp)
                    cv2.imshow('Icon', icon_img)
                # Iterate through smiles
                for (sx, sy, sw, sh) in smiles:
                    # Draws a red rectangle around the smile
                    cv2.rectangle(frame, (x+sx, y+sy), (x+sx + sw, y+sy + sh), (0, 0, 255), 3)
            else:
                # Adds one to the no smile frames count
                no_smile_frames += 1
                # If the total no smile frames count reaches the wait frames, restores the smile counts
                if no_smile_frames == wait_frames:
                    smile_frames = 0
                    no_smile_frames = 0
        cv2.imshow('Icon', icon_img)
    else:
        # Adds one to the sleep frames count
        sleep_frames += 1
        print(sleep_frames)
        # If the sleep frames reaches 100, enters the sleep mode and display the avatar with the sleep icon
        if sleep_frames == 100:
            slp = True
            display_icon(sleep)
            cv2.imshow('Icon', icon_img)

    # Display the frame
    cv2.imshow('Webcam Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releasing camera resources
capture.release()
cv2.destroyAllWindows()
