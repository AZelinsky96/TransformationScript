#!/home/anthonyz/anaconda2/bin/python



import os
import sys
import re
import csv
import shutil
import warnings




class FileLoader:
    """
    This class will handle all interactions for parsing, splitting, and flattening files.
    This is instatianted in main and main is executed.
    """

    def __init__(self):
        ## Input file in instatiantion is the the last system argument passed to the command line
        self.file = sys.argv[-1].strip()


    def LoadFile(self):
        """
        This method will find the file type of the input file, and search if the file is not located within the current directory.
        If the file is not located within the current directory, there is an option to search the subdirectories from the current to see if the file is there.
        """
        def finder(name, path):
            """
            The function to search the directories for presence of file.
            """
            for root, dirs, files in os.walk(path):
                if name in files:
                    return os.path.join(root, name)


        self.file_type = self.file.split(".")[-1]
        print "File Entered: %s" %(self.file)

        while True:
            """
            Confirmation of file entered.

            """
            confirm_ = raw_input("Please Confirm the file entered is correct: [y/n]")

            if confirm_.lower() == "y":
                break
            elif confirm_.lower() == "n":
                print("Please upload the correct file as last arg. \nYou entered: {}".format(self.file))
                sys.exit()
            else:
                print("Please enter either [y/n]...\n")


        if self.file not in os.listdir(os.getcwd()):
            """
            Confirmation of file presence. Will perform search if chosen to do so.

            """

            print "File not in directory.: %s" % (os.getcwd())

            while True:

                find = raw_input("Would you like to search for file? [y/n] ")
                if find.lower() == "y":
                    while True:
                        location_c = str(raw_input("Would you like to search sub directories[1] or enter directory path[2]? - [1/2]: "))

                        if location_c == "1":
                            file_loc = finder(self.file, os.getcwd())
                            break
                        elif location_c == "2":

                            path_ = raw_input("Enter Path to File: ")
                            if self.file in os.listdir(path_):
                                file_loc = os.path.join(path_, self.file)

                                break

                            else:
                                sys.exit("File not found in directory: %s. \nPlease Check directory and it's contents, or move file to current directory.\n" % (path_))
                        else:
                            print "Please enter either [1/2] \n"

                    self.file =  file_loc

                    break

                elif find.lower() == "n":
                    sys.exit("Please move file to current directory")
                else:
                    print "Please enter either [y/n]\n"




    def MakeDirectory(self):
        base = os.getcwd()
        directory_contents = os.listdir(base)
        folder_name = self.file.split(".")[0]
        print folder_name
        if os.path.isdir(os.path.join(base,folder_name)) == False:
            os.mkdir(folder_name)
        folder_name = os.path.join(base, folder_name)
        shutil.copy(self.file, folder_name)

        os.chdir(folder_name)



    def FileSplitter(self):
        print "Loading: %s" % (self.file)
        print self.file_type

        if self.file_type == "xlsx":
            FileLoader.XlsxSplitter(self.file)
        elif self.file_type == "xls":
            FileLoader.XlsSplitter(self.file)
        elif self.file_type == "json":
            FileLoader.JsonLoader(self.file)
        elif self.file_type == "xml":
            FileLoader.XmlParser(self.file)
        else:
            print "Please Check Documentation and ensure that data file is compatible with load types."




## Static methods to handle different file inputs
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
        print os.getcwd()
        file = x

        global reduced_item

        def to_string(s):
            try:
                return str(s)
            except:
        #Change the encoding type if needed
                return s.encode('utf-8')

        def reduce(key, value):
            if isinstance(value, list):
                i = 0
                for sub in value:
                    reduce(key+'_'+to_string(i), sub)
                    i+= 1
            elif isinstance(value, dict):
                sub_keys = value.keys()
                for sub_key in sub_keys:
                    reduce(key+'_'+to_string(sub_key), value[sub_key])
            else:
                reduced_item[to_string(key)] = to_string(value)


        if len(file) == 0:
            sys.exit("Please Enter file.")
        else:

            fp = open(file, "r")
            json_value = fp.read()
            raw_data = json.loads(json_value)
            fp.close()
            data_to_be_processed = raw_data

            processed_data = []
            header = []

            for item in data_to_be_processed:
                print "Processing %s Branch" % (item)
                reduced_item = {}
                node = item
                reduce(node, data_to_be_processed[item])
                header += reduced_item.keys()

                processed_data.append(reduced_item)

            header = list(set(header))
            header.sort()
            data = {}
            for i in processed_data:
                for j,k  in i.iteritems():
                    data[j] = k

            #print data

            with open("%s.csv" % (sys.argv[-1].split(".")[0]), "w+") as f:
                writer = csv.DictWriter(f, header , quoting = csv.QUOTE_ALL)
                writer.writeheader()
                print "Writing Data to CSV"
                writer.writerow(data)


    @staticmethod
    def XmlParser(x):
        import xml.etree.ElementTree
        global reduced_item

        def internal_iter(tree, accum):
            """Recursively iterate through the elements of the tree accumulating
                a dictionary result.

                :param tree: The XML element tree
                :type tree: xml.etree.ElementTree
                :param accum: Dictionary into which data is accumulated
                :type accum: dict
                :rtype: dict
            """
            if tree is None:
                return accum

            if tree.getchildren():
                accum[tree.tag] = {}
                for each in tree.getchildren():
                    result = internal_iter(each, {})
                    if each.tag in accum[tree.tag]:
                        if not isinstance(accum[tree.tag][each.tag], list):
                            accum[tree.tag][each.tag] = [
                                accum[tree.tag][each.tag]
                            ]
                        accum[tree.tag][each.tag].append(result[each.tag])
                    else:
                        accum[tree.tag].update(result)
            else:
                accum[tree.tag] = tree.text

            return accum


        def DictParser(data_to_be_processed):
            def to_string(s):
                try:
                    return str(s)
                except:
                    return s.encode('utf-8')

            def reduce(key, value):
                if isinstance(value, list):
                    i = 0
                    for sub in value:
                        reduce(key+'_'+to_string(i), sub)
                        i+= 1
                elif isinstance(value, dict):
                    sub_keys = value.keys()
                    for sub_key in sub_keys:
                        reduce(key+'_'+to_string(sub_key), value[sub_key])
                else:
                    reduced_item[to_string(key)] = to_string(value)




            processed_data = []
            header = []

            for item in data_to_be_processed:
                print "Processing %s Branch" % (item)
                reduced_item = {}
                node = item
                reduce(node, data_to_be_processed[item])
                header += reduced_item.keys()

                processed_data.append(reduced_item)

            header = list(set(header))
            header.sort()
            data = {}
            for i in processed_data:
                for j,k  in i.iteritems():
                    data[j] = k
            #print data
            with open("%s.csv" % (sys.argv[-1].split(".")[0]), "w+") as f:
                writer = csv.DictWriter(f, header , quoting = csv.QUOTE_ALL)
                writer.writeheader()
                print "Writing Data to CSV"
                writer.writerow(data)


        print "Loading XML File"

        with open(x, "r") as f:
            xml_string = f.read()


        data_to_be_processed = internal_iter(xml.etree.ElementTree.fromstring(xml_string), {})
        DictParser(data_to_be_processed)



def main():

    fileloader = FileLoader()
    fileloader.LoadFile()
    fileloader.MakeDirectory()
    fileloader.FileSplitter()



main()
