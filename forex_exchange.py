import sqlite3
import requests
import json
import re
import csv

db_path = 'forex.sqlite3'
rates_url = 'https://api.exchangeratesapi.io/latest'
output_file = 'currency_log.csv'


# get list of rates from site
def get_rates_from_site(path):
    response = requests.get(path)
    json_data = json.loads(response.text)
    rates = json_data['rates']

    return rates


# get list of currencies from database
def get_currencies_from_db(cur):
    currency_codes = cur.execute("select currency_code from rates").fetchall()

    return currency_codes


# get currency rate from database
def get_currency_rate_db(cur, currency):
    dirty_rate = cur.execute("select rate from rates where currency_code = ?", (currency,)).fetchall()
    str_rate = re.sub("[,()\[\] ]", "", str(dirty_rate))
    rate = float(str_rate)

    return rate


# insert new record to database
def insert_new_record_db(cur, conn, values):
    cur.execute("insert into rates values (?, ?, ?)", values)
    conn.commit()


# update record in database
def update_record_db(cur, conn, values):
    cur.execute("update rates set rate = ? where currency_code = ?", values)
    conn.commit()


# delete record from database
def delete_record_db(cur, conn, currency):
    cur.execute("delete from rates where currency_code = ?", (currency,))
    conn.commit()


# create to csv file
def write_log(logs, output_filename):
    with open(output_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(('currency', 'old_rate', 'new_rate', 'percent_change'))
        writer.writerows(logs)


site_rates = get_rates_from_site(rates_url)

with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()

    dirty_db_data = get_currencies_from_db(cursor)
    db_data = [re.sub("[,()'' ]", "", str(record)) for record in dirty_db_data]
    log_list = []

    for record in site_rates:
        if record not in db_data:
            row = (record, None, site_rates[record])
            insert_new_record_db(cursor, connection, row)
            log_list.append([record, None, site_rates[record], 'New record'])
        elif record in db_data and site_rates[record] != get_currency_rate_db(cursor, record):
            row = (site_rates[record], record)
            deviation = 100 * (site_rates[record] - get_currency_rate_db(cursor, record)) / get_currency_rate_db(cursor,
                                                                                                                 record)
            log_list.append([record, get_currency_rate_db(cursor, record), site_rates[record], deviation])
            update_record_db(cursor, connection, row)

    for record in db_data:
        if record not in site_rates:
            log_list.append([record, get_currency_rate_db(cursor, record), None, 'Deleted record'])
            delete_record_db(cursor, connection, record)

    write_log(log_list, output_file)
