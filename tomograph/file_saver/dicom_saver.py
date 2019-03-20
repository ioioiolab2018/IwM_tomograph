import datetime
import pydicom
from pydicom import Dataset, FileDataset
import os
import time
import numpy as np
from pydicom.data import get_testdata_files


class DICOMSaver:
    def save(self, image: [[float]], filename: str, date: datetime = datetime.datetime.now(), comment: str = ''):
        full_path = os.path.dirname(os.path.abspath(__file__))

        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"
        file_meta.ImplementationClassUID = "1.2.3.4"

        ds = FileDataset(full_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

        ds.PatientName = "Test^Name"
        ds.PatientID = "00-000-000"

        # Set the transfer syntax
        # ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian
        ds.is_little_endian = True
        ds.is_implicit_VR = True

        ds.ContentDate = date.strftime('%Y%m%d')
        ds.ContentTime = date.strftime('%H%M%S.%f')

        ds.PixelData = image.tobytes()
        ds.save_as(filename + '.dcm')

    def save_test(self, pixel_array, filename):
        full_path = os.path.dirname(os.path.abspath(__file__))

        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # 'Secondary Capture Image Storage'
        file_meta.MediaStorageSOPInstanceUID = '1.2.3'
        file_meta.ImplementationClassUID = '1.2.3.4'
        ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)
        filename_s = get_testdata_files("CT_small.dcm")[0]
        ds = pydicom.dcmread(filename_s)

        ds.SOPInstanceUID = '1.3.6.1.4.1.9590.100.1.1.111165684411017669021768385720736873780'
        ds.SOPClassUID = 'Secondary Capture Image Storage'
        ds.ContentDate = str(datetime.date.today()).replace('-', '')
        ds.ContentTime = str(time.time())  # milliseconds since the epoch
        ds.Modality = 'CT'
        ds.StudyInstanceUID = '1.3.6.1.4.1.5962.1.2.1.20040119072730.12322'
        ds.SeriesInstanceUID = '1.3.6.1.4.1.5962.1.3.1.1.20040119072730.12322'
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0
        ds.Columns = pixel_array.shape[0]
        ds.Rows = pixel_array.shape[1]
        ds.Width = pixel_array.shape[0]
        ds.Height = pixel_array.shape[1]
        ds.PixelSpacing = 1

        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15

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

        ds.save_as(filename + '.dcm')

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
