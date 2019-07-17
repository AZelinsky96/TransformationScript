"""
Purpose: The primary objective of this program is to intake a file and convert the
file into an ingestible csv file.

Created by: Anthony Zelinsky
Modified: 7/15/19


"""


import os
import sys
import re
import csv

class FileLoader:
    def __init__(self):
        self.file_ = sys.argv[-1]
    def LoadFile(self):

        file_extension = sys.argv[-1].split(".")[-1]
        if "xlsx" == file_extension.lower().strip():
            self.file_type = "xlsx"
            print("File Entered:",self.file_)
            confirm_ = input("Please Confirm the file entered is correct: [y/n]")
        else:
            print("Please upload the correct file as last arg. \nYou entered: {}".format(self.file_))


    def FileSplitter(self):
        if self.file_type == "xlsx":
            FileLoader.XlsxSplitter(self.file_)

        if self.file_type == "xls":
            FileLoader.XlsSplitter(self.file_)




    ## Static Methods
    @staticmethod
    def XlsxSplitter(x):
        import openpyxl as xl
        print("Parsing xlsx file.")

        wb = xl.load_workbook(x)
        sheet_names = wb.sheetnames
        for i in sheet_names:
            sheet = wb[i]
            with open("{}.csv".format(sheet.title), "w", newline = "") as f:
                writer = csv.writer(f)
                for rows in sheet.rows:
                    writer.writerow([cell.value for cell in rows])

            print("Processed Sheet: {}".format(sheet.title))
        #print(x)

    @staticmethod
    def XlsSplitter(x):
        print(x)

    @staticmethod
    def TextFileProcessor(x):
        print(x)

    @staticmethod
    def JsonProcessor(x):
        print(x)

    @staticmethod
    def XMLProcessor(x):
        print(x)

    @staticmethod
    def PdfProcessor(x):
        print(x)



def main():

    fileloader = FileLoader()

    fileloader.LoadFile()
    fileloader.FileSplitter()


if __name__ == "__main__":
    main()
