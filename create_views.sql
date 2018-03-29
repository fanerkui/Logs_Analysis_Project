create view totalview as
    select date, count(*) as totalnum
    from (select date(time) as date
    from log
    ) as datetable
    group by date;

create view errorview as
    select date, count(*) as errornum
    from (select date(time) as date
    from log
    where status = '404 NOT FOUND') as dateerror
    group by date
    order by date;
