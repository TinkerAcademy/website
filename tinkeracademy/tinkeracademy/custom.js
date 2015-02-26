jQuery(document).ready(function( $ ) { 
		
		//FitVids
		$(".fitvid,iframe").fitVids();
		
		
		//Responsive Menu
		$(".nav").mobileMenu();
		$("<div class='mobile-icon'></div>").insertAfter(".select-menu");
        
        
        //Device Class
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
        
	       $("body").addClass("device");
	
	    }
	    
	    //View Lightbox
	    $(".slides li a").addClass("view");
	    $(".slides li a").attr('rel', 'lightbox')
	    
});