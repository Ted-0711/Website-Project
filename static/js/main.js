(function($) {

	"use strict";	

  	$(".main-menu a").click(function(){
		var id =  $(this).attr('class');
		id = id.split('-');
		$('a.active').removeClass('active');
    	$(this).addClass('active');
		$("#menu-container .content").slideUp('slow');
		$("#menu-container #menu-"+id[1]).slideDown('slow');		
		$("#menu-container .homepage").slideUp('slow');
		return false;
	});


	$(".main-menu a.homebutton").click(function(){
		$("#menu-container .content").slideUp('slow');
		$("#menu-container .homepage").slideDown('slow');
		$(".logo-top-margin").animate({marginLeft:'45%'}, "slow");
		$(".logo-top-margin").animate({marginTop:'120px'}, "slow");
		return false;
	});

	$(".main-menu a.aboutbutton").click(function(){
		$("#menu-container .content").slideUp('slow');
		$("#menu-container .about-section").slideDown('slow');
		$(".logo-top-margin").animate({marginTop:'0'}, "slow");
		$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
		return false;
	});

	$(".main-menu a.projectbutton").click(function(){
		$("#menu-container .content").slideUp('slow');
		$("#menu-container .gallery-section-1").slideDown('slow');
		$(".logo-top-margin").animate({marginTop:'0'}, "slow");
		$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
		return false;
	});

	$(".main-menu a.contactbutton").click(function(){
		$("#menu-container .content").fadeOut();
		$("#menu-container .contact-section-1").slideDown('slow');
		$(".logo-top-margin").animate({marginTop:'0'}, "slow");
		$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
		return false;
	});


	// var pages = document.getElementById('pages');
	// var i;
	// var array = new Array(parseInt(pages.dataset.lost_pages));
	//
	// for (i = 1; i <= parseInt(pages.dataset.lost_pages); i++){
	// 	array[i - 1] = "#menu-container .gallery-section-" + i;
	// }

	// for (var i = 1; i <= parseInt(pages.dataset.lost_pages); i++) {
	// 	var page_menu_str = ".page-menu-lost a.page-" + i;
	// 	var gallery_section_str = "#menu-container .gallery-section-" + i;
	// 	var temp = new String(gallery_section_str);
	// 	$(page_menu_str).click(function(){
	// 		$("#menu-container .content").slideUp('slow');
	// 		console.log(temp);
	// 		$(temp).slideDown('slow');
	// 		$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 		$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 		return false;
	// 	});
	// }

	for (var i = 1; i <= parseInt(pages.dataset.lost_pages); i++) {
		var page_menu_str = ".page-menu-lost a.page-" + i;
		var gallery_section_str = "#menu-container .gallery-section-" + i;
		eval('$(page_menu_str).click(function(){\
			$("#menu-container .content").slideUp("slow");\
			$("' + gallery_section_str + '").slideDown("slow");\
			$(".logo-top-margin").animate({marginTop:"0"}, "slow");\
			$(".logo-top-margin").animate({marginLeft:"0"}, "slow");\
			return false;\
		});');
	}	// 与下方等价

	// $(".page-menu-lost a.page-1").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-1").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });
	//
	// $(".page-menu-lost a.page-2").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-2").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });
	//
	// $(".page-menu-lost a.page-3").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-3").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });
	//
	// $(".page-menu-lost a.page-4").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-4").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });
	//
	// $(".page-menu-lost a.page-5").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-5").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });
	//
	// $(".page-menu-lost a.page-6").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-6").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });
	//
	// $(".page-menu-lost a.page-7").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-7").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });
	//
	// $(".page-menu-lost a.page-8").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-8").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });
	//
	// $(".page-menu-lost a.page-9").click(function(){
	// 	$("#menu-container .content").slideUp('slow');
	// 	$("#menu-container .gallery-section-3").slideDown('slow');
	// 	$(".logo-top-margin").animate({marginTop:'0'}, "slow");
	// 	$(".logo-top-margin").animate({marginLeft:'0'}, "slow");
	// 	return false;
	// });

	for (var i = 1; i <= parseInt(pages.dataset.pick_pages); i++) {
		var page_menu_str = ".page-menu-found a.page-" + i;
		var contact_section_str = "#menu-container .contact-section-" + i;
		eval('$(page_menu_str).click(function(){\
			$("#menu-container .content").slideUp("slow");\
			$("' + contact_section_str + '").slideDown("slow");\
			$(".logo-top-margin").animate({marginTop:"0"}, "slow");\
			$(".logo-top-margin").animate({marginLeft:"0"}, "slow");\
			return false;\
		});');
	}

	$('.toggle-menu').click(function(){
        $('.show-menu').stop(true,true).slideToggle();
        return false;
    });

    $('.show-menu a').click(function() {
    	$('.show-menu').fadeOut('slow');
    });


})(jQuery);