import pandas as pd
import math 
import matplotlib.pyplot as plt

#Fonction de visualisation
def visusalize(datas):
    plt.scatter(datas["km"], datas["price"], color="blue", label="Données réelles") 
    plt.plot(datas["km"], datas["estimated price"], color="red", label="Prédiction de la régression")
    plt.xlabel("Variable indépendante")
    plt.ylabel("Variable dépendante")
    plt.legend()
    plt.title("Visualisation de la régression linéaire")
    plt.show()

# Fonction de prediction
def estimatePrice(mileage, teta0, teta1):
    return (teta0 + (teta1 * mileage))

def printEstimatedPrice(column, tetas):
    return (tetas[0] + (teta[1] * mileage))

def normalize(number, n_min, n_max):
    return (number - n_min) / (n_max - n_min)

def calculate_square(column, mean):
    return (pow(column - mean, 2))

#Fonction pour calculer la variance qui est la moyenne des carrés des écarts de chaque valeur par rapport à la moyenne
def calculate_v(mean, column, size):
    new_col = column.apply(calculate_square, args=(mean,))
    square_mean = new_col.sum() / size
    return (square_mean)

#Fonction pour standardiser les valeurs
def standardize_column(column, standard_deviation, mean):
    return ((column - mean) / standard_deviation )

def destandardize_col(column, standard_deviation, mean):
    return ((column * standard_deviation) + mean)
#Fonctions pour destandardiser les teta
def destandardise_teta1(teta1, standard_deviation):
    return (teta1 / standard_deviation)

def destandardise_teta0(teta0, standard_deviation, m, teta1_d):
    return (teta0 * standard_deviation - m * teta1_d)
#Fonctions pour calculer les erreurs correspond a la partie estimatePrice(mileage[i]) − price[i] de la formule
def calculate_err_0(line, tmp0, tmp1, test):
    if test == 0:
        return (estimatePrice(line["s_km"], tmp0, tmp1) - line["price"])
    else:
        return (estimatePrice(line["km"], tmp0, tmp1) - line["price"])

# Pour le teta 1 il faut multiplier la marge d'erreur par le mileage par rapport a l'influence qu'il a sur la courbe
def calculate_err_1(line, tmp0, tmp1):
    return ((estimatePrice(line["s_km"], tmp0, tmp1) - line["price"]) * line["s_km"])

def calcute_sum_m(tmp0, tmp1, datas):
    tab0 = []
    tab1 = []
    # Je recupere le nombre de donnees
    m = datas.shape[0]

    for index, row in datas.iterrows():
        tab0.append(calculate_err_0(row, tmp0, tmp1, 0))
        tab1.append(calculate_err_1(row, tmp0, tmp1))
    # J'applique le 1/m * somme des erreurs
    sums_m = []
    try:
        sums_m.append(sum(tab0) * (1 / m))
    except Exception as e:
        print("Nombre en question:", sum(tab0), "/nError:", e)
    sums_m.append(sum(tab1) * (1 / m))
    return (sums_m)

# Ici je calcule la mean absolute error pour mes comparaisons d'erreurs car si j'utilise l'erreur moyenne les negatifs et positif vont s'annuler
def calculate_mae(tmp0, tmp1, datas):
    tab0 = []
    m = datas.shape[0]
    for index, row in datas.iterrows():
        tab0.append(abs(calculate_err_0(row, tmp0, tmp1, 1)))
    #print("sum:", sum(tab0), "   m:", m, "    1/m:", 1 / m)
    #print("tab:", tab0)
    err_m = sum(tab0) * (1 / m)
    return (err_m)
    
def ft_linear_regression(datas, teta0, teta1):
    tmp0 = teta0
    tmp1 = teta1
    new0 = tmp0
    new1 = tmp1
    s_tmp1 = 0
    s_tmp0 = 0
    #print(normalized_datas)
    #On va standardiser les valeurs pour ca on calcule l'ecart type
    mean_mileage = datas["km"].sum() /  len(datas["km"])
    standard_deviation_mileage = math.sqrt(calculate_v(mean_mileage, datas["km"], len(datas["km"])))
    datas["s_km"] = datas["km"].apply(standardize_column, args=(standard_deviation_mileage, mean_mileage))
    # On defini un learning rate de depart pour faire des pas plus ou moins grand sur la courbe d'erreur
    learning_rate = 0.000001
    nb_iterations = 50
    weaker_err = calculate_mae(tmp0, tmp1, datas)
    print("werror", weaker_err)
    #print ("datas:", datas)
    i = 0
    savedi = i
    while i < nb_iterations:

        # Il faut ici recuperer la moyenne de la somme des erreurs pour teta0 et teta1
        sums_m = calcute_sum_m(tmp0, tmp1, datas)
        
        # On peu maintenant recalculer teta0 et teta1
        tmp0 = tmp0 - learning_rate * sums_m[0]
        tmp1 = tmp1 - learning_rate * sums_m[1]
        s_tmp1 = destandardise_teta1(tmp1, standard_deviation_mileage)
        s_tmp0 = destandardise_teta0(tmp0, standard_deviation_mileage, mean_mileage, s_tmp1) 
        new_err = calculate_mae(s_tmp0, s_tmp1, datas)
        print("Moyenne d'erreur:",  new_err)
        #print("new err", new_err)
        if weaker_err > new_err:
            weaker_err = new_err
            new0 = s_tmp0
            new1 = s_tmp1
            savedi = i
        datas["estimated price"] = datas["km"].apply(estimatePrice, args=(s_tmp0, s_tmp1))
        visusalize(datas)
        i += 1
    print(weaker_err, " ", savedi)
    datas["estimated price"] = datas["km"].apply(estimatePrice, args=(new0, new1))
    print(datas, "/nNormailized tetas:", new0, " ", new1)
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



    

    
    