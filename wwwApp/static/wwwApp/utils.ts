function set_crew(selected_crew: any, selected_flight: any) {
    var crew = selected_flight.childNodes[4];
    var captain_name = selected_crew.childNodes[0].innerText;
    var textnode = document.createTextNode(captain_name);
    crew.innerText = captain_name;
}
function unset_crew(selected_flight: any) {
    var crew = selected_flight.childNodes[4];
    crew.innerText = '';
}

function show_alert(type, text, length) {
    alert = document.getElementById("alert");
    alert.setAttribute("class", "alert " + type);
    alert.innerHTML = ''
    alert.appendChild(document.createTextNode(text));

    $("#alert").fadeTo(2000, length).slideUp(length, function () {
        $("#alert").slideUp(length);
        alert.removeChild(alert.lastChild);
    });
}