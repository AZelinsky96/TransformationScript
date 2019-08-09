import sys 
import json
import csv
import os
##
# Convert to string keeping encoding in mind...
##

def to_string(s):
    try:
        return str(s)
    except:
        #Change the encoding type if needed
        return s.encode('utf-8')


##
# This function converts an item like
# {
#   "item_1":"value_11",
#   "item_2":"value_12",
#   "item_3":"value_13",
#   "item_4":["sub_value_14", "sub_value_15"],
#   "item_5":{
#       "sub_item_1":"sub_item_value_11",
#       "sub_item_2":["sub_item_value_12", "sub_item_value_13"]
#   }
# }
# To
# {
#   "node_item_1":"value_11",
#   "node_item_2":"value_12",
#   "node_item_3":"value_13",
#   "node_item_4_0":"sub_value_14",
#   "node_item_4_1":"sub_value_15",
#   "node_item_5_sub_item_1":"sub_item_value_11",
#   "node_item_5_sub_item_2_0":"sub_item_value_12",
#   "node_item_5_sub_item_2_0":"sub_item_value_13"
# }
##
def reduce_item(key, value):
    global reduced_item

    #Reduction Condition 1
    if type(value) is list:
        i=0
        for sub_item in value:
            reduce_item(key+'_'+to_string(i), sub_item)
            i=i+1

    #Reduction Condition 2
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key+'_'+to_string(sub_key), value[sub_key])

    #Base Condition
    else:
        reduced_item[to_string(key)] = to_string(value)


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print "No Four arguments"
    #    print "\nUsage: python json_to_csv.py <node> <json_in_file_path> <csv_out_file_path>\n"
    else:
        #Reading arguments
        #node = sys.argv[1]
        #json_file_path = sys.argv[2]
        os.chdir("DataFiles")
        for i,k in enumerate(os.listdir(os.getcwd())):
            print "Index: %s,  File: %s "  % (i,k)

        while True:
            file_ = raw_input("Please Enter the file in list above to ingest: ")

            try:
                file_ = int(file_)
                break
            except:
                print "ERROR: Please enter an  integer value.\n"


        json_file_path = os.listdir(os.getcwd())[file_]

        #csv_file_path = sys.argv[3]

        fp = open(json_file_path, 'r')
        json_value = fp.read()
        raw_data = json.loads(json_value)
        fp.close()

        try:
            data_to_be_processed = raw_data[node]
        except:
            data_to_be_processed = raw_data

        processed_data = []
        header = []
        #print data_to_be_processed
        for item in data_to_be_processed:
            print item
            reduced_item = {}
            node = item
            reduce_item(node, data_to_be_processed[item])
            header += reduced_item.keys()
            #print header
            processed_data.append(reduced_item)
        #print processed_data





        header = list(set(header))
        header.sort()
        print processed_data
        with open("%s.csv" % (json_file_path.split(".")[0]), 'w+') as f:
            writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)
