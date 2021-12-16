import os
from urllib.request import urlopen

local_path_GOOG = os.path.join('data', 'GOOG.csv')
local_path_PFE = os.path.join('data', 'PFE.csv')
local_path_AAPL = os.path.join('data', 'AAPL.csv')

GOOG_url = "https://query1.finance.yahoo.com/v7/finance/download/GOOG?period1=1608060316&period2=1639596316&interval=1d&events=history&includeAdjustedClose=true"
PFE_url = "https://query1.finance.yahoo.com/v7/finance/download/PFE?period1=1608070192&period2=1639606192&interval=1d&events=history&includeAdjustedClose=true"
AAPL_url = "https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1608071578&period2=1639607578&interval=1d&events=history&includeAdjustedClose=true"

paths = {local_path_GOOG: GOOG_url, local_path_PFE: PFE_url, local_path_AAPL: AAPL_url}

if not (os.path.isdir('data')):
    print('There is no "data" directory. Creating...')
    os.mkdir('data')

for path in paths.keys():

    if not os.path.isfile(path):
        url = paths[path]
        print("{} not found, downloading {}...".format(path, url))
        with urlopen(url) as file, open(path, 'r') as f:
            f.write(file.read())
    else:
        print("{} found".format(path))

for filename in os.listdir("data"):

    if filename.endswith('csv') and not filename.startswith("OUT"):
        print("Reading {}".format(filename))

        with open(os.path.join('data', filename), "r") as file:
            rows =[]

            for line in file.readlines():
                line = line.replace("\n","")
                rows.append(line.split(","))

        print("Change column added")
        openIndex = rows[0].index('Open')
        closeIndex = rows[0].index('Close')

        for row in rows:
            if rows.index(row) == 0:
                row.append('Change')
            else:
                Change = (float(row[closeIndex])-float(row[openIndex]))/float(row[openIndex])
                row.append(Change)

        newFileName = "OUT_"+filename
        newFileContent = ""

        for row in rows:
            for element in row:
                if row.index(element) < len(row)-1:
                    newFileContent +=element.__str__() + ","
                else:
                    newFileContent += element.__str__() + "\n"

        print("New file saved in {} path.".format(os.path.join('data',newFileName)))

        with open(os.path.join('data',newFileName),"w") as newFile:
            newFile.write(newFileContent)

        print("Done!")