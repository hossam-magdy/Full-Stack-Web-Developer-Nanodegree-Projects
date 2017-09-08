# Full Stack Nanodegree Project: Log Analysis

## What is this project? What does it do?
It is an *internal reporting tool* that prints out reports (in plain text) based on the data in the database of *newspaper site*. This reporting tool is a Python program using the psycopg2 module to connect to the database.

It is designed to answer 3 questions from database:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Sample output:
```
$ python log_analysis.py
1. What are the most popular three articles of all time?
"Candidate is jerk, alleges rival" — 338647 views
"Bears love berries, alleges bear" — 253801 views
"Bad things gone, say good people" — 170098 views

2. Who are the most popular article authors of all time?
Ursula La Multa — 507594 views
Rudolf von Treppenwitz — 423457 views
Anonymous Contributor — 170098 views
Markoff Chaney — 84557 views

3. On which days did more than 1% of requests lead to errors?
Jul 17, 2016 — 2.26%
```

## How to run the project?
1. Download & install [Python](https://www.python.org/downloads/) (2 or 3), [PostgreSQL](https://www.postgresql.org/download/) and [Psycopg2](http://initd.org/psycopg/docs/install.html)
2. Create "news" database and import "newsdata.zip".
You can `cd` the project directory then run:
`echo 'CREATE DATABASE news;' | psql; unzip -p newsdata.zip | psql news;`
3. Run "python log_analysis.py"

Note: This project runs on any of Python2 & Python3
