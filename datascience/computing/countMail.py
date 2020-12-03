from datetime import date as Date
import calendar

def countMail(datas, by=""):
    if by == "":
        result = 0
        for _ in datas:
            result += 1

        return result

    dic = {}

    if by == "WEEK":
        for i in range(1,8): dic[i] = 0
        for data in datas:
            date = data.get('Date')

            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            weekDay = Date(year, month, day).isoweekday()
            dic[weekDay] += 1

        result = {}
        for key in dic.keys():
            day = list(calendar.day_name)[int(key) - 1]
            result[day] = dic.get(key)

        return result

    elif by == "HOUR":
        for i in range(0,24) : dic[i] = 0

        for data in datas:
            date = data.get('Date')

            hour = int(date[11:13])
            dic[hour] += 1

        return dic
