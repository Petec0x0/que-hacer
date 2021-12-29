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
var login_form = document.forms['login_form'];


// set cookie function
function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function login_now(){
    //display spin loader
    spin_loader.style.display = 'block';
    
    // get form data
    var username = login_form.username.value;
    var password = login_form.password.value;

    // validate form data
    if((username == "") || (password == "")){
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
                var token = json_reponse.token;
                setCookie('token',token,7);
                // hide spin loader
                spin_loader.style.display = 'none';
                alert("Credentials verified successfully");
                // redirect to login page 
                window.location = `${api_host_url}todos`;
            }
        }else if(this.status == 401){
            // show info/alert box
            info_box.style.display = 'block';
            // hide spin loader
            spin_loader.style.display = 'none';
        }
    };
    xhttp.open("POST", api_host_url+"auth/login", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhttp.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password));
    xhttp.send(JSON.stringify({username:username, password:password}));
}