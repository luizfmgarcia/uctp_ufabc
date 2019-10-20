import os
import csv

with open("manyInstances.csv", encoding='unicode_escape') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    next(spamreader, None)  # skip the headers
    for row in spamreader:
        executeString = "src\main.py"
        for i in row:
            executeString = executeString + " " + str(i)
        os.system(executeString)

