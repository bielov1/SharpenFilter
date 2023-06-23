import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
from PIL import ImageTk, Image
from scipy.signal import convolve2d
import easygui

__author__ = "Oleh Bielov"
__group__ = "IO-11"
__command__ = "26"
__version__ = "1.0.0"
__email__ = "olaph22@gmail.com"
__status__ = "Demo"

class ImProc:
    """
        Головний об'єкт для обробки зображення.
        В цьому обє'кті знаходяться такій функії, як run(), getPathFile, sharpen(),
        toGrayScale()(optional), Gaussianfilter(), conv(), unshaprMasking(), saveImage(),
        setImage(), getOriginalImage() і getProcessedImage().
    """
    def __init__(self, window, sigmaTextField, var):
        self.window = window
        self.sigmaTextField = sigmaTextField
        self.var = var
        self.imHeight = None
        self.imWidth = None
        self.pixels = None
        self.original_image = None
        self.image = None
        self.file_path = None
        self.image_conv = None
        self.processed_image = None
    #функція run() - важлива функція, яка розбита на підфункції, тобто
    #викликає інші функції, щоб отримати і потім сформувати нове зображення
    def run(self):
        try:
            self.getPathFile()
            if(self.var.get() == 1):
                self.toGrayScale()
            elif(self.var.get() == 0):
                self.sharpen()
            G = self.Gaussianfilter()
            GG = self.conv(self.pixels, G)
            processed_image = self.unsharpMasking(self.pixels, GG)
            self.processed_image =Image.fromarray(np.clip(np.array(processed_image, dtype='float'), 0, 255).astype('uint8'))
            self.setImage()
        except Exception as e:

            easygui.msgbox("Сталася помилка! Виберіть будь-ласка ваш файл або ви не ввели значення для sigma", "Error")

    #функція, яка отримує шлях до файлу
    def getPathFile(self):
        self.file_path = askopenfilename()
        return


    #функція, яка перетворює зображення у вигляд функції f(x,y,z)
    def sharpen(self):
        self.image = Image.open(self.file_path)
        self.pixels = np.array(self.image)
        self.imWidth, self.imHeight = self.image.size
        self.original_image = Image.fromarray(np.array(self.pixels, dtype='uint8'))
        return


    #функція, яка перетворює зображення у вигляд функції f(x,y).
    #Також вона перетворює RGB фото у чорно-біле фото
    def toGrayScale(self):
        self.image = Image.open(self.file_path)
        np_pixels = np.array(self.image)
        self.imWidth, self.imHeight = self.image.size
        self.pixels = np.array(
            [[0] * self.imWidth for _ in range(self.imHeight)])
        for i in range(self.imHeight):
            for j in range(self.imWidth):
                b = np_pixels[i][j][0]
                g = np_pixels[i][j][1]
                r = np_pixels[i][j][2]
                grayscale_value = int(b * 0.114 + g * 0.587 + r * 0.299)
                self.pixels[i][j] = grayscale_value
        self.original_image = Image.fromarray(self.pixels.astype('uint8'))
        return


    #фільтр Гаусса призначенний для створення маски для подальшої обробки зображення
    #В залежності від розміру фотографії, функція автоматично підбире розмір маски
    def Gaussianfilter(self):
        #в залежності від ширини фото ми беремо для розміру маски Гауса 6% або 0.06 від її ширини
        #потім знаходимо найбільше sigma. Наприклад, ширина зображення 2048p =>
        #2048*0.06 = 122 - але треба брати такий розмір щоб при 6*sigma було на один менше ніж 2048*0.06 = 122,тому це 127
        #[6*sigma][6*sigma] => 6*25 > 122 - не підходить
        #тому 6*21 < 127 => sigma = 21

        #але код дає користувачу самому ввести значення sigma

        sigma = float(self.sigmaTextField.get())
        G_kernel = int(self.imWidth * 0.06)
        m, n = [(ss - 1.) / 2. for ss in (G_kernel, G_kernel)]
        y, x = np.ogrid[-m:m + 1, -n:n + 1]
        G = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
        G = G / G.sum()
        return G

    #функція згортка.
    #приймає два початкові значення: image - зображення, kernel - маска
    def conv(self, image, kernel):
        #перевірка на RGB фото
        if len(image.shape) == 3:
            image_conv = np.zeros_like(image,
                                       dtype='float64')
            for i in range(image.shape[2]):
                image_conv[:, :, i] = convolve2d(image[:, :, i], kernel, mode='same')
        else:
            image_conv = convolve2d(image, kernel, mode='same')

        image_conv = image_conv / np.sum(kernel)
        return image_conv


    #сам метом обробки, який збільшує різкість зображення
    def unsharpMasking(self, original_image, blurred_image):
        mask_image = original_image - blurred_image
        g_image = original_image + 1*mask_image
        return g_image

    def getOriginalImage(self):
        return self.original_image

    def getProcessedImage(self):
        return self.processed_image


    #функція для збереження результату в комп'ютер
    def save_Image(self):
        filetypes = [
            ('JPEG', '*.jpg'),
            ('PNG', '*.png')
        ]
        #може зберегти тільки ті зображення в яких
        save_path = tk.filedialog.asksaveasfilename(
            defaultextension='.jpg', filetypes=filetypes)  # opens a save file dialog to get the save path
        if save_path:
            try:
                ext = save_path.split('.')[-1]
                if ext == 'png':
                    self.processed_image.save(save_path, 'PNG')
                else:
                    self.processed_image.convert('RGB').save(save_path, 'JPEG')
            except Exception as e:
                easygui.msgbox("Сталася помилка! Неможливо зберегти файл.")


    #показ фотографії у вікні користувача
    def setImage(self):
        self.window.canvas_for_image.image = ImageTk.PhotoImage(
            self.processed_image.resize((min(self.imWidth, 1200), min(self.imHeight, 600)), Image.LANCZOS))
        self.window.canvas_for_image.config(image=self.window.canvas_for_image.image)