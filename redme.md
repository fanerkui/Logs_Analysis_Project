# Logs Analysis

I use my code to generate a logs analysis report allowing help us analysis data from news database.

## Installation and use

* Download log_analysis.py;
* Move log_analysis.py to vagrant;
* run python log_analysis.py commands;
* open report.txt;
* Then you can see a logs analysis report.

## Views

* create a totalview

create or replace view totalview as
select date, COUNT(\*) as totalnum
from (select DATE(time) as date
from log
) as datetable
GROUP BY date;

* create a errorview

create or replace view errorview as
select date, COUNT(\*) as errornum
from (select DATE(time) as date
from log
where status = '404 NOT FOUND') as dateerror
GROUP BY date
ORDER BY date;

## License

GPL
