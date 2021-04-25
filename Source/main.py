# Wojciech Szlosek

from datetime import datetime
from datetime import timedelta
import time
import random


def num_of_week(datess) -> int:
    """Return a unique week number."""

    w1 = datetime.date(datess).strftime("%V")

    return int(w1) + datess.year


def get_date(list_of_lines) -> list:
    """Return all dates (yyyy-mm-dd hh:mm:ss) from the file."""

    date = []

    for l in list_of_lines:
        date.append(l[0].strip())

    return date


def get_statuses(list_of_statuses) -> list:
    """Return all statuses (Reader entry/exit) from the file."""

    statuses = []

    for l in list_of_statuses:
        statuses.append(l[1].strip())

    return statuses


def get_door_codes(list_of_codes) -> list:
    """Return all door codes from the file."""

    codes = []

    for l in list_of_codes:
        codes.append(l[2].strip())

    return codes


def is_valid_date(year, month, day) -> bool:
    """Checks if the date format is correct."""

    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        day_count_for_month[2] = 29

    return 1 <= month <= 12 and 1 <= day <= day_count_for_month[month]


def is_valid_time(hours, minutes, seconds) -> bool:
    """Checks if the time format is correct."""

    return 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59


def open_and_separate(filename):
    """Reads data from a file, dividing it into columns."""

    f = open(filename, "r")
    fields = []
    c = ";"
    i = 1

    # First line does not contain data of interest:
    flag = True

    len_of_file = 0

    for line in f:

        if line == "\n":
            continue

        if flag and "Reader" in line:
            flag = False

        if flag and "Reader" not in line:
            line = line.replace(" ", "")
            c = line[4]
            flag = False
            continue

        if line.count(c) != 2:
            continue

        year = int(line[0:4])
        month = int(line[5:7])
        day = int(line[8:10])
        hours = int(line[11:13])
        minutes = int(line[14:16])
        seconds = int(line[17:19])

        if not is_valid_date(year, month, day) or not is_valid_time(hours, minutes, seconds):
            #  print(f"Błędne dane wejściowe w linii numer {i + 1}! "
            #  f"Rezultat działania programu jej nie uwzględni.")
            continue

        len_of_file += 1
        fields.append(line.split(c))
        i += 1

    date = get_date(fields)
    statuses = get_statuses(fields)
    codes = get_door_codes(fields)

    f.close()

    return date, statuses, codes, len_of_file


def sort_lists(date, statuses, codes):
    """Sorts the lists by date (oldest to newest)."""

    sorted_lists = sorted(zip(date, statuses, codes),
                          key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"))
    date, statuses, codes = [[x[i] for x in sorted_lists] for i in range(3)]

    return date, statuses, codes


def different_time(t1, t2) -> timedelta:
    """Returns the time between two dates."""

    w1 = datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    w2 = datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")

    return w1 - w2


def list_to_str(arr) -> str:
    s = ""
    for c in arr:
        s += c + " "

    return s[0:-1]


def operation_i(date, statuses, codes, day) -> bool:
    """Checks if the considered date is inconclusive (i)."""

    days = []
    flag = False

    for d in date:
        days.append(d[0:10])

    first_index = days.index(day)
    last_index = len(days) - days[::-1].index(day) - 1

    special_char = ["/", ".", "|", "\\", "-", "<", ">", "+", "*", "#"]
    char_split = ""

    for c in special_char:
        if c in str(codes[first_index]):
            char_split = c
            cnt = str(codes[first_index]).count(char_split)
            if cnt == 3:
                flag = False
                break

    for i in range(first_index, last_index + 1):
        if str(codes[i]).count(char_split) != 3:
            flag = True

    # First case, the code is not a form "*/floor number/*/*"
    if flag:
        # First situation: no "exit" in statuses at the exit of the building
        if "exit" not in statuses[last_index]:
            return True

        # Second situation: no "entry"
        is_entry = False
        for i in range(first_index, last_index + 1):
            if "entry" in statuses[i]:
                is_entry = True

        if not is_entry:
            return True

    # Code of door: ("*/floor number/*/*")
    else:
        floor_list = []

        for i in range(first_index, last_index + 1):
            floor_list.append((str(codes[i]).split("/"))[1])

        if floor_list[-1] != "0" or "exit" not in str(statuses[last_index]):
            return True

        # We assume that the office is on any NON-ZERO floor

        is_entry = False

        for i, num_floor in enumerate(floor_list):
            if num_floor != "0":
                if "entry" in str(statuses[first_index + i]):
                    is_entry = True

        if not is_entry:
            return True

    return False


def sum_of_hours_in_week(different_dates, intervals):
    """Return the sum of hours spent by the employee at work per week.
    format: [ (first week), (second week), ... ] in form: (...) = (h, min, sec)
    """

    i = 0
    w = 0
    t1 = datetime.strptime('00:00:00', '%H:%M:%S')
    TIMEZERO = datetime.strptime('00:00:00', '%H:%M:%S')
    hours = [t1]
    num_of_day = num_of_week(datetime.strptime(different_dates[0], "%Y-%m-%d"))

    for d in different_dates:
        day = datetime.strptime(d, "%Y-%m-%d")
        tim = datetime.strptime(intervals[w], "%H:%M:%S")
        if num_of_week(day) != num_of_day:
            num_of_day = num_of_week(day)
            i += 1
            hours.append(t1)
        hours[i] = (hours[i] - TIMEZERO + tim)
        w += 1

    for h in range(len(hours)):
        hourss, minutes, seconds = convert_timedelta(hours[h] - TIMEZERO)
        hours[h] = (hourss, minutes, seconds)

    return hours  # [ (1 tydzien), (2 tydzien), ... ] w formie [ (h, min, sek), ... ]


def tuple_to_timeformat(tup) -> str:
    """Converts tuple to time format < e.g. (11, 2, 4) -> "11:02:04" >."""

    return f"{int(tup[0]):02}:{int(tup[1]):02}:{int(tup[2]):02}"


def convert_timedelta(duration) -> tuple:
    """Converts timedelta to tuple (h, min, sec)."""

    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)

    return hours, minutes, seconds


def full_time_weekly(different_dates) -> list:
    """Return the sum of full-time hours."""

    FULL = timedelta(hours=8)
    full_per_week = [1]
    index = 0
    numbers_of_week = []

    for d in different_dates:
        numbers_of_week.append(num_of_week(datetime.strptime(d, "%Y-%m-%d")))
    numbers_of_week.append(0)

    for i in range(len(numbers_of_week)):
        if numbers_of_week[i] != 0:
            if numbers_of_week[i] == numbers_of_week[i + 1]:
                full_per_week[index] += 1
            else:
                full_per_week.append(1)
                index += 1

    full_per_week.pop()
    max_of_week = []

    for l in full_per_week:
        max_of_week.append(l * FULL)

    return max_of_week


def display(different_dates, intervals, dates, statuses, codes):
    output = []
    t = 0
    for i in range(len(different_dates)):
        opt = []
        day = datetime.strptime(different_dates[i], "%Y-%m-%d")
        tim = datetime.strptime(intervals[i], "%H:%M:%S")
        nine_hours = datetime.strptime("09:00:00", "%H:%M:%S")
        six_hours = datetime.strptime("06:00:00", "%H:%M:%S")

        if day.weekday() == 5 or day.weekday() == 6:  # saturday or sunday
            opt.append("w")

        if tim > nine_hours:
            opt.append("ot")
        elif tim < six_hours:
            opt.append("ut")

        if operation_i(dates, statuses, codes, different_dates[i]):
            opt.append("i")

        sum_of_hours = sum_of_hours_in_week(different_dates, intervals)[t]

        flag = False

        if i + 1 < len(different_dates):
            if num_of_week(datetime.strptime(different_dates[i], "%Y-%m-%d")) != num_of_week(
                    datetime.strptime(different_dates[i + 1], "%Y-%m-%d")):
                flag = True
        else:
            flag = True

        if flag:
            full_time = full_time_weekly(different_dates)[t]

            if timedelta(hours=sum_of_hours[0], minutes=sum_of_hours[1], seconds=sum_of_hours[2]) > full_time:
                difference = timedelta(hours=sum_of_hours[0], minutes=sum_of_hours[1],
                                       seconds=sum_of_hours[2]) - full_time
                difference = tuple_to_timeformat(convert_timedelta(difference))
                difference = str(difference)
            else:
                difference = full_time - timedelta(hours=sum_of_hours[0], minutes=sum_of_hours[1],
                                                   seconds=sum_of_hours[2])
                difference = tuple_to_timeformat(convert_timedelta(difference))
                difference = "-" + str(difference)

            output.append(f"Day {different_dates[i]} Work {intervals[i]} {list_to_str(opt)} "
                          f"{tuple_to_timeformat(sum_of_hours)} {difference}")
            t += 1
        else:
            if len(opt) == 0:
                output.append(f"Day {different_dates[i]} Work {intervals[i]}")
            else:
                output.append(f"Day {different_dates[i]} Work {intervals[i]} {list_to_str(opt)}")

    return output


def save_in_file(to_file, new_filename="result"):
    f = open(new_filename, "w")

    if len(to_file) == 0:
        f.write(" ")
        f.close()
        return

    for i, line in enumerate(to_file):
        if i == len(to_file) - 1:
            f.write(line)
            break
        f.write(f"{line}\n")

    f.close()


def program(filename="input.csv"):
    date, statuses, codes, len_of_file = open_and_separate(filename)
    to_file = []

    if len_of_file == 0:
        save_in_file(to_file)
        return

    date, statuses, codes = sort_lists(date, statuses, codes)
    n = len(date)
    intervals = []
    different_dates = []
    f1 = date[0]

    # Creates a list of different days
    for i in range(n):
        if i == n - 1:
            if str(date[i][0:10]) not in different_dates:
                different_dates.append(str(date[i][0:10]))

            f2 = date[i]
            intervals.append(str(different_time(f2, f1)))

        elif date[i][0:10] != date[i + 1][0:10]:
            different_dates.append(str(date[i][0:10]))

            f2 = date[i]
            intervals.append(str(different_time(f2, f1)))
            f1 = date[i + 1]

    to_file = display(different_dates, intervals, date, statuses, codes)
    save_in_file(to_file)


if __name__ == '__main__':
    program()
