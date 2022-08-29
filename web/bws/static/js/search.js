$(document).ready(function(){

    $('.input-search').on('input', function(){
        if (!!$('#search-form').val()){
            $.ajax({
                type : 'GET',
                url : 'ajax/searchPointer/',
                data : { station : $('#search-form').val()},
                success : function(response) {  
                    $('#stations').empty();
                    var divNode = document.getElementById('stations');
                    
                    for (var keys in response.point){
                        var nameNode = document.createElement('a');
                        nameNode.setAttribute('class', 'btn btn-outline-primary');
                        nameNode.setAttribute('style', 'margin-top:10px;');
                        nameNode.setAttribute('id', 'station-container');
                        nameNode.setAttribute('href', response.point[keys].path + response.point[keys].id)
                        nameNode.setAttribute('target', 'blank');
                        nameNode.innerHTML = '<strong>' + response.point[keys].name + '</strong> <br>' + response.point[keys].description;
                        divNode.append(nameNode);
                    }
        
                },
                error : function(response){
                    alert(response.error);        
                }
            })
        }else{
            $('#point').empty();

        }
    });
    
    })
