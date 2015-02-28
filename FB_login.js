
//variables to calculate estimated income, baseline as of 2012
//http://www.usnews.com/education/best-graduate-schools/articles/2012/06/29/6-reasons-why-graduate-school-pays-off
var salaryGrad = 55242;
var salaryColl = 42877;
//http://work.chron.com/average-salary-college-degree-1861.html
var salaryHS = 30000;
//no data or no HS -- average in 2013
//http://quickfacts.census.gov/qfd/states/00000.html
var salaryNoData = 28155;

//rough average annual salary increase once someone has graduated
//http://www.usatoday.com/story/money/business/2014/09/07/2015-pay-raises-should-average-3/15136423/
var avgSalaryInc = 0.03; 

//today's date
var today = new Date();

//these are the codes needed to query the db
//objects include some text values for display
var ageCodes = {
  1 : {range: '< 20', verb: 'under 20', code: 1},
  2 : {range: '20-29', verb: 'twenties'},
  // median age is ~38 https://www.cia.gov/library/publications/the-world-factbook/geos/us.html
  3 : {range: '30-39', verb: 'thirties'}, 
  4 : {range: '40-49', verb: 'forties'},
  5 : {range: '50-59', verb: 'fifties'},
  6 : {range: '60-69', verb: 'sixties'},
  7 : {range: '70+', verb: 'seventies'},
}

education_codes = {
  0 : "Never attended school",
  10 : "First through 8th grade",
  11 : "Ninth through 12th grade (did not graduate)",
  12 : "High school graduate",
  13 : "Some college (did not graduate)",
  14 : "Associate's/vocational degree",
  15 : "Bachelor's degree",
  16 : "Master's or Doctoral degree",
  17 : "No data reported"
}


income_codes = {
  1 : "Less than $5,000",
  2 : "$5,000 to $9,999",
  3 : "$10,000 to $14,999",
  4 : "$15,000 to $19,999",
  5 : "$20,000 to $29,999",
  6 : "$30,000 to $39,999",
  7 : "$40,000 to $49,999",
  8 : "$50,000 to $69,999",
  9 : "$70,000 and over",
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



    //these functions get some data about the user and makes some guesses about 
    // some of their demo characteristics
      // var userEducation= function() {
      //   //start with info about education
      //   var userEdObj = {};
      //   var edList = [];
      //   if (userFBInfo.education.length > 0) { // if any education info is present
      //     for (i = 0; i < (userFBInfo.education).length; i++) { // loop through the object
      //       if (userFBInfo.education[i].year !== undefined) {  // if the year is available
      //         userEdObj[userFBInfo.education[i].type] = parseInt(userFBInfo.education[i].year.name); // append info to obj
      //         edList.push(parseInt(userFBInfo.education[i].year.name)); // append year to list

      //         //determine highest level of education based on the highest 'type' in the user object
      //         //this is not foolproof, but will give us a rough idea of education and salary

      //         //variables being set
      //         var userSalaryBase;
      //         var queryEducation;
      //         var lastGradYr;
      //         var yearsSinceGrad;
      //         var userIncome;
      //         var queryIncome;

      //         if ('Graduate School' in userEdObj) {
      //           userSalaryBase = salaryGrad; // set base salary to average
      //           queryEducation = 16; // set a userEd var for DB query
      //           lastGradYr = Math.max.apply(Math, edList); 
      //           yearsSinceGrad = (new Date().getFullYear())-lastGradYr; //years since we have graduation info
      //           console.log("Last:" + lastGradYr);

      //           //check if the last grad year is grad school
      //             if lastGradYr == userEdObj['Graduate School'] {
      //                 // compound with average increase per year A = P ( 1+r ) ^ t 
      //                 queryIncome = userSalaryBase*Math.pow((1+avgSalaryInc),yearsSinceGrad); 
      //                 console.log(queryIncome);
      //             } else {
      //               //assume grad school was 4 years after last grad year
      //               queryIncome = userSalaryBase*Math.pow((1+avgSalaryInc),(lastGradYear+4)); 
      //               console.log(queryIncome);
      //             }

      //         } else if ('College' in userEdObj && !('Graduate School' in userEdObj)) {
      //           userSalaryBase = salaryColl;
      //           queryEducation = 15;
      //             if lastGradYr == userEdObj['College']{
      //                 // compound with average increase per year A = P ( 1+r ) ^ t 
      //                 queryIncome = userSalaryBase*Math.pow((1+avgSalaryInc),yearsSinceGrad); 
      //                 console.log(queryIncome);
      //             } else {
      //               //assume college was 2 years after last grad year
      //               queryIncome = userSalaryBase*Math.pow((1+avgSalaryInc),(lastGradYear+4)); 
      //               console.log(queryIncome);

      //         } else if ('High School' in userEdObj && !('College' in userEdObj) 
      //           && !('Graduate School' in userEdObj)) { 
      //           var userSalaryBase = salaryHS;
      //           var userIncome = 12;

      //         } else { // no data given on education, assuming no education
      //           var userSalaryBase = salaryNoData;
      //           var userEducation = 5;
      //         }
      //         //figure out last available grad year to help calc salary, age
      //         console.log(userIncome);
      //         console.log(userSalaryBase);
      //         console.log(avgSalaryInc);
      //         console.log(yearsSinceGrad);


      //       } else {                  // if the year not available, add a key, but year == 0
      //           userEdObj['userFBInfo.education[i]type'] = 0; 
      //       }
      //         // console.log(userEdObj);
      //         // console.log(edList);
      //       }
      //   } 

      // }

      var userAge = function() {
        if (userFBInfo.birthday != undefined) {
          console.log("We have a birthday!");
          var bDay = new Date(userFBInfo.birthday);
          var ageYr = Math.round(parseInt((today-bDay)/(1000*60*60*24))/365);
          console.log(ageYr);
          if (ageYr < 20) {
            queryAge = 1;
          } else if (ageYr >= 20 && ageYr < 30){
            queryAge = 2;
          } else if (ageYr >= 30 && ageYr < 40){
            queryAge = 3;
          } else if (ageYr >= 40 && ageYr < 50){
            queryAge = 4;
          } else if (ageYr >= 50 && ageYr < 60){
            queryAge = 5;
          } else if (ageYr >= 60 && ageYr < 70){
            queryAge = 6;
          } else {
             queryAge = 7;
          }
        } else {
          console.log("else");
        }
        console.log(queryAge);
        return(queryAge);
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
          console.log(new Date().getFullYear())
        })
      });

      console.log("name: " + userFBInfo.first_name);
      console.log("gender: " + userFBInfo.gender);
      console.log("loc: " + userFBInfo.location.id);

      console.log(userFBInfo.education[1].year.name);
      console.log((userFBInfo.education).length);
      console.log(userFBInfo.education[0].year);
      userAge();
      console.log(locationURL, locationURL.id);
      console.log("education " + (userFBInfo.education).length);
    });
    
  }

