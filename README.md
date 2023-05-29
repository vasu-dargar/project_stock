# Stock-Symbols-Information

Requirements -

1- Python 3 (if possible, latest version)
2- MySQL database with connection to python on system (Link - 'https://dev.mysql.com/downloads/installer/')

Process to start application(on localhost -> http://127.0.0.1:8000/) -

1- Create a database(my_database) in MySQL installed on your system using command 'create database my_database'
   Username - root
   Password - project_stock_pass
2- Navigate to project_stock folder(parent folder) which is downloaded
3- Open cmd in the directory
4- Run command 'py manage.py migrate' in cmd
5- Run command 'py manage.py runserver' in cmd
6- Open any web browser and go to 'http://127.0.0.1:8000/'
7- Use the application

* NOTE -
In some symbols if result is an error saying " Key Error : 'Meta Data' ", kindly refresh the page till result is shown.
This error is due to server providing respective stock symbol information.
