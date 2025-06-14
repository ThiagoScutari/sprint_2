#include <WiFi.h>
#include <time.h>
#include "secrets.h"  // Define WIFI_SSID e WIFI_PASSWORD

#define TRIG_PIN 23
#define ECHO_PIN 22

void setup() {
  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Conexão Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado com sucesso!");

  // Sincroniza horário via NTP
  configTime(-3 * 3600, 0, "pool.ntp.org");
  struct tm timeinfo;
  while (!getLocalTime(&timeinfo)) {
    Serial.println("Aguardando sincronização NTP...");
    delay(1000);
  }

  Serial.println("data_hora,distancia_cm");
}

void loop() {
  // Leitura do sensor HC-SR04
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance_cm = duration * 0.034 / 2;

  // Obtenção da data/hora
  struct tm timeinfo;
  if (getLocalTime(&timeinfo)) {
    char datetime[25];
    strftime(datetime, sizeof(datetime), "%Y-%m-%d %H:%M:%S", &timeinfo);

    // Exibe resultado no formato desejado
    Serial.print(datetime);
    Serial.print(",");
    Serial.println(distance_cm, 1);  // 1 casa decimal
  } else {
    Serial.println("Erro ao obter hora local");
  }

  delay(500);  // Aguarda meio segundo para próxima leitura
}
