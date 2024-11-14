import pandas as pd

# Fonction de prediction
def estimatePrice(mileage, teta0, teta1):
    return (teta0 + (teta1 * mileage))

def normalize(number, n_min, n_max):
    return (number - n_min) / (n_max - n_min)

def normalize_column(column):
    n_min = column.min()
    n_max = column.max()
    return (column - n_min) / (n_max - n_min)
#Fonctions pour calculer les erreurs correspond a la partie estimatePrice(mileage[i]) − price[i] de la formule
def calculate_err_0(line, tmp0, tmp1):
        return (estimatePrice(line["km"], tmp0, tmp1) - line["price"])

# Pour le teta 1 il faut multiplie la marge d'erreur par le mileage normalise par a l'influence qu'il a sur la courbe
def calculate_err_1(line, tmp0, tmp1, min, max):
        return ((estimatePrice(line["km"], tmp0, tmp1) - line["price"]) * normalize(line["km"], min, max))

def calcute_sum_m(tmp0, tmp1, datas):
    tab0 = []
    tab1 = []
    vmin = datas["km"].min()
    vmax = datas["km"].max()
    # Je recupere le nombre de donnees
    m = datas.shape[0]

    for index, row in datas.iterrows():
        tab0.append(calculate_err_0(row, tmp0, tmp1))
        tab1.append(calculate_err_1(row, tmp0, tmp1, vmin, vmax))
    # J'applique le 1/m * somme des erreurs
    sums_m = []
    try:
        sums_m.append(sum(tab0) * (1 / m))
    except Exception as e:
        print("Nombre en question:", sum(tab0), "/nError:", e)
    sums_m.append(sum(tab1) * (1 / m))
    return (sums_m)
    
def ft_linear_regression(datas, teta0, teta1):
    tmp0 = teta0
    tmp1 = teta1
    normalized_datas = datas.apply(normalize_column)
    #print(normalized_datas)
    # On defini un learning rate de depart pour faire des pas plus ou moins grand sur la courbe d'erreur
    learning_rate = 0.000041
    nb_iterations = 10
    weaker_err = calcute_sum_m(tmp0, tmp1, datas)[0]
    #print ("datas:", datas)
    i = 0
    while i < nb_iterations:

        # Il faut ici recuperer la moyenne de la somme des erreurs pour teta0 et teta1
        sums_m = calcute_sum_m(tmp0, tmp1, datas)
        print(estimatePrice(82029, tmp0, tmp1))
        print("Moyenne d'etteur:", sums_m[0])
        # On peu maintenant recalculer teta0 et teta1
        tmp0 = tmp0 - learning_rate * sums_m[0]
        tmp1 = tmp1 - learning_rate * sums_m[1] 
        if abs(sums_m[0]) < abs(weaker_err):
            weaker_err = sums_m[0]
        i += 1
    print(weaker_err, " ", i)

def main():
    # Recuperation des donnees dans le csv
    datas = None
    tetas = None

    try:
        datas = pd.read_csv("data.csv")
    except Exception as e:
        print("Something went wrong with the csv file:", str(e))
        return
    # Recuperation des tetas dans un csv
    try:
        tetas = pd.read_csv("tetas.csv")
    except Exception as e:
        print("Something went wrong, there must be a file named tetas.csv with 2 column named teta0 and teta1 with one value each in the root of the project:", str(e))
        return
    teta0 = 0
    teta1 = 0
    try:
        teta0 = float(tetas["teta0"].iloc[0])
        teta1 = float(tetas["teta1"].iloc[0])
    except Exception as e:
        print("Something went wrong with teta0 and teta1 in the csv file:", str(e))
        return
    ft_linear_regression(datas, teta0, teta1)

main()



    

    
    