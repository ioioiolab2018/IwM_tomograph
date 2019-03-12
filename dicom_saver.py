import datetime
import pydicom
import os


class DICOMSaver:
    def save(self, image: [[float]], filename: str, date: datetime = datetime.datetime.now(), comment: str = ''):
        full_path = os.path.dirname(os.path.abspath(__file__))

        file_meta = pydicom.Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"
        file_meta.ImplementationClassUID = "1.2.3.4"

        ds = pydicom.FileDataset(full_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

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
