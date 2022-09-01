<h1 align="center"><img src="https://user-images.githubusercontent.com/16292535/150152830-a0077ec7-d677-4e19-b282-04401bb5a060.png" alt="logos Ceweb.br NIC.br CGI.br " width="250" height="auto"></h1>

<h1 align="center">
    <img src="https://ceweb.br/media/imgs/Moverse_na_Web_banner-site.jpg" alt="Vamos transformar Brumadinho. Projeto Mover-se na WEB!" width="450" height="auto">
</h1>

<h1 align="center"> Sistema de Monitoramento em Tempo Real de Qualidade de Água de um Rio </h1>

<h2 align="center"> Detalhes da Configuração do Hardware </h2>


Para enviar o sketch (código) para placa será necessário utilizar a Arduino IDE. Nela precisam ser instaladas as seguintes bibliotecas:

* ArduinoJson
* DallasTemperature
* OneWire 

E incluir a url da placa nas preferências, como exibido na figura abaixo.





URL DA PLACA TTGO: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

Também será necessário abrir o código e configurar a IDE da seguinte forma, como exibido na figura: 

Placa: "ESP32 Wrover Module"
Upload Speed: "921600"
Flash Frequency: "80MHz"
Flash Mode: "QIO"
Partition Scheme: "Default 4MB with spiffs (1.2MB APP/1.5MB SPIFFS)"
Core Debug Level: "Nenhum"




Por fim será necessário plugar a placa na USB do computador e enviar o sketch para a TTGO.