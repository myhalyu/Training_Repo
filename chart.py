import csv
import datetime
import matplotlib.pyplot as plt
import numpy

file_name = 'HistoricalQuotes.csv'


def read_data_csv(file, column):
    data = {}
    with open(file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            isValidDate = True
            try:
                year, month, day = line['date'].split('/')
                datetime.date(int(year),int(month),int(day))
            except ValueError:
                isValidDate = False
            if isValidDate == True:
                date = datetime.date(int(year),int(month),int(day))
                data[date] = float(line[column])
    return data


D = read_data_csv(file_name, 'open')
E = read_data_csv(file_name, 'close')


x1 = D.keys()
y1 = D.values()
plt.plot(x1, y1)

x2 = E.keys()
y2 = E.values()
plt.plot(x2, y2)

plt.ylabel('Price in USD')
plt.title('EPAM Stock')

plt.show()
