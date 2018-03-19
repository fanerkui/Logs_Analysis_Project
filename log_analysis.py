import psycopg2


def get_log_analysis(query_command):
    '''Get PostgresSQL database logs analysis report.
    '''
    DB = psycopg2.connect("dbname=news")
    c = DB.cursor()
    c.execute(query_command)
    rows = c.fetchall()
    for row in rows:
        print " ", row[0], "-->", row[1]
    DB.close()


def create_views(query_command):
    '''create PostgresSQL view.
    '''
    DB = psycopg2.connect("dbname=news")
    c = DB.cursor()
    c.execute(query_command)
    DB.close()

query = "select articles.title, num \
    from articles, \
    (select replace(path,'/article/','') as logslug, \
    count(*) as num \
    from log \
    where  path != '/' \
    group by log.path \
    order by num desc) as logtitle \
    where articles.slug = logslug \
    limit 3;"
print("1.What are the most popular three articles of all time?")
print("answer:")
get_log_analysis(query)
print("")

query = "select authors.name, count(*) as views \
    from authors,articles, \
    (select replace(path,'/article/','') as logslug \
    from log \
    where  path != '/') as logtitle \
    where articles.slug = logslug \
    and articles.author = authors.id \
    group by authors.name \
    order by views desc;"
print("2. Who are the most popular article authors of all time?")
print("answer:")
get_log_analysis(query)
print("")

query = "create or replace view totalview as \
    select date, count(*) as totalnum \
    from (select date(time) as date \
    from log \
    ) as datetable \
    group by date;"
create_views(query)
query = "create or replace view errorview as \
    select date, count(*) as errornum \
    from (select date(time) as date \
    from log \
    where status = '404 NOT FOUND') as dateerror \
    group by date \
    order by date;"
create_views(query)
query = "select totalview.date, \
    ((1.0 * errorview.errornum) / (1.0 * totalview.totalnum)) \
    as percentage \
    from totalview, errorview \
    where totalview.date = errorview.date \
    and ((1.0 * errorview.errornum) / (1.0 * totalview.totalnum)) > 0.01;"
print("3. On which days did more than 0.01 of requests lead to errors?")
print("answer:")
get_log_analysis(query)
print("")
