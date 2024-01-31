import serial
import time
import csv
import pandas as pd

csv_tiedosto = "arvot.csv"
excel_tiedosto = "arvot.xlsx"

sarjaportin_nimi = 'COM5'
sarjaportin_nopeus = 9600

sarjaportti = serial.Serial(sarjaportin_nimi, sarjaportin_nopeus, timeout=1)

def lue_sarjaportti():
    try:
        while True:
            data = sarjaportti.readline().decode('utf-8').strip()
            if data:
                lampotila, kosteus = erottele(data)
                vie_csv(lampotila, kosteus, csv_tiedosto)
                vie_exceliin(lampotila, kosteus, excel_tiedosto)
    finally:
        sarjaportti.close()
        print("Sarjaportti vapautettu.")

def vie_csv(lampotila, kosteus, csv_tiedosto):
    try:
        with open(csv_tiedosto, mode='w', newline='') as tiedosto:
            csv_kirjoittaja = csv.writer(tiedosto)
            aika = time.strftime('%Y-%m-%d %H:%M:%S')
            rivi = [aika, lampotila, kosteus]
            csv_kirjoittaja.writerow(rivi)

    except Exception as e:
        print(f"Virhe tallennettaessa tiedostoon: {e}")

def vie_exceliin(lampotila, kosteus, excel_tiedosto):
    try:
        aika = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            df = pd.read_excel(excel_tiedosto)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Aika", "Lämpötila", "Kosteus"])

        uusi_rivi = pd.DataFrame([[aika, lampotila, kosteus]], columns=['Aika', 'Lämpötila', 'Kosteus'])
        df = pd.concat([df, uusi_rivi], ignore_index=True)
        df.to_excel(excel_tiedosto, index=False)
    except Exception as e:
        print(f"Virhe tallennettaessa Excel-tiedostoon: {e}")

def erottele(data):
    osat = data.split("-")
    lampotila = osat[0]
    kosteus = osat[1]
    lampotila_arvo = float(lampotila)
    kosteus_arvo = float(kosteus)
    print(str(lampotila_arvo) +" C" + " - " + str(kosteus_arvo) + " %")
    return lampotila_arvo, kosteus_arvo

if __name__ == "__main__":
    try:
        lue_sarjaportti()
    except KeyboardInterrupt:
        print("Keskeytys. Suljetaan ohjelma.")
        sarjaportti.close()
