let flagButtonNode = document.getElementById('period-day-button')
let divPeriodDaysNode = document.getElementById('period-in-days')
let selectMonthNode = document.getElementById('date')

selectMonthNode.addEventListener('click', () => {
    var valueMonth = selectMonthNode.value
    var dayBegin = document.getElementById('begin')
    var dayEnd = document.getElementById('end')

    var date = new Date()
    var ano = date.getFullYear()
    
    var mes = (selectMonthNode === 'Selecionar o mês') ? date.getMonth() : valueMonth
    
    ultimo_dia = (new Date(ano,mes,0)).getDate()
    
    console.log(ultimo_dia)
    var mesAtual = (mes < 10) ? '0'+mes : mes

    var dataInicial = String(ano+'-'+mesAtual+'-01')
    var dataFinal = String(ano+'-'+mesAtual+'-'+ultimo_dia)

    if (selectMonthNode !== 'Selecione o mês' || selectMonthNode ) {
        dayBegin.value = dataInicial       
        dayEnd.value = dataFinal       
    }

})


flagButtonNode.addEventListener('click', () => {
    
    if (flagButtonNode.value == 'Periodo em dias'){

        divPeriodDaysNode.style.display = 'flex'
        selectMonthNode.style.display = 'none'
        flagButtonNode.setAttribute('value', 'Selecionar mês')
    }
    else {
        
        selectMonthNode.style.display = 'flex'
        divPeriodDaysNode.style.display = 'none'
        flagButtonNode.setAttribute('value', 'Periodo em dias')
    }

    
    
})
