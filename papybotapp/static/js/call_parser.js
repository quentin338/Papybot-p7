function ajaxPost(url, data, callback) {
    var req = new XMLHttpRequest();
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


let form = document.querySelector("form");

form.addEventListener("submit", function (e) {
    e.preventDefault();

    let form = new FormData();
    form.append("query", e.target.elements.input.value);

    ajaxPost("/parser/", form, function (response) {
        response = JSON.parse(response);

        document.getElementById("results").textContent = response.content;

        let aElt = document.createElement("a");
        aElt.setAttribute("href" ,response.url);
        aElt.textContent = response.url;

        let urlElt = document.getElementById("url");
        urlElt.innerHTML = "";
        urlElt.appendChild(aElt);

        console.log(response);
    })
});
