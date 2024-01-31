import serial
import time
import csv
import pandas as pd

tiedosto = "arvot2.csv"
excel = "arvot2.xlsx"

# Sarjaportin tiedot
sarjaportin_nimi = 'COM5'
sarjaportin_nopeus = 9600

# Sarjaportin alustus
sarjaportti = serial.Serial(sarjaportin_nimi, sarjaportin_nopeus, timeout=1)

def lue_sarjaportti():
    try:
        while True:
            data = sarjaportti.readline().decode('utf-8').strip()
            if data:
                vie_csv(data)
                vie_exceliin(data)
    finally:
        sarjaportti.close()
        print("Sarjaportti vapautettu.")

def vie_csv(data):
    try:
        with open(tiedosto, mode='a', newline='') as csv_tiedosto:
            csv_writer = csv.writer(csv_tiedosto)
            aika = time.strftime('%Y-%m-%d %H:%M:%S')
            lampotila, kosteus = erottele(data)
            rivi = [aika, lampotila, kosteus]
            csv_writer.writerow(rivi)

    except Exception as e:
        print(f"Virhe tallennettaessa tiedostoon: {e}")

def vie_exceliin(data):
    try:
        aika = time.strftime('%Y-%m-%d %H:%M:%S')
        lampotila, kosteus = erottele(data)
        try:
            df = pd.read_excel(excel)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Aika", "Lämpötila", "Kosteus"])

        uusi_rivi = pd.DataFrame([[aika, lampotila, kosteus]], columns=['Aika', 'Lämpötila', 'Kosteus'])
        df = pd.concat([df, uusi_rivi], ignore_index=True)
        df.to_excel(excel, index=False)
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
