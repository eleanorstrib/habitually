

var ageCodes = {
  1 : {range: '< 20', verb: 'under 20'},
  2 : {range: '20-29', verb: 'twenties'},
  3 : {range: '30-39', verb: 'thirties'}, 
  4 : {range: '40-49', verb: 'forties'},
  5 : {range: '50-59', verb: 'fifties'},
  6 : {range: '60-69', verb: 'sixties'},
  7 : {range: '70+', verb: 'seventies'},
}


var regionCodes = {
  AL: {code: 4, region: 'Western'},
  AZ: {code: 4, region: 'Western'},
  CA: {code: 4, region: 'Western'},
  CO: {code: 4, region: 'Western'},
  //FIX ME -- ADD ALL STATES
  // 1: {Northeast:
  //     ['CT', 'ME', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']},
  // 2: {Midwest:
  //     ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NB', 'ND', 'OH', 'SD', 'WI']},
  // 3 : {South: 
  //     ['AL', 'AK', 'DE', 'DC', 'FL', 'GA', 'KY', 'LA', 'MD', 'MI', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA', 'WV']},
  // 4 : {West: ['AK', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MT', 'NV', 'NM', 'OR', 'UT', 'WA', 'WI']},
};

//Checks if user is logged in and displays a message based on the result
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    // console.log(response);
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      callAPI(); //
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
function callAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.first_name);
      document.getElementById('status').innerHTML =
        'Thanks for logging in, ' + response.name + '!';
      console.log(response);
      var userFBInfo = response;
      var locationURL = "http://graph.facebook.com/" + userFBInfo.location.id
      // var education_year = _.each(userFBInfo.education, function(education){
      //   console.log(education.get("school"));
      // });

    //this function finds the last grad year available for the user
      var edyear = function() {
        edList = [];
        for(x = 0; x < (userFBInfo.education).length; x++) {
            if (userFBInfo.education[x].year !== undefined) {
              edList.push(parseInt(userFBInfo.education[x].year.name));
            } else {
              continue;
            }
        lastGradYr = Math.max.apply(Math, edList);
        console.log("Last:" + lastGradYr);
        }
      }

      // gets location data for the user, passes back a region code 
      //needed to query the database
      $.getJSON(locationURL, function(data){
        var locationIn = data.location.located_in; // this is the id of the parent location
        var parentLocationURL = "http://graph.facebook.com/" + locationIn; //url for the object needed
        $.getJSON(parentLocationURL, function(moreData){
          var userState = moreData.location.state; // goes into the object for parent loc, gets state
          console.log(userState);
          console.log(regionCodes[userState].region);
        })
      });

      console.log("name: " + userFBInfo.first_name);
      console.log("gender: " + userFBInfo.gender);
      console.log("loc: " + userFBInfo.location.id);

      console.log(userFBInfo.education[1].year.name);
      console.log((userFBInfo.education).length);
      console.log(userFBInfo.education[0].year);
      edyear();
      console.log(locationURL, locationURL.id);
    });
    
  }

