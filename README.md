# TransformationScript

Purpose: 
Script to intake files of various formats and transform them into csv format for ingestion into HDFS. 

Scripts: 

The complete script is DataTransform_P2.py. The dependencies for the script can be found in python_dependencies_python2. These packages are the standard packages included in the Anaconda 2 distribution.


Directions for Use: 
Pass in the file as the last argument from the command line to transform the data into a csv. It will flatten all all structures of the data.

Example Statement: 

python DataTransform_P2.py testfile.xlsx

Ignore: 
- data_script_p3 folder: This is a directory for a python 3 environment. Will continue work for developing in python 3. 
- json_test.py: This is a file I created to test out json functionality
- xmltest.py: This is a file I created to test out xml functionality
- remote: Github remote names across workstations
- python_env.txt: Reminder of development environment for python 2.
