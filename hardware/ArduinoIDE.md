<h1 align="center"><img src="https://user-images.githubusercontent.com/16292535/150152830-a0077ec7-d677-4e19-b282-04401bb5a060.png" alt="logos Ceweb.br NIC.br CGI.br " width="250" height="auto"></h1>

<h1 align="center">
    <img src="https://ceweb.br/media/imgs/Moverse_na_Web_banner-site.jpg" alt="Vamos transformar Brumadinho. Projeto Mover-se na WEB!" width="450" height="auto">
</h1>

<h1 align="center"> Sistema de Monitoramento em Tempo Real de Qualidade de Água de um Rio </h1>

<h2 align="center"> Detalhes da Configuração do Arduino IDE </h2>


Para enviar o sketch da estação (disponível [aqui](sketch/station.ino)) para placa será necessário utilizar o [Arduino IDE](https://www.arduino.cc/en/software). Através dessa ferramenta será necessário instalar as seguintes bibliotecas:

* ArduinoJson
* DallasTemperature
* OneWire 

E adicionar a url das configurações placa TTGO na opção de preferências do Arduino IDE, conforme indicado na documentação da placa TTGO. 

![URLs das placas](img/arduino_ide_1.png)

URL: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

Também será necessário configurar a IDE da seguinte forma, como exibido na figura: 

```
Placa: "ESP32 Wrover Module"
Upload Speed: "921600"
Flash Frequency: "80MHz"
Flash Mode: "QIO"
Partition Scheme: "Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS)"
Core Debug Level: "Nenhum"
```

![Configuração da IDE](img/arduino_ide_2.png)

A última etapa é plugar a placa na USB do computador e enviar o sketch para a TTGO.
