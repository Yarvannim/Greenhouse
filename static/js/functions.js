fetch('http://127.0.0.1:5000/data?greenhouse=1&amount=20')
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    appendData(data);
  })
  .catch(function (err) {
    console.log(err);
  });

function appendData(data) {
const datatable = document.querySelector(".dataDisplay");
for (let i = 0; i < data.results.length; i++) {
    const row = document.createElement("tr");
    row.innerHTML = 
    '<td>' + data.results[i].Greenhouse_number + '</td>' 
    +'<td>' + data.results[i].time + '</td>' 
    +'<td>' + data.results[i].light_level + '</td>'
    +'<td>' + data.results[i].humidity + '</td>' 
    +'<td>' + data.results[i].temperature + '</td>' 
    datatable.appendChild(row);
}
}