# Logs Analysis

This project be used to solve logs analysis question.

## Requirements
* vagrant
* VirtualBox

## Question list
* 1. What are the most popular three articles of all time?
* 2. Who are the most popular article authors of all time?
* 3. On which days did more than 1% of requests lead to errors?

## Installation
* Run vagrant up and vagrant ssh to configure the virtual environment.
* To load the data, cd into the vagrant directory and use the command psql -d news -f newsdata.sql.
* Import the views from the command line by typing: psql -d news -f create_views.sql.
* Run python log_analysis.py.
* Look at report.txt.

## License

GPL
