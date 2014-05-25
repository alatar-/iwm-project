$(document).ready(
    function() {
        $("#"+prefix+"nn_patient").before("<p>");
        $("#"+prefix+"nn_patient").attr({"data-parsley-check":"[1,1]", "data-parsley-group":"nn_patient"});
        $("#"+prefix+"nn_patient").after("<ul class=\"parsley-errors-list\"></ul>");
        $("#"+prefix+"nn_patient").after("<p>");
        $("form").parsley({trigger: "click focus mousedown focusin focusout change keyup"});
        checked = 0;
        $("form").parsley().subscribe('parsley:form:validate', function (formInstance) {
            // if one of these blocks is not failing do not prevent submission
            // we use here group validation with option force (validate even non required fields)
            if (formInstance.isValid("patient", true, checked) || formInstance.isValid("nn_patient", true, checked)) {
                $("form").parsley().destroy();
                $("form").submit();
                return true;
            }
                
            // else stop form submission
            else if(checked == 0) {
                checked = 1;
                formInstance.submitEvent.preventDefault();
                alert("Niektóre pola wydają się być wypełnione niepoprawnie. Upewnij się, że wprowadzasz poprawnie swoje dane. Jeśli na pewno chcesz zatwierdzić dane, które podałeś, ponownie zatwierdź wysłanie formularza.");
                $('.invalid-form-error-message')
                .html("You must correctly fill at least one of these 2 blocks' fields!")
                .addClass("filled");
                return false;
            }
            if(checked == 1) {
                $("form").parsley().destroy();
                $("form").submit();
            }

         });
    }
);