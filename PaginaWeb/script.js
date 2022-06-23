//URL DEL API
const api_url = ('http://localhost:8000/api/v1/ezGet');

const ctx = document.getElementById('tablaEz');

//TOMA LOS DATOS DEL API
async function getData(){
    const response = await fetch(api_url);
    const data = await response.json();
    console.log(data);
    appendData(data);
    }

//MUESTRA LOS DATOS EN LA PAGINA
function appendData(data) {
    var nombres = [] , horas = []
    var datosEl = document.getElementById("datos");
        for (var i = 0; i < data.length; i++) {
            var div = document.createElement("div");

            div.innerHTML = 'DiscordID: ' + data[i].discordid + ' Horas: ' + data[i].hours.toFixed(2)
            + ' Ultima conexion: ' + moment(data[i].lasttimeconnected).format('MM/DD/YY');
            nombres.push(data[i].discordid)
            horas.push(data[i].hours)
            datosEl.appendChild(div);
        }
     
        const tablaEz = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: nombres,
                datasets: [{
                    label: 'Top más conectados',
                    data: horas,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

getData(); 


