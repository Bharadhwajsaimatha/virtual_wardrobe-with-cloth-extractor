import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os

# matplotlib inline
plt.rc('figure', autolayout=True)

def process_image(file_path):
    # T-shirt image folder
    Tee_path = file_path
    # Reading the image and displaying
    image = cv.imread(Tee_path, 1)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    print(image.shape)

    # Image Resizing
    image_size = 480
    aspect_ratio = image.shape[0] / image.shape[1]
    if aspect_ratio > 1:
        new_height = int(image_size)
        new_width = int(new_height / aspect_ratio)
    else:
        new_width = int(image_size)
        new_height = int(aspect_ratio * new_width)
    # new_width = 640
    # new_height = 480
    image_resized = cv.resize(image, (new_width, new_height))
    print(image_resized.shape)
    # plt.imshow(image_resized)
    # plt.show()

    # Extracting tshirt
    # creating a mask
    mask = np.zeros(image_resized.shape[:2], dtype=np.uint8)
    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)

    # defining the ROI

    if image_resized.shape[1] > image_resized.shape[0]:
        rect_box = (5, 5, int(image_resized.shape[1]) - 10, int(image_resized.shape[0]))
    elif image_resized.shape[1] < image_resized.shape[0]:
        rect_box = (5, 5, int(image_resized.shape[1]), int(image_resized.shape[0] - 10))
    else:
        rect_box = (5, 5, int(image_resized.shape[1]) - 10, int(image_resized.shape[0]) - 10)

    cv.grabCut(image_resized, mask, rect_box, bg_model, fg_model, 5, cv.GC_INIT_WITH_RECT)

    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Create a mask where the foreground and possible foreground pixels are marked
    foreground_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Multiply the original image with the foreground mask to extract the foreground
    foreground_image = image_resized * foreground_mask[:, :, np.newaxis]

    # Create a transparent background
    transparent_bg = np.zeros((image_resized.shape[0], image_resized.shape[1], 4), dtype=np.uint8)

    # Create an alpha channel
    alpha = np.where(foreground_mask == 1, 255, 0).astype('uint8')

    # Copy the foreground image to the transparent background
    transparent_bg[:, :, :3] = foreground_image
    transparent_bg[:, :, 3] = alpha

    # Copy the foreground image onto the transparent background
    transparent_bg = cv.resize(transparent_bg, (440, 580))
    print(transparent_bg.shape)
    plt.imshow(transparent_bg)
    plt.title("Extracted Image")
    plt.show()
    return transparent_bg, Tee_path

def save_image(transparent_bg, dest_folder, tee_path):
    file_name = os.path.basename(tee_path)
    name, extension = os.path.splitext(file_name)
    file_path = os.path.join(dest_folder + '/extracted_' + name + '.png')
    cv.imwrite(file_path, transparent_bg)

    print("Image saved to:", dest_folder)

def upload_image():
    # Open file dialog to select an image file
    filetypes = [
        ('JPEG', '*.jpeg'),
        ('JPG', '*.jpg'),
        ('PNG', '*.png')
    ]

    # Open file dialog and restrict file types
    file_path = filedialog.askopenfilename(filetypes=filetypes)

    # Process the selected image
    transparent_bg, Tee_path = process_image(file_path)

    def select_destination():
        # Open a directory dialog to select the destination folder
        dest_folder = filedialog.askdirectory(initialdir="/", title="Select Destination Folder")

        # Save the extracted image to the destination folder
        save_image(transparent_bg, dest_folder, Tee_path)

        messagebox.showinfo("Extracted Image Folder", "Extracted Image saved to - " + str(dest_folder))

        # Close the destination selection window
        dest_window.destroy()

    # Create a new window for selecting the destination folder
    dest_window = tk.Toplevel()
    dest_window.geometry("500x500")
    dest_window.title("Select Destination Folder")

    # Create a label and button in the destination window
    dest_label = tk.Label(dest_window, text="Select destination folder to save the extracted image")
    dest_label.place(x = 125, y = 145)

    dest_button = tk.Button(dest_window, text="Select Folder", command=select_destination)
    dest_button.place(x = 210, y = 180)
top = tk.Tk()
top.geometry("500x500")
top.title("T-shirt Extractor")

message = messagebox.showinfo("Info", "Select the image of a single T-shirt having JPG, JPEG and PNG format")

value1 = tk.Label(top,
                  text = "Select Your T-Shirt Image")
value1.place(x = 190, y = 145)

# Create a button to upload the image
upload_button = tk.Button(top, text="Upload Image", command=upload_image)
upload_button.place(x = 210, y = 180)


# Start the Tkinter event loop
top.mainloop()






