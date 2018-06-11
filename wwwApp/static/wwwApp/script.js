var selected_flight = undefined, selected_crew = undefined, date = undefined;

function add_relation() {
    selected_flight.removeAttribute("style");
    selected_crew.removeAttribute("style");
    document.getElementById("add_relation").setAttribute("disabled", "");
    $.ajax({
        type: 'GET',
        url: '/add_relation_service/',
        dataType: 'json',
        data: {
            crew_id: selected_crew.getAttribute("id"),
            flight_id: selected_flight.getAttribute("id")
        },
        success: function (data) {
            alert = document.getElementById("alert");
            alert.setAttribute("class", "alert " + data.alert_class);
            alert.innerHTML = ''
            alert.appendChild(document.createTextNode(data.alert));
            fetchFlights();
            $("#alert").fadeTo(2000, 500).slideUp(500, function () {
                $("#alert").slideUp(500);
                alert.removeChild(alert.lastChild);
            });
        }
    });
    selected_flight = undefined;
    selected_crew = undefined;

}

function remove_crew() {
    selected_flight.removeAttribute("style");
    document.getElementById("remove_crew").setAttribute("disabled", "");
    $.ajax({
        type: 'GET',
        url: '/remove_relation_service/',
        dataType: 'json',
        data: {
            flight_id: selected_flight.getAttribute("id")
        },
        success: function () {
            fetchFlights();
        }
    });
}

function check_if_relation_is_selected() {
    if (selected_flight != undefined) {
        document.getElementById("remove_crew").removeAttribute("disabled");
    }
    if (selected_flight != undefined && selected_crew != undefined) {
        document.getElementById("add_relation").removeAttribute("disabled");
    } else {
        document.getElementById("add_relation").setAttribute("disabled","true")
    }
}

function select_flight(node) {
    if (selected_flight == node) {
        selected_flight.removeAttribute("style");
        selected_flight = undefined;
        check_if_relation_is_selected();
        return;
    }
    if (selected_flight != undefined) {
        selected_flight.removeAttribute("style");
    }
    selected_flight = node;
    node.style.backgroundColor = "darkgrey";
    check_if_relation_is_selected();
}
// function select_item(node,selected_row) {
//
// }

function select_crew(node) {
    if (selected_crew == node) {
        selected_crew.removeAttribute("style");
        selected_crew = undefined;
        check_if_relation_is_selected();
        return;
    }
    if (selected_crew != undefined) {
        selected_crew.removeAttribute("style");
    }
    selected_crew = node;
    node.style.backgroundColor = "darkgrey";
    check_if_relation_is_selected();
}

function fetchFlights() {
    var config = {
        type: 'GET',
        url: '/flights_service/',
        dataType: 'json',
        success: function (data) {
            var flight_table_body = document.getElementById("flight_table_body");
            flight_table_body.innerHTML = '';
            $.each(data, function (index, element) {
                var node = jQuery.parseHTML(
                    "<tr id=\"flight\" class=\"clickable-row\" onclick=\"select_flight(this)\">" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "<td></td>" +
                    "</tr>"
                );
                var properties = ["starting_airport_name", "starting_time_formatted", "destination_airport_name",
                    "destination_time_formatted", "crew_name"];
                for (var i = 0; i < properties.length; i++) {
                    node[0].childNodes[i].appendChild(document.createTextNode(element[properties[i]]));
                }
                node[0].setAttribute("id", element.id);
                flight_table_body.appendChild(node[0]);
            });
        }
    };
    if (date != undefined)
        config.data= {date:date};
    $.ajax(config);
}

$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/crews_service/',
        dataType: 'json',
        success: function (data) {
            $.each(data, function (index, element) {
                var node = jQuery.parseHTML(
                    "<tr id=\"crew\" class=\"clickable-row\" onclick=\"select_crew(this)\">" +
                    "<td></td>" +
                    "</tr>"
                );
                var captain = document.createTextNode(element.captain_name + " " + element.captain_surname);
                node[0].firstChild.appendChild(captain);
                node[0].setAttribute("id", element.id);
                document.getElementById("crew_table_body").appendChild(node[0]);
            });
        }
    });
    $(function () {
        $("#datepicker").datepicker({
            onSelect: function (dateText) {
                date = dateText
                fetchFlights()
            },
            dateFormat: "yy-mm-dd"
        });
    });
});
