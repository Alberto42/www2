interface Request{
    crew_id : string;
    flight_id : string;
}


var requests: Array<Request> = []

function add_request(data: Request) {
    requests.push(data);
}


function synchronize() {
    $.ajax({
        type: 'GET',
        url: '/synchronize_service/',
        dataType: 'json',
        data: {requests: requests},
        success: function (data) {
            if (data.length > 0) {
                show_alert('alert-danger', 'Synchronizacja nie powidła się. ' +
                    'Przyczyną mogą być zmiany w danych na serwerze i/lub próba przypisania załogi do 2 różnych lotów odbywających się w tym samym czasie. ' +
                    'Zaznaczono loty powodujące problem.',2000);

                $.each(data, function (index, element) {
                    document.getElementById(element["id"]).style.backgroundColor = 'red';
                });
            } else {
                show_alert('alert-success','Synchronizaja przeprowadzona pomyślnie!',700);
            }
        }

        }
    });
}