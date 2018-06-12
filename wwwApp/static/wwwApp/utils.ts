function set_crew(selected_crew: any, selected_flight: any) {
    var crew = selected_flight.childNodes[4];
    var captain_name = selected_crew.childNodes[0].innerText;
    var textnode = document.createTextNode(captain_name);
    if (crew.childElementCount == 1)
        crew.replaceChild(textnode,crew.childNodes[0]);
    else
        crew.appendChild(textnode);


}