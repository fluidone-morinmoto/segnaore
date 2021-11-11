function activateDateTimePicker(selector) {
    jQuery.datetimepicker.setLocale('it');

    jQuery(selector).datetimepicker({
        i18n:{
            if:{
                months:[
                    'Gennaio','Febbraio','Marco','Aprile', 'Maggio',
                    'Giugno','Luglio','Agosto', 'Settembre', 'Ottobre',
                    'Novembre','Dicembre',
                ],
                dayOfWeek:[
                    "Lun", "Mar", "Mer", "Gio",
                    "Ven", "Sab", "Dom",
                ]
            }
        },
        timepicker: true,
        format:'d/m/Y H:i',
        useSeconds: false,
        step: 15
    });
}
