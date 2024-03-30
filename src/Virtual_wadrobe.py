#This code illustrates the virtual try_on feature
#importing libs
#protobuf to 3.19.0 or 3.20.0

import cv2 as cv
import cvzone
from cvzone.PoseModule import PoseDetector as PD
import time
import tkinter as tk
from tkinter import filedialog

def process_image(file_path):
    # Load the shirt image
    tee_path = file_path
    tee_img = cv.imread(tee_path, cv.IMREAD_UNCHANGED)

    time.sleep(5)

    pose_detect = PD()

    # Open webcam
    webcam = cv.VideoCapture(0)

    while True:
        # Read frame from webcam
        success, cur_frame = webcam.read()

        # Detect pose and landmarks
        cur_frame = pose_detect.findPose(cur_frame)
        landmark_list, bbox = pose_detect.findPosition(cur_frame, bboxWithHands=False, draw=False)

        if bbox and len(landmark_list) >= 24:
            # Get the shoulder and hip landmarks
            lm11 = landmark_list[11][1:3]  # Right shoulder
            lm12 = landmark_list[12][1:3]  # Left shoulder
            lm23 = landmark_list[23][1:3]  # Right hip
            lm24 = landmark_list[24][1:3]  # Left hip

            # Calculate the width and height of the shirt overlay based on the shoulder and hip landmarks
            shirt_width = int(abs(lm11[0] - lm12[0]))+60
            shirt_height = int(abs(lm11[1] - lm23[1]))+40

            # Resize the shirt image to match the size of the overlay
            shirt_resized = cv.resize(tee_img, (shirt_width, shirt_height))

            # Calculate the position for overlaying the shirt on the body
            shirt_x = int(min(lm11[0], lm12[0]))-30
            shirt_y = int(min(lm11[1]-30, lm23[1]-30))

            # Overlay the shirt image on the frame
            cur_frame = cvzone.overlayPNG(cur_frame, shirt_resized, (shirt_x, shirt_y))

        # Display the resulting frame
        cv.imshow('Webcam', cur_frame)

        # Exit loop if 'q' is pressed
        if cv.waitKey(1) == ord('q'):
            break

    # Release the webcam and close the window
    webcam.release()
    cv.destroyAllWindows()

def upload_image():
    # Open file dialog to select an image file
    filetypes = [
        ('PNG', '*.png')
    ]

    # Open file dialog and restrict file types
    file_path = filedialog.askopenfilename(filetypes=filetypes)

    # Pass the image file path to another function
    process_image(file_path)

# Create a Tkinter window
top = tk.Tk()
top.geometry("500x500")
top.title("Virtual Wadrobe")

value1 = tk.Label(top,
                  text = "Select Your Extracted T-Shirt Image")
value1.place(x = 170, y = 145)

# Create a button to upload the image
upload_button = tk.Button(top, text="Upload Image", command=upload_image)
upload_button.place(x = 210, y = 180)

value2 = tk.Label(top,
                  text = "Info : Stand one or one and a half meters away from the camera")
value2.place(x = 90, y = 225)

# Start the Tkinter event loop
top.mainloop()