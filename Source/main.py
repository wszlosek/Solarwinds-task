# Wojciech Szlosek

from datetime import datetime

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


def getFrontDoorsCode(date, statuses, codes): # ???

    frontDoors = []

    for i in range(1, len(date)):
        if (date[i][0:10] != date[i-1][0:10] and "exit" in statuses[i-1]):
            frontDoors.append(codes[i-1])

    return frontDoors


def openAndSeparate(filename):

    f = open(filename, "r")
    fields = []

    # first line does not contain data of interest:
    flag = True
    len = 0

    for line in f:

        len += 1

        if line == "\n":
            continue

        if flag:
            line = line.replace(" ", "")
            c = line[4]
            flag = False
            continue

        if line.count(c) != 2:
            print(f"Błędne dane wejściowe w linii numer {len}! "
                  f"Rezultat działania programu jej nie uwzględni.")
            continue

        fields.append(line.split(c))


    date = getDate(fields)
    statuses = getStatuses(fields)
    codes = getDoorCodes(fields)

    drzwiWejsciowe = getFrontDoorsCode(date, statuses, codes)
    print(drzwiWejsciowe)

    f.close()

    return(date, statuses, codes)


def sortLists(date, statuses, codes):

    sorted_lists = sorted(zip(date, statuses, codes),
                          key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"))
    date, statuses, codes = [[x[i] for x in sorted_lists] for i in range(3)]

    return(date, statuses, codes)


def differentTime(t1, t2):

    w1 = datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    w2 = datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")

    return w1-w2


def program(filename):

    date, statuses, codes = openAndSeparate(filename)
    date, statuses, codes = sortLists(date, statuses, codes)
    print(differentTime(date[21], date[14]))


if __name__ == '__main__':

    program("input.csv")
