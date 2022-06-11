//URL DEL API
const api_url = ('http://localhost:8000/api/v1/ezGet');

//TOMA LOS DATOS DEL API
async function getData(){
    const response = await fetch(api_url);
    const data = await response.json();
    console.log(data);
    appendData(data);
    }

//MUESTRA LOS DATOS EN LA PAGINA
function appendData(data) {
    var datosEl = document.getElementById("datos");
        for (var i = 0; i < data.length; i++) {
            var div = document.createElement("div");
            div.innerHTML = 'Name: ' + data[i].discordid + ' Hours: ' + data[i].hours
            + ' Last Time Connected: ' + data[i].lasttimeconnected;
            datosEl.appendChild(div);
        }
    }

getData(); 
