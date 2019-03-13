import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
from god import God
from skimage.transform import resize
from skimage.util import img_as_ubyte
from skimage.util import img_as_float
import numpy as np
from skimage import data
from skimage.util.dtype import dtype_range
from skimage import exposure

import matplotlib.pyplot as plt

import numpy as np

class Application(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        master.title("Tomograph")
        master.resizable(width=True, height=True)
        self.master = master

        self.alpha_var = tk.StringVar()
        self.arc_len_var = tk.StringVar()
        self.detector_no_var = tk.StringVar()

        self.alpha_entry = tk.Entry(self, textvariable=self.alpha_var)
        self.arc_length_entry = tk.Entry(self, textvariable=self.arc_len_var)
        self.detectors_no_entry = tk.Entry(self, textvariable=self.detector_no_var)

        self.is_filter = tk.IntVar()
        self.is_iterative = tk.IntVar()
        self.progress = tk.IntVar()

        self.filename = "images/Paski2.jpg"

        self.run_button = tk.Button(self)
        self.run_inverse_button = tk.Button(self, state=tk.DISABLED)
        self.choose_button = tk.Button(self)
        self.update_variables_button = tk.Button(self, text="Update Variables", command=self.update_variables)

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
        self.god = None
        self.create_widgets()
        self.pack()
        self.update_variables()

    def create_widgets(self):
        # set variables
        self.arc_len_var.set("180")
        self.alpha_var.set("0.9")
        self.detector_no_var.set("100")

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
        self.detectors_no_entry.grid(row=3, column=1)
        tk.Label(self, text="Arc length").grid(row=2, column=2)
        self.arc_length_entry.grid(row=3, column=2)
        self.update_variables_button.grid(row=3, column=4, sticky=tk.W)

        # Sliders
        self.transform_slider.grid(row=4, column=0, columnspan=3)
        self.transform_slider.bind("<ButtonRelease-1>", self.run_transform)
        self.inverse_slider.grid(row=5, column=0, columnspan=3)
        self.inverse_slider.bind("<ButtonRelease-1>", self.run_inverse)
        # Start image
        self.show_image()
        self.image.grid(row=6, column=0, columnspan=3)

        self.sinogram.grid(row=6, column=4, sticky=tk.N)
        self.inverse_image.grid(row=6, column=5, sticky=tk.N)

        # Quit button
        self.quit.grid(row=7, column=0, sticky=tk.E)

    def update_variables(self):
        alpha = 3
        n = 100
        arc_len = 180
        try:
            alpha = float(self.alpha_var.get())
        except:
            print("zły format alpha")
        try:
            n = int(self.detector_no_var.get())
        except:
            print("zły format alpha")
        try:
            arc_len = int(self.arc_len_var.get())
        except:
            print("zły format alpha")

        self.god = God(self.filename, n, alpha, arc_len)

    def show_image(self):
        image = Image.open(self.filename)
        self.img = ImageTk.PhotoImage(image)
        self.image.configure(image=self.img)

    def show_sinogram(self, sinogram):
        image = Image.fromarray(np.asarray(sinogram) * 255)
        self.sin = ImageTk.PhotoImage(image)
        self.sinogram.configure(image=self.sin)

    def show_result_image(self, sinogram):
        image = Image.fromarray(np.asarray(sinogram) * 255)
        self.res = ImageTk.PhotoImage(image)
        self.inverse_image.configure(image=self.res)

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

        for i in range(0, end):
            self.progress.set((i / end) * 100)
            result = self.god.get_sinogram(i)
            result = np.transpose(result)
            result = resize(result, (200, 400))
            self.show_sinogram(result)
            self.master.update()
        self.show_progress(0)
        self.run_inverse_button.config(state="normal")

    def run_inverse(self, __=0):
        end = self.god.iteration_no
        if self.is_iterative.get() == 0:
            end = int(((self.inverse_slider.get()) / 100) * self.god.iteration_no)

        for i in range(1, end):
            self.progress.set((i / end) * 100)
            result = self.god.get_inverse_result(i)
            result = np.transpose(result)
            # result=img_as_ubyte(result)
            # print(np.min(result), np.max(result))
            # p2 = np.percentile(result, 10)
            # p98 = np.percentile(result, 99)
            # result = exposure.rescale_intensity(result, in_range=(p2, p98))
            # result = img_as_float(result)
            self.show_result_image(result)
            self.master.update()
        self.show_progress(0)
        self.run_inverse_button.config(state="normal")

    def choose_file(self):
        self.filename = filedialog.askopenfilename(initialdir="./", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.show_image()
        self.update_variables()


root = tk.Tk()
app = Application(master=root)
app.mainloop()
