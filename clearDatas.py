import csv
import sys
import re

def extract_mails(mail_set):
    match = re.match("frozenset\({(.*?)}\)", mail_set)
    if match:
        return match[1].split(", ")

    else: 
        return "None"

def filterData(data):
    d= {}
    for key in data.keys():
        if "Cat" in key:
            pass

        else: d[key] = data[key]

    return d

if __name__ == "__main__":
    maxInt = sys.maxsize
    while True:
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)

    try:
        filename = sys.argv[1]
        with open(filename, "r") as file:
            print("Loading...")
            datas = csv.DictReader(file)    
            datas = list(datas)
    except :
        print("*** Invalid filename ***\nUsage : python script_clearDatas.py FILENAME")
        exit(-1)

    csv_columns = []

    for key in datas[0].keys():
            if not "Cat" in key:
                csv_columns.append(key)

    output = open("data_response.csv", 'w')
    writer = csv.DictWriter(output, fieldnames = csv_columns)
    writer.writeheader()

    print("Computing...")

    c = 0
    sum = 0

    alreadyAdded = {}

    try:
        for data in datas:
            subject = data.get("Subject")
            if subject.startswith("Re:") and subject[3:].strip() != '':
                sender = extract_mails(data.get('From'))

                d_subject = data.get("Subject")[4:]

                ok = False

                for d in datas:
                    if d.get("Subject")  == d_subject:
                        receivers = extract_mails(d.get("To"))
                        if sender[0] in receivers:
                            ok = True
                            if alreadyAdded.get(d.get('Message-ID')) == None:
                                sum += 1
                                writer.writerow(filterData(d))
                                alreadyAdded[d.get('Message-ID')] = 1
                            break

                if ok:
                    writer.writerow(filterData(data))
                    sum += 1

            c += 1

            if c % 1000 == 0:
                print('Aready done : ' + str(c))

    except KeyboardInterrupt:
        pass

    print('Result : ' + str(sum))