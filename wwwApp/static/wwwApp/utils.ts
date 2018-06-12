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

    $("#alert").show(); // use slide down for animation
      setTimeout(function () {
          if (alert.innerText == text) {
              $("#alert").slideUp(500);
              alert.removeChild(alert.lastChild);
          }
      }, length);
}

function check_if_not_busy() {
    if (busy) {
        show_alert("alert-warning","Aktualnie wykonywana jest synchronizacja, spróbuj później",2000)
        return false
    }
    return true;
}