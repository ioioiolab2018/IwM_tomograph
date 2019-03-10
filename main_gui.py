import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
from matplotlib import cm

from god import God
from skimage import color
import matplotlib.pyplot as plt
from skimage.transform import resize
import numpy as np


class Application(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        master.title("Tomograph")
        master.resizable(width=True, height=True)
        self.master = master

        self.alpha_entry = tk.Entry(self)
        self.arc_length_entry = tk.Entry(self)
        self.detectorc_no_entry = tk.Entry(self)

        self.is_filter = tk.IntVar()
        self.is_iterative = tk.IntVar()
        self.progress = tk.IntVar()

        self.filename = "Paski2.jpg"

        self.run_button = tk.Button(self)
        self.run_inverse_button = tk.Button(self, state=tk.DISABLED)
        self.choose_button = tk.Button(self)
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.cb_is_filter = tk.Checkbutton(self, text="Use filtering", variable=self.is_filter)
        self.cb_is_iterative = tk.Checkbutton(self, text="Auto", variable=self.is_iterative,
                                              command=self.check_iterative)
        self.image = tk.Label(self)
        self.sinogram = tk.Label(self)
        self.inverse_image = tk.Label(self)
        self.transform_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=400)
        self.inverse_slider = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=400)
        self.img = None
        self.sin = None
        self.res = None
        self.create_widgets()
        self.pack()
        self.create_god()

    def create_god(self):
        alpha = 3
        n = 100
        arc_len = 180
        try:
            alpha = float(self.alpha_entry.get())
        except:
            print("zły format alpha")
        try:
            n = int(self.detectorc_no_entry.get())
        except:
            print("zły format alpha")
        try:
            arc_len = int(self.arc_length_entry.get())
        except:
            print("zły format alpha")

        self.god = God(self.filename, n, alpha, arc_len)

    def create_widgets(self):
        # Start  transform button
        self.run_button["text"] = "Run transform"
        self.run_button["command"] = self.run_transform
        self.run_button.grid(row=0, column=0)

        # Start inverse transform button
        self.run_inverse_button["text"] = "Run inverse"
        self.run_inverse_button["command"] = self.run_inverse
        self.run_inverse_button.grid(row=0, column=1)

        # Choose file button
        self.choose_button["text"] = "Choose file"
        self.choose_button["command"] = self.choose_file
        self.choose_button.grid(row=0, column=2)

        # Filter checkbox
        self.cb_is_filter.grid(row=1, column=0)

        self.cb_is_iterative.grid(row=1, column=1)

        # Progress bar
        self.progress.set(0)
        progressbar = ttk.Progressbar(self, maximum=100, variable=self.progress, orient='horizontal',
                                      mode='determinate')  # tworzenie poziomego paska postępu
        progressbar.grid(row=1, column=2)

        # Variables
        tk.Label(self, text="Alpha").grid(row=2, column=0)
        self.alpha_entry.grid(row=3, column=0)
        tk.Label(self, text="Detectors No").grid(row=2, column=1)
        self.detectorc_no_entry.grid(row=3, column=1)
        tk.Label(self, text="Arc length").grid(row=2, column=2)
        self.arc_length_entry.grid(row=3, column=2)

        # Sliders
        self.transform_slider.grid(row=4, column=0, columnspan=3)
        self.transform_slider.bind("<ButtonRelease-1>", self.run_transform)
        self.inverse_slider.grid(row=5, column=0, columnspan=3)

        # Start image
        self.show_image()
        self.image.grid(row=6, column=0, columnspan=3)

        self.sinogram.grid(row=6, column=4, sticky=tk.N)

        # Quit button
        self.quit.grid(row=7, column=0, sticky=tk.E)

    def show_image(self):
        image = Image.open(self.filename)
        self.img = ImageTk.PhotoImage(image)
        self.image.configure(image=self.img)

    def show_sinogram(self, sinogram):
        image = Image.fromarray(np.asarray(sinogram) * 255)
        self.sin = ImageTk.PhotoImage(image)
        self.sinogram.configure(image=self.sin)

    def show_result(self, sinogram):
        # TODO
        print("")
        # image = Image.fromarray(np.uint8(cm.gist_earth(sinogram)*255))
        # self.img = ImageTk.PhotoImage(image)
        # self.image.configure(image=self.img)

    def show_progress(self, progress):
        self.progress.set(progress)

    def check_iterative(self):
        if self.is_iterative.get() == 1:
            self.transform_slider.grid_remove()
            self.inverse_slider.grid_remove()
        else:
            self.transform_slider.grid(row=4, column=0, columnspan=3)
            self.inverse_slider.grid(row=5, column=0, columnspan=3)

    def run_transform(self, __=0):
        end = self.god.iteration_no
        if self.is_iterative.get() == 0:
            end = int(((self.transform_slider.get()) / 100) * self.god.iteration_no)

        for i in range(end):
            self.progress.set((i / end) * 100)
            result = self.god.get_sinogram(i)
            if i % 3 == 0:
                arr2 = np.transpose(result)
                image = resize(arr2, (300, 500))
                self.show_sinogram(image)
                self.master.update()

        self.run_inverse_button.config(state="normal")

    def run_inverse(self):
        print("Inverse transform!")

    def choose_file(self):
        self.filename = filedialog.askopenfilename(initialdir="./", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.show_image()
        self.create_god()


root = tk.Tk()
app = Application(master=root)
app.mainloop()

# im = Image.fromarray(np.uint8(cm.gist_earth(myarray)*255))
