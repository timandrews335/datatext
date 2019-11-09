# datatext
This python script uses a supplied ODBC query and exports the results to a text file, with the option of zipping up that file.

datatext.py must be called with a .json file as it's argument.  The supplied json file contains the database connection and query information, along with the output parameters.

The json file must contain the following information:

{
	"connection_string": "<someconnectionstring>"<br />
	,"sql_select": "SELECT somedata FROM something WHERE LastUpdated >= '??'"<br />
	,"use_delta":	true<br />
	,"delta_connection_string":  "<someconnectionstring>"<br />
	,"delta_sql_select":  "SELECT MAX(LastUpdated) FROM SomeTable"<br />
	, "text_file": "<choose a file name>"<br />
	, "append_timestamp_to_text_file":	true<br />
	, "text_file_extension":  "csv"<br />
	, "delimeter": ","<br />
	, "zip_the_file":	true<br />

}

connection_string - a valid ODBC connection string pointing to the database to copy the data from<br />
sql_select - the select query to copy the data from.  An optional delta placeholder may be denoted by double question marks (??)<br />
use_delta - true or false - choose to swap in a value to extract data incrementally.  As an example "SELECT * FROM SomeTable WHERE LastUpdated >= '??'"<br />
delta_connection_string - the connection string to the database that delta information will be derived from.  Leave as an empty string if a delta extract is not to be used<br />
delta_sql_select - the query to select the delta extract information to supply to the data extract select query<br />
text_file - the name of the text file to write the results to, without the extension<br />
append_timestamp_to_text_file - true or fale - should the text file receive the current date/time as part of the file name?<br />
text_file_extension - extension of the results text file, e.g., csv<br />
delimeter - comma or \t are common examples<br />
zip_the_file - should the text file be zipped up?<br />

# example usage:
py datatext.py MySettingsFile.json


-Tim Andrews 2019-11-08