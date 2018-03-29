#!/usr/bin/env python
import psycopg2

"""Get a log report.

"""

filename = 'report.txt'


def get_log_analysis(query_command, flag):
    '''Get PostgresSQL database logs analysis report.
    '''
    DB = psycopg2.connect("dbname=news")
    c = DB.cursor()
    c.execute(query_command)
    rows = c.fetchall()
    for row in rows:
        if flag == 1:
            with open(filename, 'a') as file_object:
                file_object.write(str(row[0])+" -- ")
                file_object.write(str(round(row[1]*100, 1))+"% errors\n")
        else:
            with open(filename, 'a') as file_object:
                file_object.write(""+str(row[0])+" -- "+str(row[1])+" views\n")
    DB.close()

query = """
    SELECT articles.title, num
    FROM articles,
    (SELECT replace(path,'/article/','') AS logslug, count(*) AS num
    FROM log
    WHERE  path != '/'
    GROUP BY log.path
    ORDER BY num desc) AS logtitle
    WHERE articles.slug = logslug
    LIMIT 3;
    """
doubtstr = "1.What are the most popular \
three articles of all time? \n"
with open(filename, 'w') as file_object:
    file_object.write(doubtstr)
    file_object.write("answer: \n")
get_log_analysis(query, 0)
print("")

query = """
    SELECT authors.name, count(*) AS views
    FROM authors,articles,
    (SELECT replace(path,'/article/','') AS logslug
    FROM log
    WHERE  path != '/') AS logtitle
    WHERE articles.slug = logslug
    AND articles.author = authors.id
    GROUP BY authors.name
    ORDER BY views desc;
    """
doubtstr = "\n2. Who are the most popular \
article authors of all time? \n"
with open(filename, 'a') as file_object:
    file_object.write(doubtstr)
    file_object.write("answer: \n")
get_log_analysis(query, 0)
print("")

query = """
    SELECT totalview.date,
    ((1.0 * errorview.errornum) / (1.0 * totalview.totalnum))
    AS percentage
    from totalview, errorview
    WHERE totalview.date = errorview.date
    AND ((1.0 * errorview.errornum) / (1.0 * totalview.totalnum)) > 0.01;
    """
doubtstr = "\n3. On which days did more than \
0.01 of requests lead to errors? \n"
with open(filename, 'a') as file_object:
    file_object.write(doubtstr)
    file_object.write("answer: \n")
get_log_analysis(query, 1)
print("")
