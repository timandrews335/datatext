# datatext
This python script uses a supplied ODBC query and exports the results to a text file, with the option of zipping up that file.

datatext.py must be called with a .json file as it's argument.  The supplied json file contains the database connection and query information, along with the output parameters.

The json file must contain the following information:

{
	"connection_string": "<someconnectionstring>"__
	,"sql_select": "SELECT somedata FROM something WHERE LastUpdated >= '??'"__
	,"use_delta":	true__
	,"delta_connection_string":  "<someconnectionstring>"__
	,"delta_sql_select":  "SELECT MAX(LastUpdated) FROM SomeTable"__
	, "text_file": "<choose a file name>"__
	, "append_timestamp_to_text_file":	true__
	, "text_file_extension":  "csv"__
	, "delimeter": ","__
	, "zip_the_file":	true__

}

connection_string - a valid ODBC connection string pointing to the database to copy the data from__
sql_select - the select query to copy the data from.  An optional delta placeholder may be denoted by double question marks (??)__
use_delta - true or false - choose to swap in a value to extract data incrementally.  As an example "SELECT * FROM SomeTable WHERE LastUpdated >= '??'"__
delta_connection_string - the connection string to the database that delta information will be derived from.  Leave as an empty string if a delta extract is not to be used__
delta_sql_select - the query to select the delta extract information to supply to the data extract select query__
text_file - the name of the text file to write the results to, without the extension__
append_timestamp_to_text_file - true or fale - should the text file receive the current date/time as part of the file name?__
text_file_extension - extension of the results text file, e.g., csv__
delimeter - comma or \t are common examples__
zip_the_file - should the text file be zipped up?__

# example usage:
py datatext.py MySettingsFile.json


-Tim Andrews 2019-11-08