// import * as $ from "jquery";
import {create_alert,remove_alert, show_alert} from "./utils";
import {fetchFlights} from "./fetch_flight";

interface Request{
    crew_id : string;
    flight_id : string;
}

let requests: Array<Request> = []

let last_red_buttons: Array<any> = [];

let busy : boolean

export function add_request(data: Request) {
    requests.push(data);
}

export function synchronize() {
    if (!check_if_not_busy())
        return;
    busy = true;
    let id_alert = create_alert('alert-warning','Synchronizuje. Wszystkie operacje są zabronione');
    hide_red_buttons()
    $.ajax({
        type: 'GET',
        url: '/synchronize_service/',
        dataType: 'json',
        data: {requests: requests},
            success: function (data) {
                if (data.length > 0) {
                    show_alert('alert-danger', 'Synchronizacja nie powidła się. ' +
                        'Przyczyną mogą być zmiany w danych na serwerze i/lub próba przypisania załogi do 2 różnych lotów odbywających się w tym samym czasie. ' +
                        'Zaznaczono loty powodujące problem.',10000);

                    $.each(data, function (index, element) {
                        document.getElementById(element["id"]).style.backgroundColor = 'red';
                    });
                    last_red_buttons = data.slice();
                } else {
                    show_alert('alert-success','Synchronizaja przeprowadzona pomyślnie!',2000);
                    fetchFlights();
                }
                remove_alert(id_alert);
                busy = false;
            }

        });
}
window.synchronize = synchronize;

export function hide_red_buttons() {
    $.each(last_red_buttons, function (index, element) {
        document.getElementById(element["id"]).removeAttribute("style");
    });
}

export function check_if_not_busy() {
    if (busy) {
        show_alert("alert-warning","Aktualnie wykonywana jest synchronizacja, spróbuj później",2000)
        return false
    }
    return true;
}