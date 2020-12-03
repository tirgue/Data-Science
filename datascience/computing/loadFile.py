import csv
import sys

def loadFile(filename):
    maxInt = sys.maxsize
    while True:
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)

    return list(csv.DictReader(open(filename)))

    