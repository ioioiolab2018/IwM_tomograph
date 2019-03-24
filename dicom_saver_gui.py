import tkinter as tk


class DicomWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Child")  # wewnetrzny dostep do wlasnosci okna

        tk.Button(self, text="Otworz okno Child z okna Child", command=self.onButton).grid()

    def onButton(self):
        self.child = DicomWindow(self)  # przekazanie okna jako rodzica
