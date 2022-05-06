import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

data = []

file = open("clean_penguins.csv", "r")
reader = csv.reader(file)
arrayForm = list(reader)

for data_RAW in arrayForm:
    # ignore first row, as they are column
    # this code could be adapted to use the column names to create the structured list
    if data_RAW[0] == "id":
        continue # skip to next loop

    # Fetch and cast all the data
    id = int(data_RAW[0])
    species = str(data_RAW[1])
    bill_length_mm = float(data_RAW[2])
    bill_depth_mm = float(data_RAW[3])
    flipper_length_mm = float(data_RAW[4])
    body_mass_g = float(data_RAW[5])

    # format data into a dictionary for easy access later
    structured_data = {
        "id": id,
        "species": species,
        "bill_length_mm": bill_length_mm,
        "bill_depth_mm": bill_depth_mm,
        "flipper_length_mm": flipper_length_mm,
        "body_mass_g/100": body_mass_g
    }

    # Add structured data (dic) to the list
    data.append(structured_data)


choice = "flipper_length_mm"
otherKeys = ["bill_length_mm", "bill_depth_mm", "body_mass_g/100"]

chosenData = []
otherData = []

for record in data:
    chosenData.append(record[choice])

    currentP = 0
    for a in otherKeys:
        currentP = currentP + int(record[a])
    currentP = currentP / 3
    
    otherData.append(currentP)

print(otherData)



plt.scatter(chosenData, otherData)
ax = plt.axes()
ax.plot([0,1],[0,1], transform=ax.transAxes)
plt.ylim([0, 150])
plt.xlim([0, 250])
plt.show()
