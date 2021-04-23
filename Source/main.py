# Wojciech Szlosek

from datetime import datetime, timedelta
import time


def num_of_week(datess):
    w1 = datetime.date(datess).strftime("%V")

    return int(w1) + datess.year  # zwraca numer tygodnia powiekszony o rok (np. 2019)


def get_date(list_of_lines):
    date = []

    for l in list_of_lines:
        date.append(l[0].strip())

    return date


def get_statuses(list_of_statuses):
    statuses = []

    for l in list_of_statuses:
        statuses.append(l[1].strip())

    return statuses


def get_door_codes(list_of_codes):
    codes = []

    for l in list_of_codes:
        codes.append(l[2].strip())

    return codes


def open_and_separate(filename):
    f = open(filename, "r")
    fields = []
    c = ";"

    # first line does not contain data of interest:
    flag = True

    len = 0

    for line in f:

        if line == "\n":
            continue

        if flag and "Reader" not in line:
            line = line.replace(" ", "")
            c = line[4]
            flag = False
            continue

        if line.count(c) != 2:
            print(f"Błędne dane wejściowe w linii numer {len + 1}! "
                  f"Rezultat działania programu jej nie uwzględni.")
            continue

        len += 1
        fields.append(line.split(c))

    date = get_date(fields)
    statuses = get_statuses(fields)
    codes = get_door_codes(fields)

    f.close()

    return (date, statuses, codes, len)


def sortLists(date, statuses, codes):
    sorted_lists = sorted(zip(date, statuses, codes),
                          key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"))
    date, statuses, codes = [[x[i] for x in sorted_lists] for i in range(3)]

    return (date, statuses, codes)


def differentTime(t1, t2):
    w1 = datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    w2 = datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")

    return w1 - w2


def list_to_str(arr):
    s = ""

    for c in arr:
        s += c + " "

    return s[0:-1]


def operation_i(date, statuses, codes, day):
    days = []

    for d in date:
        days.append(d[0:10])

    firstIndex = days.index(day)
    lastIndex = len(days) - days[::-1].index(day) - 1

    if "exit" not in statuses[lastIndex]:  # first situation: no "exit" at the exit of the building
        return True

    isEntry = False  # second situation: no "entry" (musi wejść przynajmniej raz z identyfikatorem - do biura)
    for i in range(firstIndex, lastIndex + 1):
        if "entry" in statuses[i]:
            isEntry = True

    if isEntry == False:
        return True

    # do dokończenia, należy rozpatrzyć inne przypadki gdy dodajemy 'i'


def convertTimedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)

    return hours, minutes, seconds


def sum_of_hours_in_week(differentDates, intervals):
    i = 0
    w = 0
    t1 = datetime.strptime('00:00:00', '%H:%M:%S')
    TIMEZERO = datetime.strptime('00:00:00', '%H:%M:%S')
    hours = []
    hours.append(t1)
    num_of_day = num_of_week(datetime.strptime(differentDates[0], "%Y-%m-%d"))

    for d in differentDates:
        day = datetime.strptime(d, "%Y-%m-%d")
        time = datetime.strptime(intervals[w], "%H:%M:%S")
        if num_of_week(day) != num_of_day:
            num_of_day = num_of_week(day)
            i += 1
            hours.append(t1)
        hours[i] = (hours[i] - TIMEZERO + time)
        w += 1

    for h in range(len(hours)):
        hourss, minutes, seconds = convertTimedelta(hours[h] - TIMEZERO)
        hours[h] = (hourss, minutes, seconds)

    return hours  # [ (1 tydzien), (2 tydzien), ... ] w formie [ (h, min, sek), ... ]


def tuple_to_timeformat(tup):  # (11, 2, 4) -> 11:02:04

    return f"{int(tup[0]):02}:{int(tup[1]):02}:{int(tup[2]):02}"


def full_time_weekly(differentDates):
    FULL = timedelta(hours=8)
    full_per_week = []
    full_per_week.append(1)
    index = 0
    numbers_of_week = []

    for d in differentDates:
        numbers_of_week.append(num_of_week(datetime.strptime(d, "%Y-%m-%d")))
    numbers_of_week.append(0)

    for i in range(len(numbers_of_week)):
        if(numbers_of_week[i] != 0):
            if numbers_of_week[i] == numbers_of_week[i+1]:
                full_per_week[index] += 1
            else:
                full_per_week.append(1)
                index += 1

    full_per_week.pop()
   # print(numbers_of_week)
   # print(full_per_week)

    max_of_week = []

    for l in full_per_week:
        max_of_week.append(l * FULL)

    return max_of_week


def display(differentDates, intervals, dates, statuses, codes):
    t = 0

    for i in range(len(differentDates)):
        opt = []
        day = datetime.strptime(differentDates[i], "%Y-%m-%d")
        time = datetime.strptime(intervals[i], "%H:%M:%S")
        nineHours = datetime.strptime("09:00:00", "%H:%M:%S")
        sixHours = datetime.strptime("06:00:00", "%H:%M:%S")

        if day.weekday() == 5 or day.weekday() == 6:  # saturday or sunday
            opt.append("w")

        if time > nineHours:
            opt.append("ot")
        elif time < sixHours:
            opt.append("ut")

        if operation_i(dates, statuses, codes, differentDates[i]):
            opt.append("i")

        sum_of_hours = sum_of_hours_in_week(differentDates, intervals)[t]

        flag = False

        if i + 1 < len(differentDates):
            if num_of_week(datetime.strptime(differentDates[i], "%Y-%m-%d")) != num_of_week(
                    datetime.strptime(differentDates[i + 1], "%Y-%m-%d")):
                flag = True
        else:
            flag = True

        if flag:

            full_time = full_time_weekly(differentDates)[t]

            if timedelta(hours=sum_of_hours[0], minutes=sum_of_hours[1], seconds=sum_of_hours[2]) > full_time:
                difference = timedelta(hours=sum_of_hours[0], minutes=sum_of_hours[1],
                                       seconds=sum_of_hours[2]) - full_time
                difference = str(difference)
            else:
                difference = full_time - timedelta(hours=sum_of_hours[0], minutes=sum_of_hours[1],
                                                   seconds=sum_of_hours[2])
                difference = "-" + str(difference)

            print(
                f"Day {differentDates[i]} Work {intervals[i]} {list_to_str(opt)} {tuple_to_timeformat(sum_of_hours)} {difference}")
            t += 1
        else:
            print(f"Day {differentDates[i]} Work {intervals[i]} {list_to_str(opt)}")


def program(filename):
    date, statuses, codes, len_of_file = open_and_separate(filename)

    if len_of_file == 0:
        return

    date, statuses, codes = sortLists(date, statuses, codes)
    n = len(date)
    intervals = []
    differentDates = []

    f1 = date[0]

    for i in range(n):

        if i == n - 1:
            if str(date[i][0:10]) not in differentDates:
                differentDates.append(str(date[i][0:10]))

            f2 = date[i]
            intervals.append(str(differentTime(f2, f1)))

        elif date[i][0:10] != date[i + 1][0:10]:
            differentDates.append(str(date[i][0:10]))

            f2 = date[i]
            intervals.append(str(differentTime(f2, f1)))
            f1 = date[i + 1]


    display(differentDates, intervals, date, statuses, codes)


if __name__ == '__main__':
    program("input.csv")
    