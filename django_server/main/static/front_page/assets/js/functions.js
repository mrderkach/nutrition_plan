
/* Background Images
-------------------------------------------------------------------*/
var  pageTopImage = jQuery('#page-top').data('background-image');
var  aboutImage = jQuery('#login').data('background-image');
var  subscribeImage = jQuery('#about').data('background-image');
var  contactImage = jQuery('#contact').data('background-image');

if (pageTopImage) {  jQuery('#page-top').css({ 'background-image':'url(' + pageTopImage + ')' }); };
if (aboutImage) {  jQuery('#login').css({ 'background-image':'url(' + aboutImage + ')' }); };
if (subscribeImage) {  jQuery('#about').css({ 'background-image':'url(' + subscribeImage + ')' }); };
if (contactImage) {  jQuery('#contact').css({ 'background-image':'url(' + contactImage + ')' }); };

/* Background Images End
-------------------------------------------------------------------*/



/* Document Ready function
-------------------------------------------------------------------*/
jQuery(document).ready(function($) {
	"use strict";


    /* Window Height Resize
    -------------------------------------------------------------------*/
    var windowheight = jQuery(window).height();
    if(windowheight > 650)
    {
         $('.pattern').removeClass('height-resize');
    }
    /* Window Height Resize End
    -------------------------------------------------------------------*/


    
	/* Main Menu   
	-------------------------------------------------------------------*/
	$('#main-menu #headernavigation').onePageNav({
		currentClass: 'active',
		changeHash: false,
		scrollSpeed: 750,
		scrollThreshold: 0.5,
		scrollOffset: 0,
		filter: '',
		easing: 'swing'
	});  

	/* Main Menu End  
	-------------------------------------------------------------------*/




	/* Time Countdown 
	-------------------------------------------------------------------*/
	$('#time_countdown').countDown({
        
         targetDate: {
             'day': 25,
             'month': 12,
             'year': 2017,
             'hour': 0,
             'min': 0,
             'sec': 0
         },
        omitWeeks: true

        // targetOffset: {
        //    'day':      0,
        //    'month':    0,
        //    'year':     1,
        //    'hour':     0,
        //    'min':      0,
        //    'sec':      3
		//},
		//omitWeeks: true

	    });



	/* Next Section   
	-------------------------------------------------------------------*/
	$('.next-section .go-to-login').click(function() {
    	$('html,body').animate({scrollTop:$('#login').offset().top}, 1000);
  	});
  	$('.next-section .go-to-subscribe').click(function() {
    	$('html,body').animate({scrollTop:$('#subscribe').offset().top}, 1000);
  	});
  	$('.next-section .go-to-contact').click(function() {
    	$('html,body').animate({scrollTop:$('#contact').offset().top}, 1000);
  	});
  	$('.next-section .go-to-page-top').click(function() {
    	$('html,body').animate({scrollTop:$('#page-top').offset().top}, 1000);
  	});

  	/* Next Section End
	-------------------------------------------------------------------*/



	/* Login Section   
	-------------------------------------------------------------------*/

  $('#login-submit').click(function(e){ 

    //Stop form submission & check the validation
    e.preventDefault();


    $('.login-error').hide();

    // Variable declaration
    var error = false;
    var k_username = $('#login-username').val();
    var k_password = $('#login-password').val();
    var path = $('#login-form').attr("action");
    var error_messages = [];
    // Form field validation
    if(k_username.length == 0){
      var error = true; 
      error_messages.push('Username is required. ');
    }  

    if(k_password.length == 0){
        var error = true;
        error_messages.push('Password is required.');
    }  

    if (error == true) {
        $('.login-error').html('<i class="fa fa-exclamation"></i> ' + error_messages.join(" \n")).fadeIn();

    // If there is no validation error, next to process the mail function
    } else if (error == false){

        //$('#login-submit').hide();
        $('.login-error-field').fadeOut();

    var data = {
        username: k_username,
        password: k_password
    };

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", path, true);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

    xhttp.responseType = 'text';
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) { 
            //document.getElementById("debug").innerHTML = xhttp.responseText;
            if ('true ' == xhttp.responseText.split("|")[0]) {
                //document.getElementById("debug").innerHTML = "HERE";
                console.log(window.location);
                var new_href = window.location.href.split("/");
                var k = new_href.indexOf("index");
                new_href = new_href.slice(0, k);
                new_href = new_href.join("/");
                window.location.assign(new_href);
           } else {
                //document.getElementById("debug").innerHTML = "THERE";
                error = xhttp.responseText.split("|")[1];
                $('.login-error').html('<i class="fa fa-exclamation contact-error"></i> ' + error).fadeIn();
            }
        }
    };

    xhttp.send(JSON.stringify(data));

    }
  });  

  $('#registration-submit').click(function(e){ 

    //Stop form submission & check the validation
    e.preventDefault();


    $('.registration-error').hide();

    // Variable declaration
    var error = false;
    var k_username = $('#registration-username').val();
    var k_password = $('#registration-password').val();
    var k_first_name = $('#registration-firstname').val();
    var k_last_name = $('#registration-lastname').val();
    var k_email = $('#registration-email').val(); 
    var path = $('#registration-form').attr("action");
    var error_messages = [];
    // Form field validation
    if(k_username.length == 0){
      var error = true; 
      error_messages.push('Username is required.');
    }  

    if(k_password.length == 0){
        var error = true;
        error_messages.push('Password is required.');
    }  
    if(k_first_name.length == 0){
        var error = true; 
        error_messages.push('First name is required.');
    }  
    if(k_last_name.length == 0){
        var error = true;
        error_messages.push('Last name is required.');
    }  
    if(k_email.length != 0 && validateEmail(k_email)){
    } else {
        var error = true; 
        error_messages.push('Please enter a valid email address.');
    }


    if (error == true) {
        $('.registration-error').html('<i class="fa fa-exclamation"></i> ' + error_messages.join(" \n")).fadeIn();

    // If there is no validation error, next to process the mail function
    } else if (error == false){

        //$('#login-submit').hide();
        $('.registration-error-field').fadeOut();

    var data = {
        username: k_username,
        password: k_password,
        first_name: k_first_name,
        last_name: k_last_name,
        email: k_email,
    };

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", path, true);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

    xhttp.responseType = 'text';
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) { 
            //document.getElementById("debug").innerHTML = xhttp.responseText;
            if ('true ' == xhttp.responseText.split("|")[0]) {
                //document.getElementById("debug").innerHTML = "HERE";
                console.log(window.location);
                var new_href = window.location.href.split("/");
                var k = new_href.indexOf("index");
                new_href = new_href.slice(0, k);
                new_href = new_href.join("/");
                window.location.assign(new_href);
           } else {
                //document.getElementById("debug").innerHTML = "THERE";
                error = xhttp.responseText.split("|")[1];
                $('.registration-error').html('<i class="fa fa-exclamation contact-error"></i> ' + error).fadeIn();
            }
        }
    };

    xhttp.send(JSON.stringify(data));

    }
  });  

    /* Login Section End
	-------------------------------------------------------------------*/



  /* Subscribe
  -------------------------------------------------------------------*/
    $(".news-letter").ajaxChimp({
        callback: mailchimpResponse,
        url: "" // Replace your mailchimp post url inside double quote "".  
    });

    function mailchimpResponse(resp) {
         if(resp.result === 'success') {
         
            $('.alert-success').html(resp.msg).fadeIn().delay(3000).fadeOut();
            
        } else if(resp.result === 'error') {
            $('.alert-warning').html(resp.msg).fadeIn().delay(3000).fadeOut();
        }  
    };




	/* Subscribe End
	-------------------------------------------------------------------*/




	/* Contact
	-------------------------------------------------------------------*/
    // Email from Validation
  $('#contact-submit').click(function(e){ 

    //Stop form submission & check the validation
    e.preventDefault();


    $('.first-name-error, .last-name-error, .contact-email-error, .contact-subject-error, .contact-message-error').hide();

    // Variable declaration
    var error = false;
    var k_first_name = $('#first_name').val();
    var k_last_name = $('#last_name').val();
    var k_email = $('#contact_email').val(); 
    var k_subject = $('#subject').val(); 
    var k_message = $('#message').val();
    var path = $('#contact-form').attr("action");

    // Form field validation
    if(k_first_name.length == 0){
      var error = true; 
      $('.first-name-error').html('<i class="fa fa-exclamation"></i> First name is required.').fadeIn();
    }  

    if(k_last_name.length == 0){
      var error = true;
      $('.last-name-error').html('<i class="fa fa-exclamation"></i> Last name is required.').fadeIn();
    }  

    if(k_email.length != 0 && validateEmail(k_email)){
       
    } else {
      var error = true; 
      $('.contact-email-error').html('<i class="fa fa-exclamation"></i> Please enter a valid email address.').fadeIn();
    }

    if(k_subject.length == 0){
      var error = true;
     $('.contact-subject-error').html('<i class="fa fa-exclamation"></i> Subject is required.').fadeIn();
    } 

    if(k_message.length == 0){
      var error = true;
      $('.contact-message-error').html('<i class="fa fa-exclamation"></i> Please provide a message.').fadeIn();
    }  

    // If there is no validation error, next to process the mail function
    if(error == false){

        $('#contact-submit').hide();
        $('#contact-loading').fadeIn();
        $('.contact-error-field').fadeOut();


      // Disable submit button just after the form processed 1st time successfully.
      $('#contact-submit').attr({'disabled' : 'true', 'value' : 'Sending' });

    var data = {
        first_name: k_first_name,
        last_name: k_last_name,
        contact_email: k_email, 
        subject: k_subject, 
        message: k_message
    };

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", path, true);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

    xhttp.responseType = 'text';
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) { 
            //document.getElementById("debug").innerHTML = xhttp.responseText;
            if ('true ' == xhttp.responseText.split("|")[0]) {
                //document.getElementById("debug").innerHTML = "HERE";
                $('#first_name').remove();
                $('#last_name').remove(); 
                $('#contact_email').remove();
                $('#subject').remove(); 
                $('#message').remove();
                $('#contact-submit').remove(); 

                $('.contact-box-hide').slideUp();
                $('.contact-message').html('<i class="fa fa-check contact-success"></i><div>Your message has been sent.</div>').fadeIn();
            } else {
                //document.getElementById("debug").innerHTML = "THERE";
                $('.contact-box-hide').hide();
                $('.contact-message').html('<i class="fa fa-exclamation contact-error"></i><div>Something went wrong, please try again later.</div>').fadeIn();
            }
        }
    };

    xhttp.send(JSON.stringify(data));

      /* Post Ajax function of jQuery to get all the data from the submission of the form as soon as the form sends the values to email.php*/
/*      $.post("php/contact.php", $("#contact-form").serialize(),function(result){
        //Check the result set from email.php file.
        if(result == 'sent'){



          //If the email is sent successfully, remove the submit button
          $('#first_name').remove();
          $('#last_name').remove(); 
          $('#contact_email').remove();
          $('#subject').remove(); 
          $('#message').remove();
          $('#contact-submit').remove(); 

          $('.contact-box-hide').slideUp();
          $('.contact-message').html('<i class="fa fa-check contact-success"></i><div>Your message has been sent.</div>').fadeIn();
        } else {
          $('.btn-contact-container').hide();
          $('.contact-message').html('<i class="fa fa-exclamation contact-error"></i><div>Something went wrong, please try again later.</div>').fadeIn();
            
        }
      });
*/
    }
  });  
 
         
  function validateEmail(sEmail) {
    var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    if (filter.test(sEmail)) {
      return true;
    } else {
      return false;
    }
  } 
 

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

	/* Contact End
	-------------------------------------------------------------------*/


    

    



});

/* Document Ready function End
-------------------------------------------------------------------*/


/* Preloder 
-------------------------------------------------------------------*/
$(window).load(function () {    
    "use strict";
    $("#loader").fadeOut();
    $("#preloader").delay(350).fadeOut("slow");
});
 /* Preloder End
-------------------------------------------------------------------*/
   
