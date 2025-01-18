from test.utils.data_file import DataFile
from test import FEATURE_DIR

class AppointmentData:
    @staticmethod
    def get_appointment_data(sheet_name="Sheet1"):
        excel_path = f"{FEATURE_DIR}/data_files/excel/appointment_data.xlsx"
        return DataFile.read_excel(excel_path, sheet_name)