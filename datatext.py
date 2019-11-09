import pyodbc
import platform
import json
import sys
import os
from zipfile import ZipFile
from datetime import datetime

'''
# datatext
This python script uses a supplied ODBC query and exports the results to a text file, with the option of zipping up that file.

datatext.py must be called with a .json file as it's argument.  The supplied json file contains the database connection and query information, along with the output parameters.

The json file must contain the following information:

{
	"connection_string": "<someconnectionstring>"
	,"sql_select": "SELECT somedata FROM something WHERE LastUpdated >= '??'"
	,"use_delta":	true
	,"delta_connection_string":  "<someconnectionstring>"
	,"delta_sql_select":  "SELECT MAX(LastUpdated) FROM SomeTable"
	, "text_file": "<choose a file name>"
	, "append_timestamp_to_text_file":	true
	, "text_file_extension":  "csv"
	, "delimeter": ","
	, "zip_the_file":	true

}

connection_string - a valid ODBC connection string pointing to the database to copy the data from
sql_select - the select query to copy the data from.  An optional delta placeholder may be denoted by double question marks (??)
use_delta - true or false - choose to swap in a value to extract data incrementally.  As an example "SELECT * FROM SomeTable WHERE LastUpdated >= '??'"
delta_connection_string - the connection string to the database that delta information will be derived from.  Leave as an empty string if a delta extract is not to be used
delta_sql_select - the query to select the delta extract information to supply to the data extract select query
text_file - the name of the text file to write the results to, without the extension
append_timestamp_to_text_file - true or fale - should the text file receive the current date/time as part of the file name?
text_file_extension - extension of the results text file, e.g., csv
delimeter - comma or \t are common examples
zip_the_file - should the text file be zipped up?

# example usage:
py datatext.py MySettingsFile.json


-Tim Andrews 2019-11-08

'''

#variables needed for input
connection_string = ""
sql_select = ""
use_delta = False
delta_connection_string = ""
delta_sql_select = ""
delta_value = ""
text_file = ""
text_file_extension = ""
delimeter = ""
line_string = ""
zip_the_file = False
current_time = datetime.now()

#helper functions
def qualifier(column_type):
    qual = ""
    if(str(column_type) == "<class 'str'>"):
        qual = '"'
    return qual

#basically, this doubles up the double quotes if the column has a double quote in it    
def qualify_column(column_type, column):
    val = column
    if(str(column_type) == "<class 'str'>"):
        val = val.replace('"', '""')
    return val


#misc variables
counter = 0
column_types = []

#Our json file should be the first and only argument (other than the python code file)
try:
    json_file = open(sys.argv[1],"r") 
    json_args = json.loads(json_file.read())
    sql_select = json_args['sql_select']
    text_file = json_args['text_file']
    if(json_args['append_timestamp_to_text_file']):
        text_file = text_file + str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "-" + str(current_time.hour) + "-" + str(current_time.minute) + "-" + str(current_time.second)
    text_file = text_file + "." + json_args['text_file_extension']
    delimeter = json_args['delimeter']
    connection_string = json_args['connection_string']
    zip_the_file = json_args['zip_the_file']
    use_delta = json_args['use_delta']
    delta_connection_string = json_args['delta_connection_string']
    delta_sql_select = json_args['delta_sql_select']  
    json_file.close()
except:
    print("you must supply a properly formatted json file as an argument.")
    sys.exit()
   
#open the results text file
results_file = open(text_file, "w")

#connect to the management database to grab the delta value to pass into the source query
if(use_delta):
    conn_delta = pyodbc.connect(delta_connection_string)
    curs_delta = conn_delta.cursor()
    delta_value = str(curs_delta.execute(delta_sql_select).fetchval())
    curs_delta.close()
    conn_delta.close()
    #Swap in the delta_value
    sql_select = sql_select.replace("??", delta_value)

#connect to the database
conn = pyodbc.connect(connection_string)
curs = conn.cursor()
curs.execute(sql_select)

#write out the header
line_string = ""
for desc in curs.description:
    line_string = line_string + desc[0]
    column_types.append(desc[1])
    line_string = line_string + delimeter
#take off the final delimeter
line_string = line_string[0:len(line_string)-1]
results_file.write(line_string)
results_file.write("\n")

#write out the data
for row in curs.fetchall():
    line_string = ""
    counter = 0
    for column in row:
        line_string = line_string + qualifier(column_types[counter]) + qualify_column(column_types[counter], str(column)) +  qualifier(column_types[counter]) + delimeter
        counter = counter + 1
    line_string = line_string[0:len(line_string)-1]     
    results_file.write(line_string)
    results_file.write("\n")
    
#cleanup
results_file.close()
curs.close()
conn.close()
    
#Zip up the file that we just created
if(zip_the_file):
    with ZipFile(text_file + ".zip","w", 8) as zip: 
        zip.write(text_file) 
        os.remove(text_file)
    

