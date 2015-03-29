var facebooklogin = function(){//variables to calculate estimated income, baseline as of 2012
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
  CT: {code: 1, region: 'Northeastern'},
  MA: {code: 1, region: 'Northeastern'},
  ME: {code: 1, region: 'Northeastern'},
  NH: {code: 1, region: 'Northeastern'},
  NJ: {code: 1, region: 'Northeastern'},
  NY: {code: 1, region: 'Northeastern'},
  PA: {code: 1, region: 'Northeastern'},
  RI: {code: 1, region: 'Northeastern'},
  VT: {code: 1, region: 'Northeastern'},
  IA: {code: 2, region: 'Midwestern'},
  IL: {code: 2, region: 'Midwestern'},
  IN: {code: 2, region: 'Midwestern'},
  KS: {code: 2, region: 'Midwestern'},
  MI: {code: 2, region: 'Midwestern'},
  MN: {code: 2, region: 'Midwestern'},
  MO: {code: 2, region: 'Midwestern'},
  NB: {code: 2, region: 'Midwestern'},
  ND: {code: 2, region: 'Midwestern'},
  OH: {code: 2, region: 'Midwestern'},
  SD: {code: 2, region: 'Midwestern'},
  WI: {code: 2, region: 'Midwestern'},
  AL: {code: 3, region: 'Southern'},
  AK: {code: 3, region: 'Southern'},
  DE: {code: 3, region: 'Southern'},
  DC: {code: 3, region: 'Southern'},
  FL: {code: 3, region: 'Southern'},
  GA: {code: 3, region: 'Southern'},
  KY: {code: 3, region: 'Southern'},
  LA: {code: 3, region: 'Southern'},
  MD: {code: 3, region: 'Southern'},
  MI: {code: 3, region: 'Southern'},
  NC: {code: 3, region: 'Southern'},
  OK: {code: 3, region: 'Southern'},
  SC: {code: 3, region: 'Southern'},
  TN: {code: 3, region: 'Southern'},
  TX: {code: 3, region: 'Southern'},
  VA: {code: 3, region: 'Southern'},
  WV: {code: 3, region: 'Southern'},
  AL: {code: 4, region: 'Western'},
  AZ: {code: 4, region: 'Western'},
  CA: {code: 4, region: 'Western'},
  CO: {code: 4, region: 'Western'},
  // HI: {code: 4, region: 'Western'},
  // ID: {code: 4, region: 'Western'},
  // MT: {code: 4, region: 'Western'},
  // NV: {code: 4, region: 'Western'},
  // NM: {code: 4, region: 'Western'},
  // OR: {code: 4, region: 'Western'},
  // UT: {code: 4, region: 'Western'},
  // WA: {code: 4, region: 'Western'},
  // WI: {code: 4, region: 'Western'},
};

var userData = {};// this object will store the data that will be used to query the db

//Checks if user is logged in and displays a message based on the result
// This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      callAPI();
    } else if (response.status === 'not_authorized') {
      // The person is logged into Facebook, but not the app.
      document.getElementById('status').innerHTML = 'Click to log ' +
        'into this app.';
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
      document.getElementById('status').innerHTML = 'Click to log ' +
        'into Facebook.';
    }
  }

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }

  window.fbAsyncInit = function() {
  FB.init({
    appId      : 418088358316146,
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.2', // use version 2.2

  });

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


  // call social graph API
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



  //   //these functions get some data about the user and makes some guesses about 
    // some of their demo characteristics
      var userEducation= function() {//checked everything closed
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

              userData.queryEducation = queryEducation;

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
              console.log("queryIncome =" + queryIncome);
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
        userData.queryIncome = queryIncome;
      } // end of userEducationIncome function

    var userAge = function() {
        if (userFBInfo.birthday != undefined) {
          var bDay = new Date(userFBInfo.birthday);
          console.log("at the math part");
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
          } else {
          //average age in the US is 37, use 30s
          queryAge = 3;
          }
        console.log("queryAge " + queryAge);
        userData.queryAge = queryAge;
      }
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
          userData.queryGender = queryGender;
          console.log("queryGender = " + queryGender);
        }
        // return queryGender;
      }
      userGender();
      userEducation();
      userAge();
      console.log("user data before region");
      console.log(userData);

      // gets location data for the user, passes back a region code 
      //needed to query the database
      var queryRegion;
      //Needs to be updated
      var userRegion = function() {
        $.when($.getJSON(locationURL)).done(function(data){
          //Facebook removed this field
          var locationIn = data.location.located_in; // this is the id of the parent location
          console.log(locationIn);
          var parentLocationURL = "http://graph.facebook.com/" + locationIn; //url for the object needed
          console.log(parentLocationURL);
          $.when($.getJSON(parentLocationURL)).done(function(moreData){
            var userState = moreData.location.state; // goes into the object for parent loc, gets state
            console.log(userState);
            var printRegion = regionCodes[userState].region;
            console.log(printRegion);
            var queryRegion = regionCodes[userState].code;
            console.log("queryRegion = "  + queryRegion);
            userData.queryRegion = queryRegion;
            console.log("Region function UD: ");
            console.log(userData);
              $.ajax({
                url:'/userDataJS.json',
                type: 'POST',
                data: userData,
                success: function(data){console.log(data)},
                dataType:'json'
              });
              console.log("Success! FB data sent!");

          });//end of nested
         });//end of getJson
      }

    //   console.log("name: " + userFBInfo.first_name);
    userRegion();

      // console.log("userData", userData);
      }); //closes FB.api
      
} //closes callAPI function
}; // closes main function
    
  

