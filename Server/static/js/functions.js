// fetch('http://127.0.0.1:5000/data?greenhouse=1&amount=20')
//   .then(function (response) {
//     return response.json();
//   })
//   .then(function (data) {
//     appendData(data);
//   })
//   .catch(function (err) {
//     console.log(err);
//   });

// function appendData(data) {
// const datatable = document.querySelector(".dataDisplay");
// for (let i = 0; i < data.results.length; i++) {
//     const row = document.createElement("tr");
//     row.innerHTML = 
//     '<td>' + data.results[i].Greenhouse_number + '</td>' 
//     +'<td>' + data.results[i].time + '</td>' 
//     +'<td>' + data.results[i].light_level + '</td>'
//     +'<td>' + data.results[i].humidity + '</td>' 
//     +'<td>' + data.results[i].temperature + '</td>' 
//     datatable.appendChild(row);
// }
// }
$(document).ready(function(){
  getAllData()
  setInterval(function(){getData()}, 30000);
});

function getData(){
  const parameters = GetParameters()
  const greenhouse = parameters.get('greenhouse')
  document.title = `Everlast | Greenhouse ${greenhouse}`
  // let greenhouse = $("#input_greenhouse").val()
  // let amount = $("#input_amount").val()
  $.getJSON(`http://127.0.0.1:5000/data?greenhouse=${greenhouse}&amount=10`, function(data){
    const results = data.results
    let newresults = results.map(result => `<tr><td>${result.Greenhouse_number}</td><td>${result.Sensor_ID}</td><td>${result.time}</td><td>${result.light_level}</td><td>${result.humidity}</td><td>${result.temperature}</td></tr>`)
    $(".dataDisplay").empty()
    $(".dataDisplay").append(newresults)
  });
}

function getAverages(parameter){
  const greenhouse = parameter.get('greenhouse')
  // let greenhouse = $("#input_greenhouse").val()
  $.getJSON(`http://127.0.0.1:5000/data/averages?greenhouse=${greenhouse}`, function(data){
    const results = data.results
    let newresults = results.map(result => `<td>${result.average_light_Level}</td><td>${result.average_humidity}</td><td>${result.average_humidity}</td>`)
    $(".Display.Average td:nth-child(2) , .Display.Average td:nth-child(3), .Display.Average td:nth-child(4)").remove()
    $(".Display.Average td:nth-child(1)").after(newresults)
  });
}

function getLowest(parameter){
  const greenhouse = parameter.get('greenhouse')
  // let greenhouse = $("#input_greenhouse").val()
  $.getJSON(`http://127.0.0.1:5000/data/minimum?greenhouse=${greenhouse}`, function(data){
    const results = data.results
    let newresults = results.map(result => `<td>${result.lowest_light_Level}</td><td>${result.lowest_humidity}</td><td>${result.lowest_humidity}</td>`)
    $(".Display.Lowest td:nth-child(2) , .Display.Lowest td:nth-child(3), .Display.Lowest td:nth-child(4)").remove()
    $(".Display.Lowest td:nth-child(1)").after(newresults)
  });
}

function getHighest(parameter){
  const greenhouse = parameter.get('greenhouse')
  // let greenhouse = $("#input_greenhouse").val()
  $.getJSON(`http://127.0.0.1:5000/data/highest?greenhouse=${greenhouse}`, function(data){
    const results = data.results
    let newresults = results.map(result => `<td>${result.highest_light_Level}</td><td>${result.highest_humidity}</td><td>${result.highest_humidity}</td>`)
    $(".Display.Highest td:nth-child(2) , .Display.Highest td:nth-child(3), .Display.Highest td:nth-child(4)").remove()
    $(".Display.Highest td:nth-child(1)").after(newresults)
  });
}

function getAllData(){
  const parameters = GetParameters()
  getData()
  getAverages(parameters)
  getLowest(parameters)
  getHighest(parameters)
}

function GetParameters(){
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  return urlParams
}