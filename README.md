# project_stock

Requirements -

1- Python 3 (if possible, latest version) with pip
2- Install python library requests
3- MySQL database with  python connector (Link - 'https://dev.mysql.com/downloads/windows/installer/8.0.html') and mysqlclient (pip install mysqlclient)
4- Install Django using command 'pip install Django' on cmd

Process to start application(on localhost -> http://127.0.0.1:8000/) -
1- Create a database(my_database) in MySQL installed on your system using command 'create database my_database'
   Username - root
   Password - project_stock_pass
2- Clone repository(project_stock)
3- Navigate to project_stock folder(parent folder) which is downloaded
4- Open cmd in the directory
5- Run command 'py manage.py migrate' in cmd
6- Run command 'py manage.py runserver' in cmd
7- Open any web browser and go to 'http://127.0.0.1:8000/'
8- Use the application

* NOTE -
In some symbols if result is an error saying " Key Error : 'Meta Data' ", kindly refresh the page till result is shown.
This error is due to server providing respective stock symbol information.
