import csv, json, sys, datetime
from script_clearDatas import extract_mails

def createDate(data):
    year = int(data.get('Date')[0:4])
    month = int(data.get('Date')[5:7])
    day = int(data.get('Date')[8:10])
    hour = int(data.get('Date')[11:13])
    minute = int(data.get('Date')[14:16])
    return datetime.datetime(year, month, day, hour, minute)

def retrieve_sending_month(date):
    return date.strftime("%b")

def retrieve_sending_day(date):
    return date.strftime("%a")

def retrieve_sending_time(date):
    if date.hour < 0:
        return "bet-0-5"
    if date.hour < 5:
        return "bet-5-8"
    if date.hour < 8:
        return "bet-8-11"
    if date.hour < 11:
        return "bet-11-14"
    if date.hour < 14:
        return "bet-14-18"
    if date.hour < 18:
        return "bet-18-20"
    if date.hour < 20:
        return "bet-20-22"
    if date.hour < 22:
        return "bet-22-0"
    
def retrieve_long_subject(data):
    # Moyenne de lettres par mot : 4.65
    # On estime qu'un sujet est long au delà d'une dizaine de mots (10 * 4.65 = 46)
    # Donc 46 caractères est la limite entre un sujet long et court
    return "yes" if len(data.get('Subject')) > 46 else "no"

def retrieve_content_size(data):
    if len(data.get('content')) < 150:
        return "small"
    elif len(data.get('content')) > 300:
        return "high" 
    else:
        return "medium"

def retrieve_formal(data):
    with open("formules.txt", "r") as file:
        content = data.get('content').lower()
        for formule in file:
            if formule in content:
                return "yes"

    return "no"

def retrieve_time_until_answer(data, datas):
    subject = data.get("Subject")
    if subject.startswith("Re:"):
        sender = extract_mails(data.get('From'))
        d_subject = data.get("Subject")[4:]
        for d in datas:
            if d.get("Subject")  == d_subject:
                receivers = extract_mails(d.get("To"))
                if sender[0] in receivers:
                    break

        respondingDate = createDate(data)
        sendingDate = createDate(d)

        delta = respondingDate - sendingDate
        if delta < datetime.timedelta():
            return -1

        return str(delta)

    else:
        return "None"

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
        print("*** Invalid filename ***\nUsage : python classify.py FILENAME")
        exit(-1)

    emails = []

    print("Computing...")
    for data in datas:
        sendingDate = createDate(data)

        time_until_answer = retrieve_time_until_answer(data, datas)

        if time_until_answer != -1:
            sending_month = retrieve_sending_month(sendingDate)
            sending_day = retrieve_sending_day(sendingDate)
            sending_time = retrieve_sending_time(sendingDate)
            long_subject = retrieve_long_subject(data)
            content_size = retrieve_content_size(data)
            formal = retrieve_formal(data)

            email = {
                "sending_month" : sending_month,
                "sending_day" : sending_day,
                "sending_time" : sending_time,
                "long_subject" : long_subject,
                "content_size" : content_size,
                "formal" : formal,
                "time_until_answer" : time_until_answer,
            }
            emails.append(email)

    output = {
        "emails" : emails
    }

    print("Writing...")
    outputFile = open("classesDatas.json", "w")
    json.dump(output, outputFile)

    print("Done")