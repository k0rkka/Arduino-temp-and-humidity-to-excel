// Kirjastot DHT:lle ja LCD:lle
#include <LiquidCrystal.h>
#include <DHT22.h>

// LCD:n ja DHT:n alustus
LiquidCrystal lcd(12,11,5,4,3,2);
DHT22 dht22(6);

// Muuttujat lämpötilalle ja kosteudelle (liukuluku tarkan arvon mittaamiseksi)
float temp;
float hum;
// Kaksialkioinen taulukkomuuttuja lämpötilalle ja kosteudelle
float mitatutArvot[2];

// Alustusfunktiossa avataan portti, alustetaan lcd ja tulostetaan tervehdys
void setup() {
  Serial.begin(9600);
  lcd.begin(16,2);
  //tervehdys();
  lcd.clear();
}

// Toistetaan loputtomasti
void loop() {
  lcd.clear();
  lampotila();
  lcd.setCursor(0, 1);
  kosteus();
  tulostaTaulukko();
  delay(5000);
}

// Lukee anturilta lämpötilan
void lampotila() {
  temp = dht22.getTemperature();
  tallennaTaulukkoon(temp, 'C');
  lcd.print("Lampot.: ");
  lcd.print(temp, 1); 
  lcd.print(" C");
}

// Lukee anturilta kosteuden
void kosteus() {
  hum = dht22.getHumidity();
  tallennaTaulukkoon(hum, '%');
  lcd.print("Kosteus: ");
  lcd.print(hum, 0); 
  lcd.print(" %");
}

// Funktio mitattujen arvojen taulukkomuuttujaan tallentamiseksi
void tallennaTaulukkoon(float arvo, char yksikko) {
  switch (yksikko) {
    case 'C':
      mitatutArvot[0] = arvo;
      break;

    case '%':
      mitatutArvot[1] = arvo;
      break;
  }
}

// Funktio uusimman alkion tulostamiseen terminaaliin jos sarjaportti auki
void tulostaTaulukko() {
  if (Serial) {
    Serial.print(mitatutArvot[0]);
    Serial.print(" C, Kosteus: ");
    Serial.print(mitatutArvot[1]);
    Serial.println(" %");
  } 
}

void tervehdys() {
  String luku = " Luetaan dataa anturilta";
  lcd.print(luku);
  int merkit = luku.length() - 1;
  for (int i = 0; i < merkit; i++) {
    lcd.scrollDisplayLeft();
    delay(100);
  }
}