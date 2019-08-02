## Python 3 script
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
import shutil

class FileLoader:
    def __init__(self):
        self.file_ = sys.argv[-1]
    def LoadFile(self):

        file_extension = sys.argv[-1].split(".")[-1]
        self.file_type = file_extension
        print("File Entered:",self.file_)

        while True:
            confirm_ = input("Please Confirm the file entered is correct: [y/n]")


            if confirm_.lower() == "y":
                break
            elif confirm_.lower() == "n":
                print("Please upload the correct file as last arg. \nYou entered: {}".format(self.file_))
                sys.exit()
            else:
                print("Please enter either [y/n]...\n")


    def MakeDirectory(self):
        dir_contents = os.listdir()
        dir_name = self.file_.split(".")[0]
        if os.path.isdir(dir_name) == False:
            os.mkdir(dir_name)
        shutil.copy(self.file_, dir_name)
        os.chdir(dir_name)



    def FileSplitter(self):
        if self.file_type == "xlsx":
            FileLoader.XlsxSplitter(self.file_)

        elif self.file_type == "xls":
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
        import xlrd
        print("Parsing xls file.")
        wb = xlrd.open_workbook(x)
        for i,k in enumerate(wb.sheet_names()):
            sheet = wb.sheet_by_index(i)
            with open("{}.csv".format(k), "w", newline = "") as f:
                writer = csv.writer(f)
                for row in range(sheet.nrows):
                    writer.writerow(sheet.row_values(row))

            print("Processed Sheet: {}".format(k))

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
    ## Instatiating the class
    fileloader = FileLoader()
    ## Loading in the file from arguments
    fileloader.LoadFile()
    ## Checking if directory is made, if not, making it
    fileloader.MakeDirectory()
    ## Splitting the file and saving as csv
    fileloader.FileSplitter()


if __name__ == "__main__":
    main()
