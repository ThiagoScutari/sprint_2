#include <WiFi.h>
#include <DHT.h>
#include <time.h>
#include <SPIFFS.h>   // ← Biblioteca para sistema de arquivos
#include "secrets.h"  // ← inclui dados sensíveis

#define PINO_DHT 23
#define MODELO_DHT DHT22

DHT dht(PINO_DHT, MODELO_DHT);
unsigned long id = 1;

void setup() {
    Serial.begin(115200);
    dht.begin();

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Conectando ao Wi-Fi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWi-Fi conectado com sucesso!");

    configTime(-3 * 3600, 0, "pool.ntp.org");

    struct tm timeinfo;
    while (!getLocalTime(&timeinfo)) {
        Serial.println("Aguardando sincronização NTP...");
        delay(1000);
    }

    Serial.println("id,datetime,temperatura,umidade");
}

void loop() {
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
        Serial.println("Falha ao ler do sensor DHT!");
        delay(2000);
        return;
    }

    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        Serial.println("Erro ao obter hora local");
        delay(2000);
        return;
    }

    char datetime[25];
    strftime(datetime, sizeof(datetime), "%Y-%m-%d %H:%M:%S", &timeinfo);

    String linha = String(id) + "," + String(datetime) + "," + String(t, 2) + "," + String(h, 2);
    Serial.println(linha);

    id++;
    delay(2000);
}
