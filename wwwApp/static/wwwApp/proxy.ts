interface Request{
    crew_id : string;
    flight_id : string;
}

let requests: Array<Request> = []

let last_red_buttons: Array<any> = [];

let busy : boolean

function add_request(data: Request) {
    requests.push(data);
}

function synchronize() {
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

function hide_red_buttons() {
    $.each(last_red_buttons, function (index, element) {
        document.getElementById(element["id"]).removeAttribute("style");
    });
}