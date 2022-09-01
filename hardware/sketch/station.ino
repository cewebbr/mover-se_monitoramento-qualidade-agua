#include <ArduinoJson.h>
#include <WiFiClientSecure.h>
// Bibliotecas do Sensor de Temperatura
#include <OneWire.h>
#include <DallasTemperature.h>
//#include <EEPROM.h>
#ifdef ESP8266
  #include <ESP8266WiFi.h>
  #include <ESP8266HTTPClient.h>
  #include <coredecls.h>    // settimeofday_cb()
#else
  #include <WiFi.h>
  #include <HTTPClient.h>
#endif

// WiFi
const char* ssid = "SSID-WIFI";
const char* password = "PASSWORRD-WIFI";

const String url_principal = "http://URL-SERVIDOR/api/";
const int tempo_sleep = 5; // minutos

// Estação
const char* base_id = "station2"; //Modificar para o ID da Estação
const int versao = 1;
int qtdSensores;

// Configuração de hora
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -3 * 60 * 60;   // -3h*60min*60s = -10800s
const int daylightOffset_sec = 0;              // Fuso em horário de verão
time_t nextNTPSync = 0;
time_t hora_atual;

// JSON
const int capacidade = JSON_OBJECT_SIZE(5) + JSON_OBJECT_SIZE(2)+ JSON_OBJECT_SIZE(8);
StaticJsonDocument<capacidade> doc;

const int capacidadeResposta = JSON_ARRAY_SIZE(4) + JSON_OBJECT_SIZE(2) + 50;
DynamicJsonDocument documento(capacidadeResposta);

// Sensor de PH
const int ph_pin = 33;
float PH_step;

const float PH4 = 3.25;
const float PH7 = 2.37;

// Sensor de Temperatura
const int temp_pin = 32;
#ifdef ESP8266
  OneWire oneWire(D1);
#else
  OneWire oneWire(temp_pin);
#endif
DallasTemperature temp(&oneWire);
DeviceAddress address;

// Sensor de Turbidez
const int tds_pin = 35;
const int qtdLeituras = 16;
float leituras_turbidez[16];


// conexão
WiFiClient client;
HTTPClient httpClient;

bool conectarWiFi() {
  Serial.println("Tentando estabelecer uma conexao com a rede Wi-Fi...");

  const unsigned long tempoInicial = millis();

  WiFi.begin(ssid, password);

  do {
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("Conexao Wi-Fi estabelecida com sucesso!");
      IPAddress ip = WiFi.localIP();
      Serial.print("IP local: ");
      Serial.printf("%d.%d.%d.%d\n", ip[0], ip[1], ip[2], ip[3]);
    
      return true;
    }
  
  delay(1000);
  
  } while ((millis() - tempoInicial) < 30000L);

  Serial.println("Impossivel estabelecer uma conexao com a rede Wi-Fi!");

  return false;
}

bool verificarWiFi() {
  if (WiFi.status() == WL_CONNECTED)
    return true;
  
  Serial.println("Conexao Wi-Fi perdida.");
  
  WiFi.disconnect(true);
  
  delay(5000);
  
  return conectarWiFi();
}

void configurar_httpClient() {
  //criar constante para url 
  httpClient.begin(client, url_principal + "post_sensor_value");
  httpClient.setTimeout(30000);
  httpClient.setReuse(false);
  httpClient.addHeader("Content-Type", "application/json");
}

void config_station(){
  String serverPath = url_principal + "config_station/" + (String)base_id;
  Serial.println(serverPath);
  httpClient.begin(serverPath.c_str());

  int httpCode = httpClient.GET();
  Serial.println(httpCode);
  if (httpCode < 0) { // caso o status for negativo, mostrará a mensagem no monitor serial
    Serial.println("request error - " + httpCode);
    economizar_energia(tempo_sleep);
  }
  else if (httpCode == HTTP_CODE_OK) {
    String payload = httpClient.getString();
    Serial.print("payload: ");
    Serial.println(payload);
    
    DeserializationError erro = deserializeJson(documento, payload);
    if (erro) {
      Serial.print("Erro ao realizar o parse do JSON: ");
      Serial.println(erro.c_str());
    } else {
      qtdSensores = documento["quantidade"];
      Serial.print("qtdSensores: ");
      Serial.println(qtdSensores);
//      EEPROM.write(1, documento["quantidade"]);

    }
  } else {
    Serial.println("request - " + httpCode);
  }
  httpClient.end(); // finaliza a conexao
}

// Obtém o status da sincronização
bool atualizacao_hora() {
  if (nextNTPSync > 0) {
    return true;
  } else {
    Serial.println("Data e horas não aualizadas");
    delay(5000);
    return atualizacao_hora();
  }
}

// Callback de sincronização
#ifdef ESP8266
  void ntpSync_cb() {
#else
  void ntpSync_cb(struct timeval *tv) {
#endif
  time_t t;
  t = time(NULL);  
  nextNTPSync = t + (SNTP_UPDATE_DELAY / 1000) + 60; // Data/Hora da próxima atualização

  Serial.println("Sincronizou com NTP em " + dateTimeStr(t));
  Serial.println("Limite para próxima sincronização é " + dateTimeStr(nextNTPSync));
}

// Formatação da time_t como "aaaa-mm-ddThh:mm:ss"
String dateTimeStr(time_t t) {
  if (t == 0) {
    return "N/D";
  } else {                              
    struct tm * ptm = localtime(&t);
    String s;
    s += ptm->tm_year + 1900;
    s += "-";
    if (ptm->tm_mon < 9) {
      s += "0";
    }
    s += ptm->tm_mon + 1;
    s += "-";
    if (ptm->tm_mday < 10) {
      s += "0";
    }
    s += ptm->tm_mday;
    s += "T";
    if (ptm->tm_hour < 10) {
      s += "0";
    }
    s += ptm->tm_hour;
    s += ":";
    if (ptm->tm_min < 10) {
      s += "0";
    }
    s += ptm->tm_min;
    s += ":";
    if (ptm->tm_sec < 10) {
      s += "0";
    }
    s += ptm->tm_sec;
    return s;
  }
}

// leitura do sensor de temperatura
float temperatura(){
  temp.requestTemperatures();
  float temperatura = temp.getTempC(address);
  return temperatura;
}

// leitura do sensor de ph
float ph(){
  int measure = analogRead(ph_pin); 
  double voltage = 3.3 / 4095.0 * measure;
  Serial.println(voltage);
  PH_step = (PH4 - PH7) / 3;
  float ph = 7.00 + ((PH7 - voltage) / PH_step);
  return ph;
}

// leitura do sensor de turbidez
void sortLeituras(float *buff, int len)
{
  int i, z, pos;
  float tmp;

  for (i = 0; i < (len - 1); i++)
  {
    pos = i;
    for (z = i + 1; z < len; z++)
    {
      if (buff[pos] > buff[z])
        pos = z;
    }
    if (pos != i)
    {
      tmp = buff[i];
      buff[i] = buff[pos];
      buff[pos] = tmp;
    }
  }
}

float tds() {
  float leitura = 0.0;
  for (int i = 0; i < qtdLeituras; i++) {
    leituras_turbidez[i] = analogRead(tds_pin);
    delay(200);
  }

  sortLeituras(leituras_turbidez, qtdLeituras);

  for (int z = qtdLeituras/4; z < (3*(qtdLeituras/4)); z++) {
    leitura += leituras_turbidez[z];
  }

  leitura = leitura/(qtdLeituras/2);
  float turbidity = map(leitura, 0, 3930, 1000, 0);
  Serial.print("leitura: ");
  Serial.println(leitura);
  Serial.print("turbidity: ");
  Serial.println(turbidity);

  return turbidity;
}

void economizar_energia(int minutos) {
//  ESP.deepSleep(60 * 1e6 * minutos, WAKE_RF_DEFAULT);
  ESP.deepSleep(60 * 1e6 * minutos);
}

void setup() {
  Serial.begin(115200);

  // Para evitar perder as primeiras mensagens do console
  Serial.println();
  Serial.flush();
  delay(1000);
  Serial.println();
  Serial.flush();
  delay(1000);
  
  Serial.println("Iniciando...");

  //configuração de servidor para atualizar data e hora
  #ifdef ESP8266
    settimeofday_cb(ntpSync_cb);
  #else
    sntp_set_time_sync_notification_cb(ntpSync_cb);
  #endif
  
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  
  WiFi.mode(WIFI_STA);
  conectarWiFi();
  config_station();

  //sensor de temperatura
  temp.begin();
  temp.getAddress(address, 0);

}

void loop() {
  
  if (!verificarWiFi())
    return;

  if (!atualizacao_hora())
    return;

  configurar_httpClient();

  hora_atual = time(NULL);
  
  Serial.println("Enviando requisicao POST HTTPS...");

  String sensores[qtdSensores];
  JsonArray sensorsArray = documento["sensors"];

  for (int i = 0; i < qtdSensores; i++){ 
    sensores[i] = sensorsArray[i].as<String>();
    Serial.println(sensores[i]);
  }

  doc["base_id"] = base_id;
  doc["datetime"] = dateTimeStr(hora_atual);
  doc["version"] = versao;
  JsonObject gps = doc.createNestedObject("gps");
  gps["lat"] = 12345.123;
  gps["lng"] = 1212.123;
  JsonObject sensors = doc.createNestedObject("sensors");
  for (int i = 0; i < qtdSensores; i++){
    if (sensores[i] == "tds"){
      sensors[sensores[i]] = tds();
    }
    if (sensores[i] == "ph"){
      sensors[sensores[i]] = ph();
    }
    if (sensores[i] == "temp"){
      sensors[sensores[i]] = temperatura();
    }    
  }
    
  String json;
  serializeJson(doc, json);
  Serial.println(json);
  
  int statusCode = httpClient.POST(json);
  
  if (statusCode > 0) {
    Serial.print("Status code: ");
    Serial.println(statusCode);
    
   
    Serial.print("Content-Length: ");
    Serial.println(httpClient.getSize());
    
    if (statusCode == HTTP_CODE_CREATED) {
      
      String body = httpClient.getString();
      Serial.println(body);
      
    }
    if (statusCode == HTTP_CODE_NOT_FOUND) {
      const int capacidade = JSON_OBJECT_SIZE(1);
      StaticJsonDocument<capacidade> documento;
      
      String body = httpClient.getString();
      Serial.println(body);
    }
  } else {
    Serial.print("Ocorreu um erro de comunicacao: ");
    Serial.println(httpClient.errorToString(statusCode));
  }
  
  httpClient.end();
  
  Serial.println();
  Serial.println("Aguardando para repetir o processo...");

  //economia de energia
  economizar_energia(tempo_sleep);
}
