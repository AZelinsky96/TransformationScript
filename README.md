# TransformationScript

Purpose: 
	Script to intake files of various formats and transform them into csv format for ingestion into HDFS. 

Scripts: 

	There are two scripts available. DataTransform_p3.py and DataTransform_p2.py. Each of the two scripts are setup for python3 and python2 respec	      tively. Each have their own set of dependencies found within python_dependencies_python(2/3)

Directions for Use: 
	Pass in the file as the last argument from the command line to transform the data into a csv. It will flatten all all structures of the data.
