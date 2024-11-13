import csv
import random

#formule pour renvoyer un point de la courbe en fonction du kilometrage
def predic(mileage, teta0, teta1):
    return (teta0 + (teta1 * mileage))
#formule de normalisation
def normalize(number, tab):
    n_max = max(tab)
    n_min = min(tab)
    return (number - n_min) / (n_max - n_min)
def calculat_err_m(m, mileage, price, teta0, teta1, teta):
    i = 0
    err_sum = 0

    #ici il faut calculer la somme des erreurs (la difference entre les prix estimes et ceux dans le dataset puis ce sera la difference entre les precedent et les nouveauc)
    while i < m:
        if teta == 0:
            err_sum += (predic(mileage[i], teta0, teta1) - price[i])
        else:
            # application de la formule pour le teta1, on multiplie le resultat par une normalisation de la donnee traitee (la transformer en une valeur entre 0 et 1) parce que plus elle est haute plus elle influencera la courbe
            err_sum += ((predic(mileage[i], teta0, teta1) - price[i]) * normalize(mileage[i], mileage))
            #print(normalize(mileage[i], mileage))
        #print("Prediction", predic(mileage[i], teta0, teta1), "/Prix", price[i])
        i += 1
    err_m = err_sum * (1 / m)
    #print("Somme des erreurs:", err_sum, "m:", m)
    return err_m

def linear_regression():
    price = []
    mileage = []

    with open("data.csv", "r") as fichier_csv:
        reader = csv.reader(fichier_csv)
        for line in reader:
            if line[0] != "km":
                mileage.append(float(line[0]))
            if (line[1] != "price"):
                price.append(float(line[1]))
    #print("prices:", price)
    #print("km:", mileage)
    m = len(mileage)
    teta0 = 0
    teta1 = 0
    #coder une fonction pour ajuster le learning rate
    learning_rate = 0.000041 
    i = 0
    errs = []
    while i < 10000: 
        err_m = calculat_err_m(m, mileage, price, teta0, teta1, 0)
        errs.append(err_m)
        print("Moyenne des erreurs", err_m)
        old0 = teta0
        old1 = teta1
        teta0 -= (learning_rate * calculat_err_m(m, mileage, price, old0, old1, 0))
        teta1 -= (learning_rate * calculat_err_m(m, mileage, price, old0, old1, 1))
        print("teta0:", teta0, ",teta1:", teta1)
        i += 1
    print(min(errs, key=abs))
    #il faut que l'erreur totale soit la plus petite possible
    #definir un learning rate a ajuster
    #appliquer la formule pour ajuster teta0
    #appliquer la formule pour ajuster teta1
linear_regression()



