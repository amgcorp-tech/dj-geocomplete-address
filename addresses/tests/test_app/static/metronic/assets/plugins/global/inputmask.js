"use strict";

var KTFormsInputmaskDemos={

    init:function(a){
        Inputmask({
            mask:"99/99",
            placeholder: "MM/YY",
            regex: "0[1-9]|1[0-2])\\/?([0-9]{2}"
        }).mask("#id_card_expiry, #id_expiration");

        Inputmask({
            mask:"9999 9999 9999 9999",
            placeholder: "XXXX XXXX XXXX XXXX"
        }).mask("#id_card_number, #id_number");

        Inputmask({
            mask:"99/99/9999",
            placeholder: "MM/DD/YYYY",
        }).mask("#id_dob, #id_patient-dob, #id_subscriber_dob, #id_insurance-subscriber_dob");

        Inputmask({
            mask:"999-99-9999",
            placeholder: "XXX-XX-XXXX"
        }).mask("#id_ssn, #id_insurance-ssn");

    }
};

KTUtil.onDOMContentLoaded((
    function(){
        KTFormsInputmaskDemos.init();
    }
));