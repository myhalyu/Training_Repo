import sqlite3
import matplotlib.pyplot as plt
import datetime

database_path = 'OLX_posts.db'
query_text = "SELECT date(added_on) as trade_day, avg(price_usd) as avg_value FROM Posts WHERE number_of_rooms = 2 group by date(added_on) order by date(added_on)"


def get_data_from_db(cur, query):
    query_result = cur.execute(query).fetchall()

    values = {}
    for row in query_result:
        year, month, day = row[0].split('-')
        date = datetime.date(int(year),int(month),int(day))
        values[date] = float(row[1])

    return values


connection = sqlite3.connect(database_path)
cursor = connection.cursor()

median_values = get_data_from_db(cursor, query_text)

x1 = median_values.keys()
y1 = median_values.values()
plt.plot(x1, y1)

plt.ylabel('Price in USD')
plt.title('Average price for 2-rooms apartments')

plt.show()


