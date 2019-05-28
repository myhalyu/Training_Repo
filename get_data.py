import requests
import sqlite3
import json
from datetime import date, timedelta

BASE_URL = 'https://35.204.204.210/{}-{}-{}/'
YEAR = 2017


def date_format_two_digits(str):
    length = len(str)
    if length == 2:
        return str
    else:
        return '0' + str


def get_url_list(year):
    url_list = []
    d1 = date(year, 1, 1)
    d2 = date(year, 12, 31)
    delta = d2 - d1
    for i in range(delta.days + 1):
        url_date = d1 + timedelta(days=i)
        month = url_date.month
        day = url_date.day
        url_list.append(BASE_URL.format(year, date_format_two_digits(str(month)), date_format_two_digits(str(day))))

    return url_list


def get_olx_posts(url):
    response = requests.get(url, verify=False)
    json_data = json.loads(response.text)

    return json_data


def insert_data_to_db(cur, conn, values):
    cur.execute("insert into posts values (?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
    conn.commit()


connection = sqlite3.connect('OLX_posts.db')
cursor = connection.cursor()
connection.execute("CREATE TABLE Posts([price_usd] int, [title] text, [text] text, [total_area] int, [kitchen_area] int, [living_area] int,	[location] text, [number_of_rooms] int,	[added_on] date)")


for url in get_url_list(YEAR):
    data = get_olx_posts(url)
    for record in data['postings']:
        row = record['price_usd'], record['title'], record['text'], record['total_area'], record['kitchen_area'], record['living_area'], record['location'], record['number_of_rooms'], record['added_on']
        insert_data_to_db(cursor, connection, row)