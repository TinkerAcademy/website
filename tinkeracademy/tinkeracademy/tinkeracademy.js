function istouchdevice() {
	return typeof window.ontouchstart !== 'undefined';
}
jQuery(document).ready(function( $ ) { 
	if (istouchdevice()) {					
		$(".mobile").addClass("curl");
	}
});	
