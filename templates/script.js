




document.addEventListener('DOMContentLoaded', init);
const URL_API = 'http://localhost:3000/api/';

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
    <td>${customer.GDP_per_capita}</td>
    <td>${customer.Social_support}</td>
    <td>${customer.Life_expectancy}</td>
    <td>${customer.Freedom}</td>
    <td>${customer.Generosity}</td>
    <td>${customer.Perceptions_of_corruption}</td>
    <td>${customer.Dystopia}</td>
    <td style="text-align:center"><a href="#" onclick="edit(${customer.Id})" class="myButton">Modifica</a>
                                 <a href="#" onclick="remove(${customer.Id})" class="myButtonD">Elimina</a></td>
    </tr>` 

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
    document.getElementById('txtGDP_per_capita').value = customer.GDP_per_capita;
    document.getElementById('txtSocial_support').value = customer.Social_support;
    document.getElementById('txtLife_expectancy').value = customer.Life_expectancy;
    document.getElementById('txtFreedom').value = customer.Freedom;
    document.getElementById('txtGenerosity').value = customer.Generosity;
    document.getElementById('txtPerceptions_of_corruption').value = customer.Perceptions_of_corruption;
    document.getElementById('txtDystopia').value = customer.Dystopia;
     
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
    document.getElementById('txtGDP_per_capita').value = '';
    document.getElementById('txtSocial_support').value = '';
    document.getElementById('txtLife_expectancy').value = '';
    document.getElementById('txtFreedom').value = '';
    document.getElementById('txtGenerosity').value = '';
    document.getElementById('txtPerceptions_of_corruption').value = '';
    document.getElementById('txtDystopia').value = '';
}





async function save() {
    var Id = document.getElementById('txtId').value;
    // dacument.getelementbyid('txtFirstname').value
    var data = {
        'Country': document.getElementById('txtCountry').value,
        'Rank': document.getElementById('txtRank').value,
        'Happiness_score': document.getElementById('txtHappiness_score').value,
        'Year_score': document.getElementById('txtYear_score').value,
        'GDP_per_capita': document.getElementById('txtGDP_per_capita').value,
        'Social_support': document.getElementById('txtSocial_support').value,
        'Life_expectancy': document.getElementById('txtLife_expectancy').value,
        'Freedom': document.getElementById('txtFreedom').value,
        'Generosity': document.getElementById('txtGenerosity').value,
        'Perceptions_of_corruption': document.getElementById('txtPerceptions_of_corruption').value,
        'Dystopia': document.getElementById('txtDystopia').value
    }

    if (Id != '') {
        data.Id = Id
    }


    var url = URL_API + "customers";
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    window.location.reload();  
}









