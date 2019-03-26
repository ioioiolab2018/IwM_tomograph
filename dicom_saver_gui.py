import tkinter as tk

from tomograph import PatientInformation
from tomograph import DICOMSaver


class DicomWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.grab_set()
        self.title("Dicom saver")  # wewnetrzny dostep do wlasnosci okna

        self.filename = tk.StringVar()
        self.name = tk.StringVar()
        self.surname = tk.StringVar()
        self.age = tk.IntVar()
        self.weight = tk.IntVar()
        self.sex = tk.StringVar()

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.name_label = tk.Label(self, text="Name").grid(column=0, row=0)
        self.name_text = tk.Entry(self, textvariable=self.name).grid(column=1, row=0)

        self.sur_name_label = tk.Label(self, text="Surname").grid(column=0, row=1)
        self.surname_text = tk.Entry(self, textvariable=self.surname).grid(column=1, row=1)

        self.age_label = tk.Label(self, text="Age").grid(column=0, row=2)
        self.age_text = tk.Entry(self, textvariable=self.age, validate='key', validatecommand=vcmd).grid(column=1,
                                                                                                         row=2)

        self.weight_label = tk.Label(self, text="Weight", ).grid(column=0, row=3)
        self.weight_text = tk.Entry(self, textvariable=self.weight, validate='key', validatecommand=vcmd).grid(column=1,
                                                                                                               row=3)

        self.sex_label = tk.Label(self, text="Sex").grid(column=0, row=4)
        self.sex_text = tk.Entry(self, textvariable=self.sex).grid(column=1, row=4)

        self.comment_label = tk.Label(self, text="Comment").grid(column=0, row=5)
        self.comment_text_box = tk.Text(self, height=10, width=15)
        self.comment_text_box.grid(column=1, row=5)

        self.filename_label = tk.Label(self, text="Filename").grid(column=0, row=6)
        self.filename_text = tk.Entry(self, textvariable=self.filename).grid(column=1, row=6)

        self.save_button = tk.Button(self, text="Save", command=self.onButton).grid(column=0, row=7)
        self.save_button = tk.Button(self, text="Cancel", command=self.destroy).grid(column=1, row=7)
        self.setVariables()

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def setVariables(self):
        self.filename.set("newFile")
        self.name.set(self.parent.patient.name)
        self.surname.set(self.parent.patient.surname)
        self.age.set(self.parent.patient.age)
        self.weight.set(self.parent.patient.weight)
        self.sex.set(self.parent.patient.sex)
        self.comment_text_box.insert(tk.END, self.parent.patient.comment)

    def onButton(self):
        self.parent.patient = PatientInformation(self.name.get(), self.surname.get(), self.age.get(), self.sex.get(),
                                                 self.weight.get(), self.comment_text_box.get("1.0", tk.END))
        DICOMSaver().save(self.parent.get_result(), self.filename.get(), self.parent.patient)
        self.destroy()
