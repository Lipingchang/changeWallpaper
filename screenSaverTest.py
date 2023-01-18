from tkinter import *
from random import randint
import os
import sys
from typing import List
from PIL import ImageTk, Image


class Screen:
    def __init__(self):
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.95)
        self.root.bind('<Button-1>', self.myquit)
        # self.root.bind('<Motion>', self.myquit)

        # print(self.canvas.config())  canvas的borderwidth本来就是0 highlightthickness初始是2
        self.canvas = Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)

        # self.ball = Balls(self.canvas)
        # self.moveBalls()

        self.images = ScreenImages(self.canvas)
        self.nextImages()

        self.root.mainloop()

    def nextImages(self):
        self.images.nextImage()
        self.root.after(10 * 1000, self.nextImages)

    def moveBalls(self):
        self.ball.moveBall()
        self.root.after(30, self.moveBalls)

    def myquit(self, event):
        self.root.destroy()


class ScreenImages:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.currentImage = 0  # 当前显示的图片index
        self.images: List[PhotoImage] = []  # 所有图片
        self.canvasImageWig = 0  # image控件的编号
        self.errorTextId = 0  # 如果没有找到图片, 会显示报错的text控件的id
        max_w = canvas.winfo_screenwidth()
        max_h = canvas.winfo_screenheight()

        # 打包后文件 运行时 会把文件解压到 _MEIPASS 路径中
        imageFileFolderPath = 'screensaverJpegFiles'
        if getattr(sys, 'frozen', False):
            # 打包后
            imageFileFolderPath = os.path.join(sys._MEIPASS, imageFileFolderPath)
        else:
            # 源文件运行
            imageFileFolderPath = os.path.join(os.path.curdir, imageFileFolderPath)

        for f in os.listdir(imageFileFolderPath):
            if f.lower().endswith("jpeg") or f.lower().endswith("jpg"):
                # 缩放图片适合屏幕
                originImg = Image.open(os.path.join(imageFileFolderPath,f))
                x_scale = max_w / originImg.size[0]
                y_scale = max_h / originImg.size[1]
                scale = x_scale if x_scale < y_scale else y_scale
                img = originImg.resize((int(scale * originImg.size[0]), int(scale * originImg.size[1])),
                                       Image.ANTIALIAS)
                self.images.append(
                    ImageTk.PhotoImage(img)
                )
        # 放入第一张图片
        if len(self.images):
            self.canvasImageWig = self.canvas.create_image(int(max_w / 2), int(max_h / 2),
                                                           image=self.images[self.currentImage], anchor=CENTER)

    def nextImage(self):
        if len(self.images):
            self.currentImage += 1
            self.currentImage = self.currentImage % len(self.images)  # TODO 除0?
            self.canvas.itemconfig(self.canvasImageWig, image=self.images[self.currentImage])
        elif self.errorTextId == 0:  # 找不到图片:
            self.errorTextId = self.canvas.create_text(
                100, 100,
                text="screen saver images not found.. click to back..",
                anchor=NW
            )


class Balls:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.screenWidth = canvas.winfo_screenwidth()
        self.screenHeight = canvas.winfo_screenheight()

        self.randValues()
        self.createBall()

    def randValues(self):
        self.radius = 100
        self.X_coord = randint(self.radius, self.screenWidth - self.radius)
        self.Y_coord = randint(self.radius, self.screenHeight - self.radius)
        self.x_speed = 5
        self.y_speed = 5
        self.color = "red"

    def randColor(self):
        randVal = lambda: randint(0, 0xffff)
        return "#{:04x}{04x}{04x}".format(randVal(), randVal(), randVal())

    def createBall(self):
        x1 = self.X_coord - self.radius
        y1 = self.Y_coord - self.radius
        x2 = self.X_coord + self.radius
        y2 = self.Y_coord + self.radius

        self.ball = self.canvas.create_oval(
            x1, y1, x2, y2, fill=self.color, outline=self.color
        )

    def moveBall(self):
        self.findBoundry()
        self.X_coord += self.x_speed
        self.Y_coord += self.y_speed
        self.canvas.move(self.ball, self.x_speed, self.y_speed)

    def findBoundry(self):
        # 如果超出界限 就反向运动
        if not self.radius < self.X_coord < self.screenWidth - self.radius:
            self.x_speed = -self.x_speed
        if not self.radius < self.Y_coord < self.screenHeight - self.radius:
            self.y_speed = - self.y_speed


Screen()
