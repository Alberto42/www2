"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var $ = require("jquery");
var proxy_1 = require("./proxy");
var utils_1 = require("./utils");
var fetch_flight_1 = require("./fetch_flight");
var selected_flight = undefined, selected_crew = undefined;
function add_relation() {
    if (!proxy_1.check_if_not_busy())
        return;
    proxy_1.hide_red_buttons();
    selected_flight.removeAttribute("style");
    selected_crew.removeAttribute("style");
    proxy_1.add_request({
        crew_id: selected_crew.getAttribute("id"),
        flight_id: selected_flight.getAttribute("id")
    });
    utils_1.set_crew(selected_crew, selected_flight);
    utils_1.show_alert("alert-info", "Dodano lokalnie załogę do lotu. Kliknij \"synchronizuj\" aby zsynchronizować zmiany z serwerem.", 2000);
    selected_flight = undefined;
    selected_crew = undefined;
    change_buttons_status();
}
function remove_crew() {
    if (!proxy_1.check_if_not_busy())
        return;
    proxy_1.hide_red_buttons();
    selected_flight.removeAttribute("style");
    document.getElementById("remove_crew").setAttribute("disabled", "");
    proxy_1.add_request({
        crew_id: "remove",
        flight_id: selected_flight.getAttribute("id")
    });
    utils_1.show_alert("alert-info", "Usunięto lokalnie przypisanie załogi do lotu. Kliknij \"synchronizuj\" aby zsynchronizować zmiany z serwerem.", 2000);
    utils_1.unset_crew(selected_flight);
    selected_flight = undefined;
    change_buttons_status();
}
function change_buttons_status() {
    if (selected_flight != undefined) {
        document.getElementById("remove_crew").removeAttribute("disabled");
    }
    else {
        document.getElementById("remove_crew").setAttribute("disabled", "true");
    }
    if (selected_flight != undefined && selected_crew != undefined) {
        document.getElementById("add_relation").removeAttribute("disabled");
    }
    else {
        document.getElementById("add_relation").setAttribute("disabled", "true");
    }
}
function select_flight(node) {
    if (selected_flight == node) {
        selected_flight.removeAttribute("style");
        selected_flight = undefined;
        change_buttons_status();
        return;
    }
    if (selected_flight != undefined) {
        selected_flight.removeAttribute("style");
    }
    selected_flight = node;
    node.style.backgroundColor = "darkgrey";
    change_buttons_status();
}
function select_crew(node) {
    if (selected_crew == node) {
        selected_crew.removeAttribute("style");
        selected_crew = undefined;
        change_buttons_status();
        return;
    }
    if (selected_crew != undefined) {
        selected_crew.removeAttribute("style");
    }
    selected_crew = node;
    node.style.backgroundColor = "darkgrey";
    change_buttons_status();
}
$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/crews_service/',
        dataType: 'json',
        success: function (data) {
            $.each(data, function (index, element) {
                var node = $.parseHTML("<tr id=\"crew\" class=\"clickable-row\" onclick=\"select_crew(this)\">" +
                    "<td></td>" +
                    "</tr>");
                var captain = document.createTextNode(element.captain_name + " " + element.captain_surname);
                node[0].firstChild.appendChild(captain);
                node[0].setAttribute("id", element.id);
                document.getElementById("crew_table_body").appendChild(node[0]);
            });
        }
    });
    $(function () {
        var $j = jQuery.noConflict();
        var datapicker = $j("#datepicker");
        datapicker.datepicker({
            onSelect: function (dateText) {
                fetch_flight_1.setDate(dateText);
                fetch_flight_1.fetchFlights();
            },
            dateFormat: "yy-mm-dd"
        });
    });
});
