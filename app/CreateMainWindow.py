import tkinter as tk
from tkinter import HORIZONTAL
from SharpenFilter import ImProc
import numpy as np
from PIL import ImageTk, Image

class MainWindow:
    """
        Об'єкт головного вікна користувача
    """
    def __init__(self, height, width, name):
        self.root = tk.Tk()
        self.blend_ratio = 0.5
        self.r = tk.IntVar()
        self.makeAFrame = tk.Frame(self.root, bg='misty rose', width=1210, height=610)
        self.canvas_for_image = tk.Label(self.makeAFrame)
        self.sigmaTextField = tk.Entry(self.root, font=("Time new Roman", 10))  # Moved this line here
        self.slider = tk.Scale(self.root, from_=0, to=1, orient=HORIZONTAL,
                                   resolution=0.01, command=self.update_image)
        self.setGrayScaleCB = tk.Checkbutton(self.root, text="Чорно-біле зображення", variable=self.r)

        self.slider.set(self.blend_ratio)
        self.height = height
        self.width = width
        self.name = name

    #Головне меню користувача
    def mainWindow(self):
        self.root.geometry("{}x{}".format(self.height, self.width))
        self.root.configure(background="dim gray")
        self.root.title("{}".format(self.name))
        self.sigmaTextField.insert(tk.END, f"3")
        self.makeAFrame.place(x=50, y=105)
        self.canvas_for_image.place(x=3, y=3)
        self.sigmaTextField.place(x=300, y=50, height=50, width=100)
        self.slider.place(x=950, y=0, height=100, width=250)
        self.img_processor = ImProc(self, self.sigmaTextField,self.r)
        selectFile = tk.Button(self.root, text="Обрати файл", font=("New Times Roman", 10),
                                   command=self.img_processor.run)
        saveImageButton = tk.Button(self.root, text="Зберегти",  font=("New Times Roman", 10),
                                    command=self.img_processor.save_Image)
        sigmaLabel = tk.Label(self.root, text="Введіть sigma", background="dim gray", font=("New Times Roman", 10), fg="white")

        self.setGrayScaleCB.place(x=50, y=10, height=20, width=150)
        sigmaLabel.place(x=300, y=25, height=20, width=100)
        saveImageButton.place(x = 170, y = 50, height=50, width=100)
        selectFile.place(x=50, y=50, height=50, width=100)
        self.root.mainloop()


    #Показ різниці між оригіналом та обробленим зображенням
    #Користувач повинен тягне за повзунок і зображення
    def update_image(self, event=None):

        self.blend_ratio = self.slider.get()
        origin_img = self.img_processor.getOriginalImage()
        processed_img = self.img_processor.getProcessedImage()

        if origin_img is not None and processed_img is not None:
            origin = np.array(origin_img)
            processed = np.array(processed_img)

            cols_origin = int(origin.shape[1] * self.blend_ratio)

            #зрізає частину оригіналу
            origin_part = origin[:, :cols_origin]

            #зрізає части обробленого зображення там, де закінчився оригінал
            processed_part = processed[:, cols_origin:]

            #об'єднуємо оригінал та оброблене зображення
            image_blended = np.concatenate((origin_part, processed_part), axis=1)

            #формуємо утворене зображення
            self.getImage = Image.fromarray(
                np.clip(np.array(image_blended, dtype='float'), 0, 255).astype('uint8'))

            max_width, max_height = 1200, 600
            self.photo = ImageTk.PhotoImage(self.getImage.resize(
                (min(max_width, image_blended.shape[1]), min(max_height, image_blended.shape[0])),
                Image.Resampling.NEAREST
            ))
            self.canvas_for_image.config(image=self.photo)