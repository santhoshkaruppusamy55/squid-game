import cv2
import os
import numpy as np
import time
from playsound import playsound 

# Define file paths
folderPath = r"C:\Users\santh\OneDrive\Desktop\ProjectExpo\squid game\red-light-green-light\frames"
soundPath = r"C:\Users\santh\OneDrive\Desktop\ProjectExpo\squid game\red-light-green-light\sounds"

# Load images
mylist = os.listdir(folderPath)
graphic = [cv2.imread(f'{folderPath}/{imPath}') for imPath in mylist]
green, red, kill, winner, intro = graphic[:5]

# Show intro screen with sound
cv2.imshow('Squid Game', cv2.resize(intro, (0, 0), fx=0.5, fy=0.5))
cv2.waitKey(125)
playsound(os.path.join(soundPath, 'RLGLsong.mp3'))

# Loop to keep intro screen open until 'q' is pressed
while True:
    cv2.imshow('Squid Game', cv2.resize(intro, (0, 0), fx=0.5, fy=0.5))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Game variables
TIMER_MAX = 30
TIMER = TIMER_MAX
maxMove = 8000000
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)

win = False
prev = time.time()
showFrame = cv2.resize(green, (0, 0), fx=0.5, fy=0.5)
isgreen = True
green_start_time = time.time()

# Main game loop
while cap.isOpened() and TIMER >= 0:
    # Check for 'w' key press immediately
    key = cv2.waitKey(1) & 0xFF
    if key == ord('w'):
        win = True
        break

    ret, frame = cap.read()
    if not ret:
        break  # Exit if there is an issue with capturing frames

    # Display the countdown timer on the screen
    cv2.putText(showFrame, str(TIMER), (50, 50), font, 1,
                (0, int(255 * (TIMER) / TIMER_MAX), int(255 * (TIMER_MAX - TIMER) / TIMER_MAX)),
                4, cv2.LINE_AA)

    cur = time.time()

    # Update the timer every second
    if cur - prev >= 1:
        prev = cur
        TIMER -= 1

        # Toggle green and red light every 3 seconds
        if isgreen and (cur - green_start_time >= 3):
            showFrame = cv2.resize(red, (0, 0), fx=0.5, fy=0.5)
            isgreen = False
            ref = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif not isgreen:
            showFrame = cv2.resize(green, (0, 0), fx=0.5, fy=0.5)
            isgreen = True
            green_start_time = cur  # Reset green start time when switching back to green

    # If light is red, check for movement
    if not isgreen:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameDelta = cv2.absdiff(ref, gray)
        frameDelta = cv2.GaussianBlur(frameDelta, (5, 5), 0)
        thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
        change = np.sum(thresh)
        if change > maxMove:
            break

    # Show camera feed in the corner of the main game frame
    camShow = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
    camH, camW = camShow.shape[0], camShow.shape[1]
    showFrame[0:camH, -camW:] = camShow

    # Display the main game frame
    cv2.imshow('Squid Game', showFrame)
    if key == ord('q'):
        break

cap.release()

# Game over screen: show win or lose outcome
if win:
    cv2.imshow('Squid Game', cv2.resize(winner, (0, 0), fx=0.5, fy=0.5))
    cv2.waitKey(125)
    playsound(os.path.join(soundPath, 'win.mp3'))
    while True:
        cv2.imshow('Squid Game', cv2.resize(winner, (0, 0), fx=0.5, fy=0.5))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    for i in range(10):
        cv2.imshow('Squid Game', cv2.resize(kill, (0, 0), fx=0.5, fy=0.5))
    playsound(os.path.join(soundPath, 'kill.mp3'))
    while True:
        cv2.imshow('Squid Game', cv2.resize(kill, (0, 0), fx=0.5, fy=0.5))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
