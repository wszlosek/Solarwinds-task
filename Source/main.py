# Wojciech Szlosek

from datetime import datetime, timedelta


def num_of_week(datess):
    w1 = datetime.date(datess).strftime("%V")

    return w1


def getDate(listOfLines):
    date = []

    for l in listOfLines:
        date.append(l[0].strip())

    return date


def getStatuses(listOfStatuses):
    statuses = []

    for l in listOfStatuses:
        statuses.append(l[1].strip())

    return statuses


def getDoorCodes(listOfCodes):
    codes = []

    for l in listOfCodes:
        codes.append(l[2].strip())

    return codes


def openAndSeparate(filename):
    f = open(filename, "r")
    fields = []

    # first line does not contain data of interest:
    flag = True
    len = 0

    for line in f:

        if line == "\n":
            continue

        if flag:
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

    date = getDate(fields)
    statuses = getStatuses(fields)
    codes = getDoorCodes(fields)

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


def listToStr(arr):
    s = ""

    for c in arr:
        s += c + " "

    return s[0:-1]


def operationI(date, statuses, codes, day):
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


def sumOfHoursInWeek(differentDates, intervals):
    i = 0
    w = 0
    t1 = datetime.strptime('00:00:00', '%H:%M:%S')
    time_zero = datetime.strptime('00:00:00', '%H:%M:%S')
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
        hours[i] = (hours[i] - time_zero + time)
        w += 1

    for h in range(len(hours)):
        hourss, minutes, seconds = convertTimedelta(hours[h] - time_zero)
        hours[h] = (hourss, minutes, seconds)

    return hours  # [ (1 tydzien), (2 tydzien), ... ] w formie [ (h, min, sek), ... ]


def display(differentDates, intervals, dates, statuses, codes):
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

        if operationI(dates, statuses, codes, differentDates[i]):
            opt.append("i")

        print(f"Day {differentDates[i]} Work {intervals[i]} {listToStr(opt)}")

    sum_of_hours = sumOfHoursInWeek(differentDates, intervals)
    print(sum_of_hours)


def program(filename):
    date, statuses, codes, lenF = openAndSeparate(filename)

    if lenF == 0:  # len of file == 0
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
