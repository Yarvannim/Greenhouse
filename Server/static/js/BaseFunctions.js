$(document).ready(function(){
    function getGreenhouses(){
        $.getJSON(`http://127.0.0.1:5000/data/greenhouses`, function(data){
          const results = data.results
          const newresults = results.map(result => `<a href="/greenhouse/?greenhouse=${result.greenhouse_id}"><div class="greenhouse"><img class='icon'/><p>Greenhouse ${result.greenhouse_number}</p></div></a>`)
          $(".greenhouses").prepend(newresults)
        })
      }
    getGreenhouses()
  });

