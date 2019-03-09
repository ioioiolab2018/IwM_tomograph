import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image


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

        self.filename = "Kropka.jpg"

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
        self.inverse_slider.grid(row=5, column=0, columnspan=3)

        # Start image

        self.show_image()
        self.image.grid(row=6, column=0, columnspan=3)

        # Quit button
        self.quit.grid(row=7, column=0, stick=tk.E)

    def show_image(self):
        image = Image.open(self.filename)
        self.img = ImageTk.PhotoImage(image)
        self.image.configure(image=self.img)

    def show_sinogram(self, sinogram):
        # TODO
        print("")
        # image = Image.fromarray(np.uint8(cm.gist_earth(sinogram)*255))
        # self.img = ImageTk.PhotoImage(image)
        # self.image.configure(image=self.img)

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

    def run_transform(self):
        for i in range(9999):
            self.progress.set((i / 9999) * 100)
            a = 99999 / 190.99
            self.master.update()
        if self.is_filter.get() == 1:
            print("Filtrowanie")
        print("Radon transform!")
        self.run_inverse_button.config(state="normal")

    def run_inverse(self):
        print("Inverse transform!")

    def choose_file(self):
        self.filename = filedialog.askopenfilename(initialdir="./", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.show_image()


root = tk.Tk()
app = Application(master=root)
app.mainloop()

# im = Image.fromarray(np.uint8(cm.gist_earth(myarray)*255))
