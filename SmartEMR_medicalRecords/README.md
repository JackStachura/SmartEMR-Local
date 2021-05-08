# Medical Records
The information in this file is to create the database. This file also includes a python file to run to generate the data for the database.
# MySQL
Have MySQL version 8.0 installed.
Create a new database an example is:
```
CREATE DATABASE medicalRecords
```

# SQL Data generator
Make sure to have python3 installed as well as the following library
```
pip3 install mysql-connector-pytho
```
To insert into the database change SQL_DB_generator.py
```
Line 14: Add_to_db = False
```
to
```
Line 14: Add_to_db = True
```

To generate multiple patients, change
```
Line 15: num_of_patient = 1
```
1 to the number of patients you would like to generate.

If Add_to_db is set to true make sure that
```
Line 48: cnx = mysql.connector.connect(user='root', password='', host='localhost', database='medicalRecords')
```
matches your SQL information
