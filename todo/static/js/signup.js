var api_host_url = "https://que-hacer.onyedikachiudeh.repl.co/";

// get the spin-loader
var spin_loader = document.getElementById('spin_loader');
// hide spin loader
spin_loader.style.display = 'none';

// get info_box/alert box for displaying messages
var info_box = document.getElementById('info_box');
// hide the alert box
info_box.style.display = 'none';

// get the signup form
var signup_form = document.forms['signup_form'];

function signup_now(){
    //display spin loader
    spin_loader.style.display = 'block';
    
    // get form data
    var username = signup_form.username.value;
    var email = signup_form.email_address.value;
    var password = signup_form.password.value;

    // validate form data
    if((username == "") || (email == "") || (password == "")){
        alert("Error: You can't have an empty form field")
        // hide spin loader
        spin_loader.style.display = 'none';
        return false;
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // get the json response from the server
            var json_reponse = JSON.parse(this.responseText);
            // check if it returned an error
            if(json_reponse.error == false){
                // hide spin loader
                spin_loader.style.display = 'none';
                // show info/alert box
                info_box.style.display = 'block';
                alert("Your account was created successfully");
                // redirect to login page 
                window.location = `${api_host_url}home`;
            }else{
                alert("Sorry, there was an error with your request.")
            }
        }
    };
    xhttp.open("POST", api_host_url+"auth/signup", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader('Access-Control-Request-Headers', 'x-requested-with');
    xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhttp.send(JSON.stringify({username:username, email:email, password:password}));
}
