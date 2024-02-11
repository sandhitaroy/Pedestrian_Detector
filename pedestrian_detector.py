import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils

top = tk.Tk()
top.geometry('800x600')
top.title('Pedestrian Detector')
top.configure(background='#CDCDCD')

label1 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect_pedestrians(file_path):
    global label1, hog
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        image = cv2.imread(file_path)
        if image is not None:
            image = imutils.resize(image, width=min(800, image.shape[1]))
            (regions, _) = hog.detectMultiScale(image, winStride=(4, 4), padding=(4, 4), scale=1.05)
            for (x, y, w, h) in regions:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Pedestrian Detection", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Error: Unable to load image.")
    elif file_path.lower().endswith('.mp4'):
        cap = cv2.VideoCapture(file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = imutils.resize(frame, width=min(800, frame.shape[1]))
                (regions, _) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(4, 4), scale=1.05)
                for (x, y, w, h) in regions:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow("Pedestrian Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Error: Unsupported file format.")

def show_detect_button(file_path):
    detect_button = Button(top, text="Detect Pedestrians", command=lambda: detect_pedestrians(file_path), padx=10, pady=5)
    detect_button.configure(background="#364156", foreground='white', font=('arial', 10, 'bold')) 
    detect_button.place(relx=0.79, rely=0.46)

def upload_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Files", "*.png;*.jpg;*.jpeg;*.mp4")])
        label1.configure(text='Uploaded file: ' + file_path)
        show_detect_button(file_path)
    except Exception as e:
        print("Error:", e)

upload_button = Button(top, text="Upload File", command=upload_file, padx=10, pady=5)
upload_button.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload_button.pack(side='bottom', pady=50)

label1.pack(side="bottom", expand=True)
heading = Label(top, text="Pedestrian Detector", pady=20, font=("arial", 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()
top.mainloop()
