// var axios = require('axios');

// var config = {
//     method: 'get',
//     url: 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=gyms-in-seattle&key=AIzaSyBQMOQnqqPr_QUac8uC00J1ueX5jV3YjMc',
//     headers: {}
// };

// axios(config)
//     .then(function (response) {
//         console.log(JSON.stringify(response.data));
//     })
//     .catch(function (error) {
//         console.log(error);
//     });

function search(e){
    e.preventDefault();
    var searchForm = document.getElementById('searchForm')
    var form = new FormData(searchForm);
    fetch('http://localhost:5000/search',{method:'POST',body:form})
        .then(res => res.json() )
        .then( data => console.log(data) )
}


