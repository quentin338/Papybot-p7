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

let firstMapDisplay = true;

// form.addEventListener("submit", function (e) {
//     e.preventDefault();
//
//     // if (firstMapDisplay === true) {
//     // document.getElementById("map").innerHTML = "";
//     // }
//
//     // Creating FormData and we pass it the input text to send it to the view
//     let form = new FormData();
//     form.append("query", e.target.elements.input.value);
//
//     ajaxPost("/parser/", form, function (response) {
//         response = JSON.parse(response);
//
//         let displayElt = document.getElementById("display-result");
//
//         // We remove the first displayed map as we create one for each result
//         if (firstMapDisplay === true) {
//             let mapElt = document.getElementById("map");
//             mapElt.parentNode.removeChild(mapElt);
//             firstMapDisplay = false;
//         }
//
//         // Creating a div with Papybot's image
//         let papybotDivElt = document.createElement("div");
//         papybotDivElt.id = "papybot-result-img";
//         papybotDivElt.classList.add("papybot-result-img");
//
//         let papybotImgElt = document.createElement("img");
//         papybotImgElt.src = "static/img/papybot300x300.jpg";
//         papybotImgElt.alt = "Papybot";
//
//         papybotDivElt.appendChild(papybotImgElt);
//
//         // Creating a div who'll have 3 <p> elts : content, url and Papybot's answer
//         let resultsElt = document.createElement("div");
//         resultsElt.classList.add("results");
//
//         // Inserting the last search on top
//         displayElt.insertBefore(resultsElt, displayElt.childNodes[0]);
//
//         // Creating div for result text content
//         let textContentDiv = document.createElement("div");
//         textContentDiv.id = "text-content";
//         textContentDiv.classList.add("text-content");
//
//         // Content <p>
//         let contentPElt = document.createElement("p");
//         contentPElt.textContent = response.content;
//         contentPElt.classList.add("wiki-content");
//
//         // Url <p>
//         let urlPElt = document.createElement("p");
//         let aElt = document.createElement("a");
//         aElt.setAttribute("href", response.url);
//         aElt.textContent = "Pour en savoir plus";
//
//         urlPElt.appendChild(aElt);
//
//         // PapyBot's answer <p>
//         let papybotPElt = document.createElement("p");
//         papybotPElt.textContent = "PapyBot : " + response.bot_response;
//
//         // Adding all 3 <p> to the div
//         textContentDiv.appendChild(papybotPElt);
//         textContentDiv.appendChild(contentPElt);
//         textContentDiv.appendChild(urlPElt);
//
//         // Adding the div the result div
//         resultsElt.appendChild(papybotDivElt);
//         resultsElt.append(textContentDiv);
//
//         console.log(response);
//
//         // Creating new Map
//         let newMapElt = document.createElement("div");
//         newMapElt.id = "map";
//         newMapElt.classList.add("map");
//
//         resultsElt.appendChild(newMapElt);
//
//         // Display Google Map
//         initMap(response.coords[0], response.coords[1]);
//
//         // Removing id to be able to keep it while creating other maps
//         newMapElt.removeAttribute("id");
//     })
// });

let lastSearch = undefined;

function deleteSearch() {
    $('#title-acc-new-search').text("Nouvelle recherche");
    $('#input').val("");
    $('#wiki-results').text("");
    $('#wiki-link').html("");
    initMap();
}

$('#btn-delete-search').click(deleteSearch);

// TODO: change HTML to TEXT
function changeAccNewSearchTitle(newTitle, url) {
    $('#title-acc-new-search').html(`Papybot vous raconte l'histoire du : ${newTitle}.`);
    $('#wiki-link').html(`Plus d'infos (<a href="${url}" target="_blank">Ici</a>)`);
}

function displayResult(response) {
    changeAccNewSearchTitle(response.address, response.url);
    $('#wiki-results').text(response.content);
    initMap(response.coords[0], response.coords[1]);
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

$('#btn-save-search').click(function() {
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
