import os
import json




def main():
    if os.path.isdir("JsonFiles") == False:
        os.mkdir("JsonFiles")

    os.chdir("JsonFiles")
    for i,k in enumerate(os.listdir(os.getcwd())):
        print "Index: %s,  File: %s "  % (i,k)
   # [print "Index: %s,  File: %s "  % (i,k) in enumerate(os.listdir(os.getcwd()))]
  
    while True:
        file_ = raw_input("Please Enter the file in list above to ingest: ")

        try:
            file_ = int(file_)
            break
        except:
            print "ERROR: Please enter an  integer value.\n"


    file_ = os.listdir(os.getcwd())[file_]

    if "json" in file_.split(".")[-1].lower():
        print "Parsing Json File\n\n"
        json_loader(file_)

def json_loader(x):
    import json
    
    with open(x , "r") as f:
        test = json.loads(f.read())
        #print test

        if isinstance(test, dict):
            top_level = test.keys()
            for top in top_level:
                column_head = str(top)
                print column_head.upper(), top
                
                json_flatten(test[top], column_head, top)            



        elif isinstance(test, list):
            """
           Work on 
            """
            for item in test.values():
                top_level = item.keys()
                               
        
       
        #json_flatten(test, column_head)

       
def json_flatten(y, column_head, top = None):
    
    """
    Utilize Pandas for this. Write each key-value as a column in csv sheet.  Keep track of the key values to write into the csv.
    """

    """
Create a dictionary outside of recursion to keep track of pathing as it iterates through
    """
    ## This method is called within the json loader. It checks if the input variable is a list. If
    ## the input variable is a list. It will loop over the contents of the list applying the same json_flatten element to check for list structure
    column_name = column_head
    if isinstance(y, list):
        for element in y:
            json_flatten(element, column_name)
    ## If the elements of y are a dictionary, it will apply the flattener element in which it will take the dictionary and loop over the items.
    elif isinstance(y, dict):
         #print y.iteritems()
         for i,k in y.iteritems():
            
             if (isinstance(y[i] , dict)) | ( isinstance(y[i] , list)):
                 column_name = column_name + "_"+ str(i)
                 print "Children Found".upper()
                 print "Parent:  %s  ------ Children: %s\n" %(i,k)
                 if isinstance(y[i], list):
                    json_flatten(y[i], column_name)
                 else:
                    json_flatten(y[i], column_name)
             else:
                column_name = column_name + "_"+ str(i)
                print "Column Name: " + column_name
                print "No Children Found".upper()
                print "Parent: %s  ------ Child Node: %s\n" %(i,k)
                column_name = "_".join(column_name.split("_")[:-1])
                
    else:
        column_head = column_head + "_"
        print "Column Name: " + column_head
        print "No Children Found".upper()
        print "Parent: %s  ------ Child Node: %s\n" %(top,y)
        column_name = "_".join(column_name.split("_")[:-1])
            



main()
