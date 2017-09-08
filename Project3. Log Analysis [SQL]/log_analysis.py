#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FSND: Project 3: Log Analysis
import psycopg2

# 1. What are the most popular three articles of all time?
"""
Example:
"Princess Shellfish Marries Prince Handsome" - 1201 views
"Baltimore Ravens Defeat Rhode Island Shoggoths" - 915 views
"Political Scandal Ends In Political Scandal" - 553 views
============================== Benchmarked SQL Queries & their output
#630ms# SELECT
            articles.title, COUNT(log.path) AS views
        FROM
            articles,
            log
        WHERE
            log.path = ('/article/' || articles.slug)
        GROUP BY articles.title
        ORDER BY views DESC
        LIMIT 3;
#450ms# SELECT
            articles.title, ex.num
        FROM
            articles,
            (SELECT
            log.path, COUNT(log.path) AS num
            FROM
            log
            WHERE
            log.path LIKE '%/article/%'
            GROUP BY log.path
            ORDER BY num DESC
            LIMIT 3) AS ex
        WHERE
            ex.path = ('/article/' || articles.slug)
        ORDER BY num DESC;
#735ms# SELECT
            articles.title, COUNT(log.path) AS num
        FROM
            articles,
            log
        WHERE
            log.path = CONCAT('/article/', articles.slug)
        GROUP BY log.path , articles.title
        ORDER BY num DESC
        LIMIT 3;
              title               |  num
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098
"""


def get_most_popular_articles():
    db_cursor.execute("""
                        SELECT
                            articles.title,
                            count(log.path) as views
                        FROM
                            articles,
                            log
                        WHERE
                            log.path=CONCAT('/article/', articles.slug)
                        GROUP BY
                            articles.title
                        ORDER BY
                            views DESC
                        LIMIT 3
                        """)
    return db_cursor.fetchall()


# 2. Who are the most popular article authors of all time?
# That is, when you sum up all of the articles each author has written,
which authors get the most page views?
"""
Example:
Ursula La Multa - 2304 views
Rudolf von Treppenwitz - 1985 views
Markoff Chaney - 1723 views
Anonymous Contributor - 1023 views
============================== Benchmarked SQL Queries & their output
#600ms# SELECT
            authors.name, COUNT(log.path) AS views
        FROM
            articles,
            authors,
            log
        WHERE
            log.path = CONCAT('/article/', articles.slug)
            AND articles.author = authors.id
        GROUP BY authors.id
        ORDER BY views DESC;
#682ms# SELECT
            authors.name,
            COUNT(ex.path) AS num_of_articles,
            SUM(num) AS views
        FROM
            authors,
            (SELECT
            articles.author, log.path, COUNT(log.path) AS num
            FROM
            articles, log
            WHERE
            log.path = ('/article/' || articles.slug)
            GROUP BY log.path , articles.author) AS ex
        WHERE
            authors.id = ex.author
        GROUP BY authors.id
        ORDER BY views DESC;
          name          | views
------------------------+--------
 Ursula La Multa        | 507594
 Rudolf von Treppenwitz | 423457
 Anonymous Contributor  | 170098
 Markoff Chaney         |  84557
"""


def get_most_popular_authors():
    db_cursor.execute("""
                        SELECT
                            authors.name,
                            count(log.path) as views
                        FROM
                            articles,
                            authors,
                            log
                        WHERE
                            log.path=CONCAT('/article/', articles.slug) AND
                            articles.author=authors.id
                        GROUP BY
                            authors.id
                        ORDER BY
                            views DESC
                        """)
    return db_cursor.fetchall()


# 3. On which days did more than 1% of requests lead to errors?
# The log table includes a column status that indicates the HTTP status code
# that the news site sent to the user's browser. (Refer back
#  to this lesson ifyou want to review the idea of HTTP status codes)
"""
Example:
July 29, 2016 - 2.5% errors
============================== Benchmarked SQL Queries & their output
#1850ms# SELECT
            TO_CHAR(DATE(time), 'Mon DD, YYYY') AS dt,
            ROUND(COUNT(CASE
                    WHEN status != '200 OK' THEN 1
                END) * 100.0 / COUNT(status),
                2) AS p_err
        FROM
            log
        GROUP BY DATE(time)
        HAVING (COUNT(CASE
            WHEN status != '200 OK' THEN 1
        END) * 100.0 / COUNT(status)) > 1
        ORDER BY p_err DESC;
#1900ms# SELECT *
        FROM
            (SELECT
                dt, (req_err::FLOAT*100/(req_err+req_ok)) AS p_err
                FROM
                (SELECT
                    date(time) AS dt,
                    COUNT(CASE WHEN status='200 OK' THEN 1 END) AS req_ok,
                    COUNT(CASE WHEN status!='200 OK' THEN 1 END) AS req_err
                    FROM
                        log
                    GROUP BY
                        dt
                ) AS dt_Rok_Rerr
            ) AS dt_Perr
        WHERE
            p_err>=1
        ORDER BY
            p_err DESC;
     date     | p_err
--------------+-------
 Jul 17, 2016 |  2.26
"""


def get_day_of_errors_greater_1p():
    db_cursor.execute("""
                        SELECT
                            TO_CHAR(DATE(time), 'Mon DD, YYYY') as date,
                            ROUND(COUNT(CASE WHEN status!='200 OK' THEN 1 END)
                            *100.0/COUNT(status), 2) as p_err
                        FROM
                            log
                        GROUP BY
                            date(time)
                        HAVING
                            (COUNT(CASE WHEN status!='200 OK' THEN 1 END)
                            *100.0/COUNT(status))>1
                        ORDER BY
                            p_err DESC
                        """)
    return db_cursor.fetchall()


# ###########################################
# news=> SELECT count(*) FROM log; -- 1677735

DBNAME = "news"
db_connection = psycopg2.connect(database=DBNAME)
db_cursor = db_connection.cursor()

print("1. What are the most popular three articles of all time?")
most_popular_articles = get_most_popular_articles()
for i in most_popular_articles:
    print('"{}" — {} views'.format(i[0], i[1]))

print("")
print("2. Who are the most popular article authors of all time?")
most_popular_authors = get_most_popular_authors()
for i in most_popular_authors:
    print('{} — {} views'.format(i[0], i[1]))

print("")
print("3. On which days did more than 1% of requests lead to errors?")
day_of_errors_greater_1p = get_day_of_errors_greater_1p()
# In case of more than one day ...
for i in day_of_errors_greater_1p:
    print('{} — {}%'.format(i[0], i[1]))


db_connection.close()
