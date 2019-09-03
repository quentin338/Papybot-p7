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
    let needToDisplayMap = true;

    if (lat === undefined || lng === undefined) {
        lat = 0;
        lng = 0;
        needToDisplayMap = false;
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

    let mapHide = $('#map');
    // If we need to display the map, we always remove .map-hide, else we always add it.
    if (needToDisplayMap === false) {
        mapHide.toggleClass("map-hide", true);
    } else {
        mapHide.toggleClass("map-hide", false);
    }
  }

function deleteSearch() {
    $('#input').val("");
    $('#wiki-results').text("");

    initMap();
}

$('#btn-delete-search').click(deleteSearch);

function displayResult(response) {
    let lat = response.coords[0];
    let lng = response.coords[1];

    $('#wiki-results').text(response.content);

    // Saving data that will be displayed on the card if we save.
    let results = $('#results');
    results.attr("data-format-address", response.address);
    results.attr("data-wiki-url", response.url);
    results.attr("data-wiki-thumbnail", response.thumbnail);
    results.attr("data-coords", `${lat} ${lng}`);

    // Displaying the map
    initMap(lat, lng);
}

function alertHide(elt, btnType) {
        elt.hide("slow", function() {
            elt.toggleClass(btnType, false)
        });
}

// Custom display of an alert with "slow" show and hide
function alertDisplay(elt, message, btnType) {
    elt.toggleClass(btnType, true);
    elt.text(message);
    elt.show("slow", function() {
        setTimeout(function() {
            alertHide(elt, btnType);
        }, 3000);
    });
}

function createCard(formatAddress, wikiContent, wikiUrl, wikiThumbnail) {
    // Architecture of the card
    let mainElt = document.createElement("div");
    let rowElt = document.createElement("div");
    mainElt.appendChild(rowElt);

    let colThumbnailElt = document.createElement("div");
    let thumbnailElt = document.createElement("img");
    colThumbnailElt.appendChild(thumbnailElt);
    rowElt.appendChild(colThumbnailElt);

    let cardElt = document.createElement("div");
    let cardBodyElt = document.createElement("div");
    cardElt.appendChild(cardBodyElt);
    rowElt.appendChild(cardElt);

    let cardTitleElt = document.createElement("h5");
    let cardTextElt = document.createElement("p");
    let cardWikiLinkElt = document.createElement("a");
    let cardMapsLinkElt = document.createElement("a");

    cardBodyElt.appendChild(cardTitleElt);
    cardBodyElt.appendChild(cardTextElt);
    cardBodyElt.appendChild(cardWikiLinkElt);
    cardBodyElt.appendChild(cardMapsLinkElt);

    // Adding classes, attributes and content
    mainElt.classList.add("card", "mb-3", "results-card");
    rowElt.classList.add("row", "no-gutters");
    colThumbnailElt.classList.add("col-md-4", "saved-thumbnail");

    thumbnailElt.classList.add("card-img-top" , "card-img");
    thumbnailElt.setAttribute("src", wikiThumbnail);
    thumbnailElt.setAttribute("alt", "");

    cardElt.classList.add("col-md-8");
    cardBodyElt.classList.add("card-body", "text-center");

    cardTitleElt.classList.add("card-title");
    cardTitleElt.innerText = formatAddress;

    cardTextElt.classList.add("card-text");
    cardTextElt.innerText = wikiContent;

    cardWikiLinkElt.classList.add("btn", "btn-primary", "wiki-saved-link");
    cardWikiLinkElt.href = wikiUrl;
    cardWikiLinkElt.text = "Article Wikipédia";

    cardMapsLinkElt.classList.add("btn", "btn-primary", "google-maps-search");
    cardMapsLinkElt.href = `https://www.google.com/maps/search/?api=1&query=${formatAddress}`;
    cardMapsLinkElt.text = "Lien GoogleMaps";

    // Inserting the card at the top of the other cards if any
    let allCardsElt = $('#all-cards');
    allCardsElt.prepend(mainElt);
}


$('#btn-save-search').click(function() {
    let alertElt = $('#alert-msg');
    let wikiContent = $('#wiki-results').text();

    // We cut short if there is nothing to save
    if (wikiContent === "") {
        alertDisplay(alertElt, "Veuillez effectuer une recherche valide avant d'enregistrer.",
            "alert-warning");
        return
    }

    // Grabbing infos from page
    let resultsData = $('#results');

    let formatAddress = resultsData.attr("data-format-address");
    let wikiUrl = resultsData.attr("data-wiki-url");
    let wikiThumbnail = resultsData.attr("data-wiki-thumbnail");

    // Creation of the card
    console.log(formatAddress, wikiContent);
    createCard(formatAddress, wikiContent, wikiUrl, wikiThumbnail);

    alertDisplay(alertElt, "Votre recherche a été enregistrée.", "alert-success");
});

let isResponseBad = function(element) {
    console.log(element);
    return element === null;
};

$('#btn-new-search').click(function() {
    let alertBtn = $('#alert-msg');
    let userInput = $('#input').val();

    if (userInput === '') {
        alertDisplay(alertBtn, "Papybot n'a pas entendu votre question.", "alert-warning");
    } else {
        ajaxPost("/parser", userInput, function(response) {
            response = JSON.parse(response);

            if (Object.values(response).some(isResponseBad) === false) {
                // We delete everything before displaying new search ( == pushing "Effacer" button)
                deleteSearch();
                displayResult(response);
            } else {
                console.log(response);
                alertDisplay(alertBtn, `${response.bot_response}`,
                    "alert-danger");
            }
        })
    }
});
