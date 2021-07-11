import datetime


def split_date_time(date, time):
    l_time = str(time).split(':')

    return datetime.datetime(date.year,
                             date.month,
                             date.day,
                             int(l_time[0]),
                             int(l_time[1]),
                             int(l_time[2]))
