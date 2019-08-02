#!/home/anthonyz/anaconda2/bin/python



import os
import sys
import re
import csv
import shutil
import warnings




class FileLoader:
    def __init__(self):
        self.file = sys.argv[-1].strip()

    def LoadFile(self):
        self.file_type = self.file.split(".")[-1]
        print "File Entered: %s" %(self.file)

        while True:
            confirm_ = raw_input("Please Confirm the file entered is correct: [y/n]")


            if confirm_.lower() == "y":
                break
            elif confirm_.lower() == "n":
                print("Please upload the correct file as last arg. \nYou entered: {}".format(self.file))
                sys.exit()
            else:
                print("Please enter either [y/n]...\n")


    def MakeDirectory(self):
        base = os.getcwd()
        directory_contents = os.listdir(base)
        folder_name = self.file.split(".")[0]
        if os.path.isdir(base + "/" + folder_name) == False:
            os.mkdir(folder_name)
        shutil.copy(self.file, folder_name)
        os.chdir(folder_name)

    def FileSplitter(self):
        print "Loading: %s" % (self.file)
        if self.file_type == "xlsx":
            FileLoader.XlsxSplitter(self.file)
        elif self.file_type == "xls":
            FileLoader.XlsSplitter(self.file)
        elif self.file_type == ".json":
            FileLoader.JsonLoader(self.file)
        else:
            print "Please Check Documentation and ensure that data file is compatible with load types."

    @staticmethod
    def XlsxSplitter(x):
        import openpyxl as xl
        print "Parsing xlsx file."

        wb = xl.load_workbook(x)
        sheet_names = wb.sheetnames

        for i in sheet_names:
            sheet = wb[i]
            with open("%s.csv" % (sheet.title), "w") as f:
                for rows in sheet.rows:
                    row = [cell.value for cell in rows]

                    line_ = ",".join(list(map(FileLoader.mapper, row))).encode("utf-8", "ignore")
                    line_ = " ".join(line_.split("\n"))
                    #print line_

                    f.write(line_ + "\n")
            print "Processed Sheet: %s" % (sheet.title)


    @staticmethod
    def XlsSplitter(x):
        import xlrd
        print "Parsing Xls File."
        wb = xlrd.open_workbook(x)
        for i,k in enumerate(wb.sheet_names()):
            sheet = wb.sheet_by_index(i)
            with open("%s.csv" % (k), "w") as f:
                for row in range(sheet.nrows):


                    line_ = ",".join(list(map(FileLoader.mapper, sheet.row_values(row)))).encode("utf-8", "ignore")
                    line_ = " ".join(line_.split("\n"))
                    f.write(line_ + "\n")

            print "Processed Sheet: %s" % (k)

    @staticmethod
    def mapper(x):
        if ("float" in str(type(x))) | ("int" in str(type(x))): return str(x)
        elif "None" in str(type(x)): return ""
        else: return x.strip().replace(u"\n", "").replace(u"\\xa0", u"").replace(",", "")


    @staticmethod
    def JsonLoader(x):
        import json
        print "Parsing Json File."

        with open(x , "r") as f:
            data = json.load(f)


def main():

    fileloader = FileLoader()
    fileloader.LoadFile()
    fileloader.MakeDirectory()

    fileloader.FileSplitter()
main()
