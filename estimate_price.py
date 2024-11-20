
import pandas as pd

#formule pour renvoyer un point de la courbe en fonction du kilometrage
def estimatePrice(mileage, teta0, teta1):
    return (teta0 + (teta1 * mileage))

def main():
    mileage_str = input("Please enter a mileage:")
    mileage = 0
    try:
        mileage = int(mileage_str)
    except Exception as e:
        print("Bad input:", str(e))
        return
    tetas = None
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
    prediction = estimatePrice(mileage, teta0, teta1)
    print(prediction)
main()