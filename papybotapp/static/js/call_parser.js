function ajaxPost(url, data, callback) {
    let req = new XMLHttpRequest();
    req.open("POST", url);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            // Appelle la fonction callback en lui passant la réponse de la requête
            callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url);
        }
    });
    req.addEventListener("error", function () {
        console.error("Erreur réseau avec l'URL " + url);
    });
    req.send(data);
}


function initMap(lat, lng) {
    if (lat === undefined || lng === undefined) {
        lat = 0;
        lng = 0;
    }

    let myLatLng = {lat: lat, lng: lng};

    let map = new google.maps.Map(document.getElementById('map'), {
      zoom: 11,
      center: myLatLng
    });

    let marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      title: 'Ici mon petit !'
    });
  }

let form = document.querySelector("form");

form.addEventListener("submit", function (e) {
    e.preventDefault();

    document.getElementById("map").innerHTML = "";

    // Creating FormData and we pass it the input text to send it to the view
    let form = new FormData();
    form.append("query", e.target.elements.input.value);

    ajaxPost("/parser/", form, function (response) {
        response = JSON.parse(response);

        let displayElt = document.getElementById("display-result");

        // Creating a div who'll have 3 <p> elts : content, url and Papybot's answer
        let resultsElt = document.createElement("div");
        resultsElt.classList.add("results");

        // Inserting the last search on top
        displayElt.insertBefore(resultsElt, displayElt.childNodes[0]);

        // Content <p>
        let contentPElt = document.createElement("p");
        contentPElt.textContent = response.content;

        // Url <p>
        let urlPElt = document.createElement("p");
        let aElt = document.createElement("a");
        aElt.setAttribute("href", response.url);
        aElt.textContent = response.url;

        urlPElt.appendChild(aElt);

        // PapyBot's answer <p>
        let papybotPElt = document.createElement("p");
        papybotPElt.textContent = "PapyBot : " + response.bot_response;

        // Adding all 3 <p>
        resultsElt.appendChild(papybotPElt);
        resultsElt.appendChild(contentPElt);
        resultsElt.appendChild(urlPElt);

        console.log(response);

        // Display Google Map
        initMap(response.coords[0], response.coords[1]);
    })
});
