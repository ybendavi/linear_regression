import pandas as pd

def estimatePrice(mileage, teta0, teta1):
    return (teta0 + (teta1 * mileage))

def calculate_ssr(datas, teta0, teta1):
    square_differences = []
    for index, row in datas.iterrows():
        square_differences.append(pow(estimatePrice(row["km"], teta0, teta1) - row["price"], 2))
    return sum(square_differences)

def square_difference(column, mean_price):
    return (pow(column - mean_price, 2))

def calcluate_r2(datas, teta0, teta1):
    # La formule pour le calculer est 1 - ssr(Residual Sum  of Square)/sst(Total sum of of Square)
    # On va d'abord avoir besoin de la moyenne des valeurs reel (prix)
    mean_price = datas["price"].sum() / len(datas["price"])
    # Maintenant on calcul la SST (la somme des ecarts entre les valeurs reelles et la moyenne au carre)
    sst = (datas["price"].apply(square_difference, args=(mean_price,))).sum()
    #print(sst)
    # On calcul la SSR (somme des ecarts entre valeurs predite et valeur reel au carre)
    ssr = calculate_ssr(datas, teta0, teta1)
    #print(ssr)
    # On applique la formule
    r2 = 1 - ssr / sst
    return r2
    


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
    #Pour calculer la precision j'ai choisi d'utiliser le coefficient de determination
    print(calcluate_r2(datas, teta0, teta1))

main()