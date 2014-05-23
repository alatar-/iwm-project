$(document).ready(
	function() {
		idArray = ["first_name", "last_name", "email", "password", "pesel", "address", "city", "zip", "gender", "born_city", "identity_id", "nip", "phone_number", "nn_patient" ];
		var prefix = "auth_user_";

		$("#"+prefix+"first_name").attr({"data-parsley-pattern":"^[A-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ][a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ ]*$", "data-parsley-required":"true", "data-parsley-group":"patient"});
		$("#"+prefix+"first_name").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"last_name").attr({"data-parsley-pattern":"^[A-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ][a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ ]*$", "data-parsley-required":"true", "data-parsley-group":"patient"});
		$("#"+prefix+"last_name").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"email").attr({"data-parsley-type":"email", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"email").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"password").attr({"data-parsley-required":"true", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"password").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"pesel").attr({"data-parsley-pattern":"^[0-9]{11}$", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"pesel").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"address").attr({"data-parsley-type":"alphanum", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"address").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"city").attr({"data-parsley-pattern":"^[A-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ][a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ ]*$", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"city").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"zip").attr({"data-parsley-presence":"true", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"zip").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"gender").attr({"data-parsley-pattern":"^(mężczyzna|kobieta|nieznana|nie dotyczy)$", "data-parsley-required":"true","data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"gender").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"born_city").attr({"data-parsley-presence":"true","data-parsley-required":"true", "data-parsley-group":"patient"});
		$("#"+prefix+"born_city").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"identity_id").attr({"data-parsley-length":"[9,9]", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"identity_id").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"nip").attr({"data-parsley-pattern":"^([0-9](-)?){9}[0-9]$", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"nip").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"phone_number").attr({"data-parsley-pattern":"^(([+]|[0]{2})[0-9]{2})?[0-9]{9}$", "data-parsley-required":"true","data-parsley-group":"patient"});
		$("#"+prefix+"phone_number").after("<ul class=\"parsley-errors-list\"></ul>");

		$("#"+prefix+"nn_patient").before("<p>");
		$("#"+prefix+"nn_patient").attr({"data-parsley-mincheck":"1", "data-parsley-group":"nn_patient"});
		$("#"+prefix+"nn_patient").after("<ul class=\"parsley-errors-list\"></ul>");
		$("#"+prefix+"nn_patient").after("<p>");
		$("form").parsley({trigger: "click focus mousedown focusin focusout change keyup"});
		checked = 0;
		$("form").parsley().subscribe('parsley:form:validate', function (formInstance) {
		    // if one of these blocks is not failing do not prevent submission
		    // we use here group validation with option force (validate even non required fields)
		    if (formInstance.isValid("patient", true) || formInstance.isValid("nn_patient", true))
			    return;
		    // else stop form submission
		    else if(!checked) {
		    	checked = 1;
		    	formInstance.submitEvent.preventDefault();
		    	alert("Niektóre pola wydają się być wypełnione niepoprawnie. Upewnij się, że wprowadzasz poprawnie swoje dane. Jeśli na pewno chcesz zatwierdzić dane, które podałeś, ponownie zatwierdź wysłanie formularza.");
			    $('.invalid-form-error-message')
			    .html("You must correctly fill at least one of these 2 blocks' fields!")
		    	.addClass("filled");
				return;
			} else {
		    	formInstance.submitEvent();
				return;
			}
		 });
	}
);