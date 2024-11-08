import csv
import random

#formule pour renvoyer un point de la courbe en fonction du kilometrage
def predic(mileage, teta0, teta1):
    return (teta0 + (teta1 * mileage))

mileage = []
price = []

with open("data.csv", "r") as fichier_csv:
    reader = csv.reader(fichier_csv)
    for line in reader:
        if line[0].isdigit():
            mileage.append(int(line[0]))
        if (line[1].isdigit()):
            price.append(int(line[1]))
m = len(mileage)

teta0 = 0
teta1 = 0
#ici il faut calculer la somme des erreurs (la difference entre les prix estimes et ceux dans le dataset puis ce sera la difference entre les precedent et les nouveauc)
for mil in mileage:
    print(predic(mil, teta0, teta1))
#il faut que l'erreur totale soit la plus petite possible
#definir un learning rate a ajuster
#appliquer la formule pour ajuster teta0
#appliquer la formule pour ajuster teta1



