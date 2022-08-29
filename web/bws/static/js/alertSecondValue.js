let selectOperador = document.getElementById('operador')
let secondValueNode = document.getElementById('second-value')

selectOperador.addEventListener('change', () => {
    if (selectOperador.value == 'Entre'){
        
        $(secondValueNode).empty()

        secondValueNode.style.display = 'inline'
        
        var labelNode = document.createElement('label')
        labelNode.setAttribute('class', 'label-description')
        labelNode.innerHTML = 'Segundo Valor:'
        secondValueNode.append(labelNode)
        
        var inputNode = document.createElement('input')
        inputNode.setAttribute('type', 'number')
        inputNode.setAttribute('placeholder', 'Digite aqui...')
        inputNode.setAttribute('class', 'form-control')
        inputNode.setAttribute('style', 'height: 45px;')
        inputNode.setAttribute('name', 'second_value')
        secondValueNode.append(inputNode)
    }
    else {
        secondValueNode.style.display = 'none'
    }
})