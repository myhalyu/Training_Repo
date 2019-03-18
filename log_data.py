import re

file_path = 'D:\Python\Repo\Training_Repo\log_data.txt'

def top_downloader(path):
    with open(file_path) as f:
        calc_dict = {}
        for line in f:
            ip_date = line.split()[1][:12] + '] ' + line.split()[0]
            size = int(line.split()[2])
            if ip_date not in calc_dict:
                calc_dict[ip_date] = size
            else:
                calc_dict[ip_date] = calc_dict[ip_date] + size
    res_dict = {}
    size_dict = {}
    for key in calc_dict:
        date, ip = key.split()[:1]
        size = calc_dict[key]
        if date not in res_dict:
            res_dict[date] = ip
            size_dict[date] = size
        elif size > size_dict[date]:
            res_dict[date] = ip
            size_dict[date] = size
    for date in res_dict:
        print(date + ' - ' + res_dict[date])


def top_hour(path):
    with open(file_path) as f:
        calc_dict = dict()
        for line in f:
            hour = line.split()[1][13:15]
            if hour not in calc_dict:
                calc_dict[hour] = 1
            else:
                calc_dict[hour] += 1
    print('The least busy hour is ' + str(min(calc_dict, key=calc_dict.get)))


top_downloader(file_path)
top_hour(file_path)
