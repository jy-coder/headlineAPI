from django.http import HttpResponse
from django.db import connection


def execute_query(query):
	cur = connection.cursor()
	cur.execute(query)
	rows = [
		dict((cur.description[i][0], value) for i, value in enumerate(row))
		for row in cur.fetchall()
	]
	return rows 