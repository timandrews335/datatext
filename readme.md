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