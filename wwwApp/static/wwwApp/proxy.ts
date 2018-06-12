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

function add_relation_proxy(ajax: AddRelationRequest) {
    $.ajax(ajax)
}