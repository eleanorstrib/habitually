//code in this file initializes the FB SDK and 
// gets user data into a JS object when the app is authorized

//Checks if user is logged in and displays a message based on the result
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      testAPI(); //
    } else if (response.status === 'not_authorized') {
      // Logged into Facebook, not the app.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    } else {
      // Not logged into FB, assume not logged into the app.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into Facebook.';
    }
  }

//wrapping the initialization of FB SDK into some JS to pull
//app id from the "secret" file
$.getScript("secret.js", function(){

	  //Initializes SDK
	  window.fbAsyncInit = function() {
		  FB.init({
		    appId      : FB_APP_ID,
		    cookie     : true,  // enable cookies, server can access session
		    xfbml      : true,  // parse social plugins on this page
		    version    : 'v2.2', // use version 2.2
		    status     : true   // check for user status on load
		  });

	  // Checks user status post-login
		  FB.getLoginStatus(function(response) {
		    statusChangeCallback(response);
		  });

	  };

	  // Load the SDK asynchronously
	  (function(d, s, id) {
	    var js, fjs = d.getElementsByTagName(s)[0];
	    if (d.getElementById(id)) return;
	    js = d.createElement(s); js.id = id;
	    js.src = "//connect.facebook.net/en_US/sdk.js";
	    fjs.parentNode.insertBefore(js, fjs);
	  }(document, 'script', 'facebook-jssdk'));


   // Use anything defined in the loaded script...
});
 
  // Test of social graph API, and call for object containing response
function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.first_name);
      document.getElementById('status').innerHTML =
        'Thanks for logging in, ' + response.name + '!';
      console.log(response);
      return response
    });
    
  }

var userDataFB = testAPI();
