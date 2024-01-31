// Kirjastot DHT:lle ja LCD:lle
#include <LiquidCrystal.h>
#include <DHT22.h>

// LCD:n ja DHT:n alustus
LiquidCrystal lcd(12,11,5,4,3,2);
DHT22 dht22(6);

// Muuttujat lämpötilalle ja kosteudelle (liukuluku tarkan arvon mittaamiseksi)
float temp;
float hum;

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
  temp = lampotila();
  lcd.setCursor(0, 1);
  hum = kosteus();
  tulosta(temp, hum);
  delay(5000);
}

// Lukee anturilta lämpötilan
float lampotila() {
  temp = dht22.getTemperature();
  lcd.print("Lampot.: ");
  lcd.print(temp, 1); 
  lcd.print(" C");
  return temp;
}

// Lukee anturilta kosteuden
float kosteus() {
  hum = dht22.getHumidity();
  lcd.print("Kosteus: ");
  lcd.print(hum, 0); 
  lcd.print(" %");
  return hum;
}

void tulosta (float temp, float hum) {
  Serial.print(temp);
  Serial.print("-");
  Serial.println(hum);
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