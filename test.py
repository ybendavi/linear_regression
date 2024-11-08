import csv

mileage = []
price = []

with open("data.csv", "r") as fichier_csv:
    reader = csv.reader(fichier_csv)
    for line in reader:
        if line[0].isdigit():
            mileage.append(int(line[0]))
        if (line[1].isdigit()):
            price.append(int(line[1]))
print(mileage)
print(price)
