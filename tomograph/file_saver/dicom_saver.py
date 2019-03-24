import datetime
import pydicom
from pydicom import Dataset, FileDataset
import os
import time
import numpy as np
from pydicom.data import get_testdata_files
from tomograph import PatientInformation


class DICOMSaver:
    def save(self, image: np.ndarray, filename: str, patient_info: PatientInformation):
        full_path = os.path.dirname(os.path.abspath(__file__))

        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"
        file_meta.ImplementationClassUID = "1.2.3.4"

        ds = FileDataset(full_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

        filename = self.__check_filename(filename)
        self.__set_image_configuration(ds, image.shape[1], image.shape[0], image.max())
        self.__set_patient_information(ds, patient_info)
        self.__set_other_information_tags(ds)

        ds.PixelData = image.tobytes()
        ds.save_as(filename)

    def save_test(self, pixel_array, filename):
        full_path = os.path.dirname(os.path.abspath(__file__))
        filename = self.__check_filename(filename)

        filename_s = get_testdata_files("CT_small.dcm")[0]
        ds = pydicom.dcmread(filename_s)

        # date = datetime.datetime.now()
        #
        # ds.ContentDate = date.strftime('%Y%m%d')
        # ds.ContentTime = date.strftime('%H%M%S.%f')

        ds.SOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
        ds.SOPClassUID = 'Secondary Capture Image Storage'
        ds.ContentDate = str(datetime.date.today()).replace('-', '')
        ds.ContentTime = str(time.time())  # milliseconds since the epoch
        ds.StudyInstanceUID = '1.3.6.1.4.1.5962.1.2.1.20040119072730.12322'
        ds.SeriesInstanceUID = '1.3.6.1.4.1.5962.1.3.1.1.20040119072730.12322'
        ds.Modality = 'CT'
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0

        ds.Columns = pixel_array.shape[1]
        ds.Rows = pixel_array.shape[0]
        ds.Width = pixel_array.shape[1]
        ds.Height = pixel_array.shape[0]

        ds.PixelSpacing = 1
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15

        # ds.is_little_endian = True
        # ds.is_implicit_VR = True

        # ds.PixelPaddingValue = -2000
        # ds.RescaleIntercept = -1024
        # ds.RescaleSlope = 1

        # ds.SecondaryCaptureDeviceManufctur = 'Python 2.7.3'

        # These are the necessary imaging components of the FileDataset object.
        # ds.SmallestImagePixelValue = b'\\x00\\x00'
        # ds.LargestImagePixelValue = b'\\xff\\xff'

        # if pixel_array.dtype != np.uint16:
        #     pixel_array = pixel_array.astype(np.uint16)
        print(pixel_array)
        print(max([max(sublist) for sublist in pixel_array]))
        ds.PixelData = pixel_array.tobytes()

        ds.save_as(filename)

        # t_ds = pydicom.dcmread('test.dcm')
        # print(t_ds)
        # return ds.pixel_array

    def test(self, pixel_array, new_filename):
        filename = get_testdata_files("CT_small.dcm")[0]
        ds = pydicom.dcmread(filename)
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0
        ds.Columns = pixel_array.shape[0]
        ds.Rows = pixel_array.shape[1]
        ds.Width = pixel_array.shape[0]
        ds.Height = pixel_array.shape[1]
        ds.PixelData = pixel_array.tobytes()
        ds.save_as(new_filename)

        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7

    @staticmethod
    def __check_filename(filename: str):
        if '.dcm' not in filename:
            filename += '.dcm'
        return filename

    @staticmethod
    def __set_image_configuration(ds, width: int, height: int, largest_pixel_value: int):
        ds.Modality = 'CT'
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0

        ds.Columns = width
        ds.Rows = height
        ds.Width = width
        ds.Height = height

        ds.PixelSpacing = 1
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15

        # ds.PixelPaddingValue = '-2000'
        # ds.RescaleIntercept = '-1024'
        ds.RescaleSlope = 1

        # ds.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'

        # ds.is_little_endian = True
        # ds.is_implicit_VR = True

        # ds.SmallestImagePixelValue = 0
        # ds.LargestImagePixelValue = largest_pixel_value

        # ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian

    @staticmethod
    def __set_patient_information(ds: FileDataset, info: PatientInformation):
        ds.PatientName = info.name + ' ' + info.surname
        ds.PatientAge = str(info.age)
        ds.PatientSex = info.sex
        ds.PatientWeight = str(info.weight)
        ds.AdditionalPatientHistory = info.comment

        # ds.PatientName = "Test^Name"
        # ds.PatientID = "00-000-000"
        # ds.PatientBirthDate

    @staticmethod
    def __set_other_information_tags(ds: FileDataset):
        date = datetime.datetime.now()

        ds.ContentDate = date.strftime('%Y%m%d')
        ds.ContentTime = date.strftime('%H%M%S.%f')
        ds.SeriesInstanceUID = '1.3.6.1.4.1.5962.1.3.1.1.20040119072730.12322'
        ds.SOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
        ds.SOPClassUID = 'Secondary Capture Image Storage'
        ds.StudyInstanceUID = '1.3.6.1.4.1.5962.1.2.1.20040119072730.12322'
        # ds.SecondaryCaptureDeviceManufctur = 'Python 2.7.3'

    def open(self, path: str):
        ds = pydicom.dcmread(path)
        patient_information = self.__get_patient_information(ds)
        image = ds.pixel_array
        return image, patient_information

    @staticmethod
    def __get_patient_information(ds: Dataset):
        name, surname = ds.PatientName.split()
        return PatientInformation(name, surname, ds.PatientAge, ds.PatientSex, ds.PatientWeight,
                                  ds.AdditionalPatientHistory)
