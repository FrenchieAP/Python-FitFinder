var axios = require('axios');

let apiKey;

async function fetchApiKey() {
    const response = await fetch('/api_key');
    const data = await response.json();
    apiKey = data.api_key;
}

var config = {
    method: 'get',
    url: 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=gyms-in-seattle&key=GOOGLE_API_KEY',
    headers: {}
};

axios(config)
    .then(function (response) {
        console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
        console.log(error);
    });

function search(e){
    e.preventDefault();
    var searchForm = document.getElementById('searchForm')
    var form = new FormData(searchForm);
    fetch('http://localhost:5000/search',{method:'POST',body:form})
        .then(res => res.json() )
        .then( data => console.log(data) )
}


