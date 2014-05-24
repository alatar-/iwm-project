$(document).ready(function(){
	select = $("select:last")
	i = 0;
	prefix = "next_drug_"
	select.after($("<input type=\"button\" class=\""+prefix+i+"\" value=\"next\">"));
	++i;
	$("button").on("click", function() {
		$("<input type=\"button\" class=\""+prefix+(i-1)+"\" value=\"next\">").after("hola");
		$("<input type=\"button\" class=\""+prefix+(i-1)+"\" value=\"next\">").after("<input type=\"button\" class=\""+prefix+i+"\" value=\"next\">");
		++i;
	});
	//.attr({"multiple":"multiple", "class":"multiselect"});
	//$(function(){
	//	$(".multiselect").multiselect();
	//});
});