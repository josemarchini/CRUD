




document.addEventListener('DOMContentLoaded', init);
const URL_API = 'http://localhost:5000/api/';

var customers = [];

// Search
function init() {
    search()
}


function agregar () {
    clean();
    abrirFormulario();
}

// Modal 
function abrirFormulario() {
    htmlModal = document.getElementById('modal');
    htmlModal.setAttribute('class', 'modale opened');
} 
function cerrarModal() {
    htmlModal = document.getElementById('modal');
    htmlModal.setAttribute('class', 'modale');
}



// Search 
async function search() {
    var url = URL_API + "customers";
    var response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    customers = await response.json();
    
    var html= '';
    for (customer of customers) { 
        var row = `<tr>
    <td>${customer.Country}</td>
    <td>${customer.Rank}</td>
    <td>${customer.Happiness_score}</td>
    <td>${customer.Year_score}</td>
    <td>${customer.Parameters}</td>
    <td>${customer.Value_parameters}</td>
    
    <!-- <td style="text-align:center"><a href="#" onclick="edit(${customer.Id})" class="myButton">Modifica</a>
                                 <a href="#" onclick="remove(${customer.Id})" class="myButtonD">Elimina</a></td>
    </tr> -->` 

    html += row;
    }
 
    document.querySelector('#customers > tbody').outerHTML = html;
}

function edit(Id) {
    abrirFormulario()
    var customer = customers.find(x => x.Id == Id)
    document.getElementById('txtId').value = customer.Id;
    document.getElementById('txtCountry').value = customer.Country;
    document.getElementById('txtRank').value = customer.Rank;
    document.getElementById('txtHappiness_score').value = customer.Happiness_score;
    document.getElementById('txtYear_score').value = customer.Year_score;
    document.getElementById('txtParameter').value = customer.Parameters;
    document.getElementById('txtValue_parameters').value = customer.Value_parameters;
     
}


async function remove(id) {
    respuesta = confirm ("Sei sicuro di voler eliminare il cliente?");
    if (respuesta) {
        var url = URL_API + "customers/" + id;
        await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        
        window.location.reload();
    }
}


function clean() {
    document.getElementById('txtId').value = '';
    document.getElementById('txtCountry').value = '';
    document.getElementById('txtRank').value = '';
    document.getElementById('txtHappiness_score').value = '';
    document.getElementById('txtYear_score').value = '';
    document.getElementById('txtParameters').value = '';
    document.getElementById('txtValue_parameters').value = '';
    
}





async function save() {
    var Id = document.getElementById('txtId').value;
    // dacument.getelementbyid('txtFirstname').value
    var data = {
        'Country': document.getElementById('txtCountry').value,
        'Rank': document.getElementById('txtRank').value,
        'Happiness_score': document.getElementById('txtHappiness_score').value,
        'Year_score': document.getElementById('txtYear_score').value,
        'Parameters': document.getElementById('txtParameters').value,
        'Value_parameters': document.getElementById('txtValue_parameters').value,
        
    }

    if (Id != '') {
        data.Id = Id
    }


    var url = URL_API + "customers";
    await fetch(url, {
        //mode: 'cors',
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {console.log(data);})
    .catch(error => {console.error(error)})

    window.location.reload();  
}

//voglio creare la funcion link1 que mi porti a http://localhost:5000/risultato

function link1() {
    window.location.href = "http://localhost:5000/risultato";
}

//voglio creare la funcion link2 que mi porti a http://localhost:5000/risultato1

function link2() {
    window.location.href = "http://localhost:5000/risultato1";
}

//voglio creare la funcion link3 que mi porti a http://localhost:5000/risultato2

function link3() {
    window.location.href = "http://localhost:5000/risultato2";
}







