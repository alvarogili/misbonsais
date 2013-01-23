$(document).on("ready", load);

function load(){
	$("#boton_menu").on("click", show_menu); 
}

function show_menu(){
	if($("#menu_chico").css("display") == "none"){
        $('#boton_menu').text('Ocultar'); 
        $("#menu_chico").css("display","block");
	}else{
		$('#boton_menu').text('Menú'); 
        $("#menu_chico").css("display","none");
	}
}