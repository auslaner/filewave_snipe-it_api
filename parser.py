from openpyxl import load_workbook


class SpreadsheetParser:
    def __init__(self, file_location, read_only=True):
        self.file_location = file_location
        self.workbook = load_workbook(self.file_location, read_only=read_only)
