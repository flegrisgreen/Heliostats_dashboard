# Heliostats Data Dashboard
## Ovierview
* This is a simple dashboard to display data from a heliostat field.
* It is built using Pyhton's Flask framework that is deployed as an app using
Google Cloud Platform's AppEngine service. The data is read for an SQL database that
is also located in the cloud platform.

## Entry point
* main.py is the entry point of the program

## Functionality
* routes.py contains the logic of the web pages
* sql_interface.py is a module used to read data from the database
* dictionary_conversion.py convert the SQL formatted data to dictionary format data
* forms.py contain the code for the web forms
* models.py provides models for forms.py to use
* ploy.py creates a simple plot of the available data
* config_data.py sends an email to an operator based on battery values.

## Notes
* The environment variables that were within the app.yaml have been omitted