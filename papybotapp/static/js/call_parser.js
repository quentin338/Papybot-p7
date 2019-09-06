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

// Official GoogleMaps init
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

    // Add/remove display: none, based on undefined coords or not
    let mapHide = $('#map');
    if (needToDisplayMap === false) {
        mapHide.toggleClass("d-none", true);
    } else {
        mapHide.toggleClass("d-none", false);
    }
  }

// Delete metadata to avoid registering 1 research twice
// We can save the same card if the same search has been done twice obv
function deleteMetaData(element) {
    element.removeAttr('data-format-address');
    element.removeAttr('data-wiki-url');
    element.removeAttr('data-wiki-thumbnail');
    element.removeAttr('data-coords');
}

// "Effacer" (delete) button
function deleteSearch() {
    $('#input').val("");
    $('#wiki-results').text("");

    // Delete data and hide the div
    let resultsElt = $('#results');
    deleteMetaData(resultsElt);
    resultsElt.toggleClass("d-none", true);

    // Reset the map with no coords
    initMap();
}

$('#btn-delete-search').click(deleteSearch);

// Display results when the response to wiki AND GoogleMaps are good
function displayResult(response) {
    let lat = response.coords[0];
    let lng = response.coords[1];

    $('#wiki-results').text(response.content);

    // Saving data that will be displayed on the card if we save
    let results = $('#results');
    results.attr("data-format-address", response.address);
    results.attr("data-wiki-url", response.url);
    results.attr("data-wiki-thumbnail", response.thumbnail);
    results.attr("data-coords", `${lat} ${lng}`);
    results.toggleClass("d-none", false);

    // Displaying the map
    initMap(lat, lng);
}

// Custom display of an alert with "slow" show/hide effect
function alertDisplay(elt, message, btnType, displayTime) {
    if (displayTime === undefined) {
        displayTime = 3000;
    }

    elt.toggleClass(btnType, true);
    elt.text(message);
    elt.show("slow", function() {
        setTimeout(function() {
            alertHide(elt, btnType);
        }, displayTime);
    });
}

function alertHide(elt, btnType) {
        elt.hide("slow", function() {
            elt.toggleClass(btnType, false)
        });
}

// Custom card creation
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
    cardTitleElt.innerText = `Votre recherche : ${formatAddress}`;

    cardTextElt.classList.add("card-text");
    cardTextElt.innerText = wikiContent;

    cardWikiLinkElt.classList.add("btn", "btn-primary", "wiki-saved-link");
    cardWikiLinkElt.href = wikiUrl;
    cardWikiLinkElt.setAttribute("target", "_blank");
    cardWikiLinkElt.text = "Article Wikipédia";

    cardMapsLinkElt.classList.add("btn", "btn-primary", "google-maps-search");
    cardMapsLinkElt.href = `https://www.google.com/maps/search/?api=1&query=${formatAddress}`;
    cardWikiLinkElt.setAttribute("target", "_blank");
    cardMapsLinkElt.text = "Lien GoogleMaps";

    // Inserting the card at the top of the other cards if any
    let allCardsElt = $('#all-cards');
    allCardsElt.prepend(mainElt);
}

// "Enregistrer" (save) button
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

    // No metadata means that one card has already been done with this search
    if (resultsData.attr('data-format-address') === undefined) {
        alertDisplay(alertElt, "Vous avez déjà enregistré cette recherche.", "alert-warning");
        return
    }

    let formatAddress = resultsData.attr("data-format-address");
    let wikiUrl = resultsData.attr("data-wiki-url");
    let wikiThumbnail = resultsData.attr("data-wiki-thumbnail");

    // Creation of the card
    createCard(formatAddress, wikiContent, wikiUrl, wikiThumbnail);

    // We delete the meta-data to not be able to make the same card twice on one search
    deleteMetaData(resultsData);

    alertDisplay(alertElt, "Votre recherche a été enregistrée.", "alert-success");
});

// Function to check if any element of an Array is null
let isResponseBad = function(element) {
    return element === null;
};

// "Raconte-moi Papybot !" (search) button
$('#btn-new-search').click(function() {
    let bodyElt = $('body');
    let alertBtn = $('#alert-msg');
    let userInput = $('#input').val();
    bodyElt.css('cursor', 'wait');

    if (userInput === '') {
        alertDisplay(alertBtn, "Papybot n'a pas entendu votre question.", "alert-warning");
        bodyElt.css('cursor', 'default')
    } else {
        ajaxPost("/parser", userInput, function(response) {
            response = JSON.parse(response);
            bodyElt.css('cursor', 'default');

            // If all values in the response are good, we can display it to the user
            if (Object.values(response).some(isResponseBad) === false) {
                // We delete everything before displaying new search ( == pushing "Effacer" button)
                deleteSearch();

                // Papybot conversation
                alertDisplay(alertBtn, `PAPYBOT : ${response.bot_response}`, "alert-success", 8000);

                // Displaying result in #results
                displayResult(response);
            } else {
                // No results from either Wiki or GoogleMaps
                alertDisplay(alertBtn, `PAPYBOT : ${response.bot_response}`,
                    "alert-danger", 5000);
            }
        })
    }
});
