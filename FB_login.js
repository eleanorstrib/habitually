console.log("accessed js file");


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

// //these are the codes needed to query the db
// //objects include some text values for display
// var ageCodes = {
//   1 : {range: '< 20', verb: 'under 20', code: 1},
//   2 : {range: '20-29', verb: 'twenties'},
//   // median age is ~38 https://www.cia.gov/library/publications/the-world-factbook/geos/us.html
//   3 : {range: '30-39', verb: 'thirties'}, 
//   4 : {range: '40-49', verb: 'forties'},
//   5 : {range: '50-59', verb: 'fifties'},
//   6 : {range: '60-69', verb: 'sixties'},
//   7 : {range: '70+', verb: 'seventies'},
// }

// education_codes = {
//   0 : "Never attended school",
//   10 : "First through 8th grade",
//   11 : "Ninth through 12th grade (did not graduate)",
//   12 : "High school graduate",
//   13 : "Some college (did not graduate)",
//   14 : "Associate's/vocational degree",
//   15 : "Bachelor's degree",
//   16 : "Master's or Doctoral degree",
//   17 : "No data reported"
// }




  //FIX ME -- ADD ALL STATES
var regionCodes = {
  AL: {code: 4, region: 'Western'},
  AZ: {code: 4, region: 'Western'},
  CA: {code: 4, region: 'Western'},
  CO: {code: 4, region: 'Western'},

  // 1: {Northeast:
  //     ['CT', 'ME', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']},
  // 2: {Midwest:
  //     ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NB', 'ND', 'OH', 'SD', 'WI']},
  // 3 : {South: 
  //     ['AL', 'AK', 'DE', 'DC', 'FL', 'GA', 'KY', 'LA', 'MD', 'MI', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA', 'WV']},
  // 4 : {West: ['AK', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MT', 'NV', 'NM', 'OR', 'UT', 'WA', 'WI']},
};

//wrapping the initialization of FB SDK into some JS to pull
//app id from the "secret" file
$.getScript("secret.js", function(){

    //Initializes SDK
    window.fbAsyncInit = function() {
      console.log("get it started")
      FB.init({
        appId      : FB_APP_ID,
        cookie     : true,  // enable cookies, server can access session
        xfbml      : true,  // parse social plugins on this page
        version    : 'v2.2', // use version 2.2
        status     : true   // check for user status on load
      });


  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  }

    // // Checks user status post-login
      function checkLoginState() {
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
// });

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
      var userEducation= function() {
        //start with info about education
        var userEdObj = {};
        var edList = [];
        if (userFBInfo.education.length > 0) { // if any education info is present
          for (i = 0; i < (userFBInfo.education).length; i++) { // loop through the object
            if (userFBInfo.education[i].year !== undefined) {  // if the year is available
              userEdObj[userFBInfo.education[i].type] = parseInt(userFBInfo.education[i].year.name); // append info to obj
              edList.push(parseInt(userFBInfo.education[i].year.name)); // append year to list

              //determine highest level of education based on the highest 'type' in the user object
              //this is not foolproof, but will give us a rough idea of education and salary

              //variables being set
              var userSalaryBase;
              var queryEducation;
              var lastGradYr;
              var yearsSinceGrad;
              var userIncome;

              if ('Graduate School' in userEdObj) {
                userSalaryBase = salaryGrad; // set base salary to average
                queryEducation = 5; // set a userEd var for DB query
                lastGradYr = Math.max.apply(Math, edList); 
                yearsSinceGrad = (new Date().getFullYear())-lastGradYr; //years since we have graduation info

                //check if the last grad year is grad school
                  if (lastGradYr == userEdObj['Graduate School']) {
                      // compound with average increase per year A = P ( 1+r ) ^ t 
                      userIncome = userSalaryBase*Math.pow((1+avgSalaryInc),yearsSinceGrad); 
                  } else {
                    //assume grad school was 4 years after last grad year
                    userIncome = userSalaryBase*Math.pow((1+avgSalaryInc),(lastGradYear+4)); 
                  }

              } else if ('College' in userEdObj && !('Graduate School' in userEdObj)) {
                userSalaryBase = salaryColl;
                queryEducation = 4;
                  if (lastGradYr == userEdObj['College']){
                      // compound with average increase per year A = P ( 1+r ) ^ t 
                      userIncome = userSalaryBase*Math.pow((1+avgSalaryInc),yearsSinceGrad); 
                  } else {
                    //assume college was 2 years after last grad year
                    userIncome = userSalaryBase*Math.pow((1+avgSalaryInc),(lastGradYear+4)); 
                  }
              } else if ('High School' in userEdObj && !('College' in userEdObj) && !('Graduate School' in userEdObj)) { 
                var userSalaryBase = salaryHS;
                var userIncome = 2;

              } else { // no data given on education, assuming HS grad
                var userSalaryBase = salaryNoData;
                var queryEducation = 2;
              }

              if (userIncome < 20000) {
                queryIncome = 1;
              } else if (userIncome >= 20000 && userIncome <= 39999) {
                queryIncome = 2;
              } else if (userIncome >= 40000 && userIncome <= 59999){
                queryIncome = 3;
              } else if (userIncome >= 60000) {
                queryIncome = 4;
              } else {
                queryIncome = 3; //if no income provided, assume average
              }
              console.log("queryIncome =" + queryIncome)
              console.log("queryEducation = " + queryEducation);

            // #FIX ME -- double check if needed
            } else {  
                // if the year not available, add a key, but year == 0
                userEdObj['userFBInfo.education[i]type'] = 0; 
                // queryIncome = 
            }
              // console.log(userEdObj);
              // console.log(edList);
            }
        } 

      } // end of userEducationIncome function

      var userAge = function() {
        if (userFBInfo.birthday != undefined) {
          var bDay = new Date(userFBInfo.birthday);
          var ageYr = Math.round(parseInt((today-bDay)/(1000*60*60*24))/365);
          if (ageYr < 20) {
            queryAge = 1;
          } else if (ageYr >= 20 && ageYr < 30) {
            queryAge = 2;
          } else if (ageYr >= 30 && ageYr < 40) {
            queryAge = 3;
          } else if (ageYr >= 40 && ageYr < 50) {
            queryAge = 4;
          } else if (ageYr >= 50 && ageYr < 60) {
            queryAge = 5;
          } else if (ageYr >= 60 && ageYr < 70) {
            queryAge = 6;
          } else if (ageYr > 70) {
             queryAge = 7;
          }
        // if we can't find an age, assume 
        } else {
          //average age in the US is 37, use 30s
          queryAge = 3;
        }
        console.log("queryAge " + queryAge);
      }

      console.log("test again" + userFBInfo.gender);
      var queryGender;
      var userGender = function() {
        if (userFBInfo.gender == "male") {
          queryGender = 1;
        } else {
          //since most FB users and a small majority of the population is female
          //this will also take cases where the gender is custom-defined for now
          queryGender = 2;
          console.log("queryGender = " + queryGender);
        }
        // return queryGender;
      }


      // gets location data for the user, passes back a region code 
      //needed to query the database
      var userRegion = function() {
            $.getJSON(locationURL, function(data){
              var locationIn = data.location.located_in; // this is the id of the parent location
              var parentLocationURL = "http://graph.facebook.com/" + locationIn; //url for the object needed
              $.getJSON(parentLocationURL, function(moreData){
                var userState = moreData.location.state; // goes into the object for parent loc, gets state
                var printRegion = regionCodes[userState].region;
                var queryRegion = regionCodes[userState].code;
                console.log("queryRegion = "  + queryRegion);
              })
            });
          }

      console.log("name: " + userFBInfo.first_name);
      userAge();
      userGender();
      userEducation();
      userRegion();


      
      
    //   console.log(userFBInfo.education[1].year.name);
    //   console.log((userFBInfo.education).length);
    //   console.log(userFBInfo.education[0].year);

    //   console.log(locationURL, locationURL.id);
    //   console.log("education " + (userFBInfo.education).length);
    });
    
  }

