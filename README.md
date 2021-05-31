## Background and Approaches taken

This application works through the use of a Django backend, combined with a PostgreSQL database. I created a database with the location, technician, and work_orders tables, using the provided csv files. Reading of the files was done by the csv library and is done on each page reload; to avoid creating objects every time, I used Django's get_or_create function, which simply gets the database object if it exists already (for example - if technician Alice Jones already exists, the webpage simply retrives and discards it).

Using Django templates, I passed the database objects to the html file, created a table with it, and used jQuery to calculate the time between shifts for technicians.

## HOW TO USE

1. Initialize a postgreSQL database and server on your computer
2. Download the source code and set database credentials in settings.py using environment variables
3. Make sure you have a csvs folder with the location, technicians, and work_orders csv files inside the scheduler directory (scheduler/csvs/locations.csv, technicians.csv, etc). The file names must match exactly.
4. Type the command python manage.py runserver to start the webserver and navigate to localhost:8000
