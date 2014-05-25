$(document).ready(
    function() {
        pesel = $("#auth_user_pesel__row td.w2p_fw").text(); 
        var year = Number(pesel.substr(0,2));
        if (year < 14) {
            year += 2000;
        } else {
            year += 1900;
        }
        var month = Number(pesel.substr(2,2)) - 1;
        var day = Number(pesel.substr(4,2));

        var today = new Date();
        var age = today.getFullYear() - year;
        if (today.getMonth() < month || (today.getMonth() == month && today.getDate() < day)) {age--;}
        $("#auth_user_pesel__row").after('<tr id="wiek"><td class="w2p_fl"><label for="wiek"">Wiek: </label></td><td class="w2p_fw">' + age.toString() + '</td><td class="w2p_fc"></td></tr>')
        console.log(age);
    }
);