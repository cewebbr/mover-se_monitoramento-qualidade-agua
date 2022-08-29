let modal = document.getElementById('div-modal')


document.getElementById('info-sensor').addEventListener('click', () => {

    var sensor = document.getElementById('sensor-type').value


    switch (sensor) {
        case 'tds':
            document.getElementById('title-info').innerText = 'Turbidez'
            document.getElementById('info').innerHTML = "A <strong>turbidez</strong> é a medida da dificuldade de um feixe de luz atravessar uma certa quantidade de água, conferindo uma aparência turva à mesma."+ 
            "Sendo assim, comprovando a presença de partículas em suspensão, resultando num aspecto turvo da água."
            break
        case 'ph':
            document.getElementById('title-info').innerText = 'PH ideal'
            document.getElementById('info').innerHTML = "A sigla <strong>pH</strong> significa <strong>Potencial Hidrogeniônico</strong>, e consiste num índice que indica a acidez, neutralidade ou alcalinidade de um meio qualquer. <br>" +  
            "A recomendação da American Public Health Association é que o pH varie de 7 a 10, o que caracteriza uma água neutra ou alcalina. Algumas águas possuem pH mais ácido, próximo de 5, enquanto outras possuem pH mais alcalino, ao redor de 9." + 
            "Nenhuma delas é imprópria para o consumo ou vai fazer mal á saúde. O ideal é que o pH da água mineral seja neutro, ao redor de 7."
            break
        case 'umidity':
            document.getElementById('title-info').innerText = 'Umidade'
            document.getElementById('info').innerHTML = "Umidade é relativo a quantidade de vapor d'água presente em determinado espaço"
            break
        case  'temp':
            break

    }

    modal.style.display = 'block'
    console.log('entrou')

})

document.getElementById('close-btn').addEventListener('click', () => {
    modal.style.display = 'none'
})

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}