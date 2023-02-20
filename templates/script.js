




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
    <td>${customer.name}</td>
    <td>${customer.lastname}</td>
    <td>${customer.email}</td>
    <td>${customer.phone}</td>
    <td style="text-align:center"><a href="#" onclick="edit(${customer.id})" class="myButton">Modifica</a>
                                 <a href="#" onclick="remove(${customer.id})" class="myButtonD">Elimina</a></td>
    </tr>` 

    html += row;
    }
 
    document.querySelector('#customers > tbody').outerHTML = html;
}

function edit(id) {
    abrirFormulario()
    var customer = customers.find(x => x.id == id)
    document.getElementById('txtId').value = customer.id;
    document.getElementById('txtFirstname').value = customer.name;
    document.getElementById('txtLastname').value = customer.lastname;
    document.getElementById('txtEmail').value = customer.email;
    document.getElementById('txtPhone').value = customer.phone;
    document.getElementById('txtAddress').value = customer.address;
     
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
    document.getElementById('txtFirstname').value = '';
    document.getElementById('txtLastname').value = '';
    document.getElementById('txtEmail').value = '';
    document.getElementById('txtPhone').value = '';
    document.getElementById('txtAddress').value = '';
}





async function save() {
    var id = document.getElementById('txtId').value;
    // dacument.getelementbyid('txtFirstname').value
    var data = {
        'name': document.getElementById('txtFirstname').value,
        'lastname': document.getElementById('txtLastname').value,
        'email': document.getElementById('txtEmail').value,
        'phone': document.getElementById('txtPhone').value,
        'address': document.getElementById('txtAddress').value
    }

    if (id != '') {
        data.id = id
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


