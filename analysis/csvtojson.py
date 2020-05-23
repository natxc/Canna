import csv, json


csvFilePath_county = "canna.csv"
jsonFilePath_county = "canna.json"

arr = []
with open (csvFilePath_county) as csvFile:
    csvReader = csv.DictReader(csvFile)
    print(csvReader)
    for csvRow in csvReader:
        arr.append(csvRow)

with open(jsonFilePath_county, "w") as jsonFile:
    jsonFile.write(json.dumps(arr, indent = 4))

