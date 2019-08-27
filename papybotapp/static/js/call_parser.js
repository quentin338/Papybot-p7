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

let form = document.querySelector("form");

let lastSearch = undefined;

function deleteSearch() {
    $('#title-acc-new-search').text("Nouvelle recherche");
    $('#input').val("");
    $('#wiki-results').text("");
    $('#wiki-link').html("");
    $('#coords').text("");
    initMap();
}

$('#btn-delete-search').click(deleteSearch);

function changeAccNewSearchTitle(newTitle, url) {
    $('#title-acc-new-search').text(`Papybot vous raconte l'histoire du : ${newTitle}.`);

    let wikiSpanElt = $('#wiki-link');
    wikiSpanElt.text("Plus d'infos ");
    wikiSpanElt.append('<a id="wiki-link-a" target="_blank"></a>');

    let wikiAElt = $('#wiki-link-a');
    wikiAElt.text("Ici");
    wikiAElt.attr("href", url)
}

function displayResult(response) {
    changeAccNewSearchTitle(response.address, response.url);
    $('#wiki-results').text(response.content);

    let lat = response.coords[0];
    let lng = response.coords[1];
    $('#coords').text(`${lat} ${lng}`);
    initMap(lat, lng);
}

function alertHide(elt, btnType) {
    if (btnType != undefined) {
        elt.hide("slow", function() {
            elt.toggleClass(btnType);
        });
    } else {
        elt.hide("slow");
    }
}


/* */
function alertDisplay(elt, message, btnType) {
    if (btnType != undefined) {
        btnType = "alert-success " + btnType;
        elt.toggleClass(btnType);
    }

    elt.text(message);
    elt.show("slow", function() {
        setTimeout(function() {
            alertHide(elt, btnType);
        }, 3000);
    });
}

function getSearchInfos() {
    return
}

$('#btn-save-search').click(function() {
    /* TODO: get response: wiki result geocoords research
    */

    alertDisplay($('#alert-msg'), "Votre recherche a été enregistrée.");
});

$('#btn-new-search').click(function() {
    let alertBtn = $('#alert-msg');
    let userInput = $('#input').val();

    if (userInput === '') {
        alertDisplay(alertBtn, "Papybot n'a pas entendu votre question.", "alert-warning");
    } else {
        ajaxPost("/parser", userInput, function(response) {
            if (response !== "") {
                response = JSON.parse(response);
                lastSearch = response;

                displayResult(response);
            } else {
                alertDisplay(alertBtn, "Papybot a un trou de mémoire, veuillez précisez votre recherche.",
                    "alert-danger");
            }
        })
    }
});
