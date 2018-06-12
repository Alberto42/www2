interface AddRelationRequestData{
    crew_id : string;
    flight_id : string;
}

interface AddRelationRequest{
    type: string;
    url: string;
    dataType: string;
    data : AddRelationRequestData;
    success : any
}

var requests: Array<AddRelationRequest> = []

function add_relation_proxy(ajax: AddRelationRequest) {
    let found: boolean = false;
    requests.forEach( (request) => {
        if (request.data.flight_id == ajax.data.flight_id) {
            found = true;
            request.data.flight_id = ajax.data.flight_id;
        }
    })
    if (found == false )
        requests.push(ajax);
    ajax.success();
}


function synchronize() {
    requests.forEach((request) => {
        $.ajax(request)
    })
    requests = [];
}