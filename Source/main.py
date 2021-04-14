# Wojciech Szlosek

def getDate(listOfLines):

    date = []

    for l in listOfLines:
        date.append(l[0].strip())

    print(date)

    return date

def getStatuses(listOfStatuses):

    statuses = []

    for l in listOfStatuses:
        statuses.append(l[1].strip())

    print(statuses)

    return statuses

def getDoorCodes(listOfCodes):

    codes = []

    for l in listOfCodes:
        codes.append(l[2].strip())

    print(codes)

    return codes

def openAndSeparate(filename):

    f = open(filename, "r")
    fields = []

    # first line does not contain data of interest:
    flag = True

    for line in f:
        if flag:
            flag = False
            continue

        fields.append(line.split(";"))

    print(fields)
    date = getDate(fields)
    statuses = getStatuses(fields)
    codes = getDoorCodes(fields)

    f.close()

    return(date, statuses, codes)

def program(filename):

    date, statuses, codes = openAndSeparate(filename)

if __name__ == '__main__':
    program("input.csv")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
