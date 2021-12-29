var api_host_url = "https://que-hacer.onyedikachiudeh.repl.co/";

// get the spin-loader
var spin_loader = document.getElementById('spin_loader');
// get the init_message
var init_message = document.getElementById('init_message');
// get the todos container
var todos_container = document.getElementById('todos_container');

// get cookie function 
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

// function for updating the todos container from the API
function update_todos(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // get the json response from the server
            var json_reponse = JSON.parse(this.responseText);
            // check if it returned an error
            if(json_reponse.error == false){
                var all_output = '';
                var todos = json_reponse.todos;
                console.log(todos);
                // display the todos
                for (todo of todos) {
                    if(todo.completed == true){
                        all_output += '<li class="completed">\
                                            <div class="form-check">\
                                                <label class="form-check-label">\
                                                <input class="checkbox" type="checkbox" checked="">\
                                                '+todo.body+'<i class="input-helper"></i>\
                                                </label>\
                                            </div> <i onclick="deleteTodo('+todo.id+')" class="remove mdi mdi-close-circle-outline"></i>\
                                        </li>';
                    }else{
                        all_output += '<li>\
                                            <div class="form-check">\
                                                <label class="form-check-label">\
                                                <input onclick="markComplete('+todo.id+')" class="checkbox" type="checkbox">\
                                                '+todo.body+'<i class="input-helper"></i>\
                                                </label>\
                                            </div> <i onclick="deleteTodo('+todo.id+')" class="remove mdi mdi-close-circle-outline"></i>\
                                        </li>';
                    }
                }
                todos_container.innerHTML = all_output;

                // hide spin loader & init_message
                spin_loader.style.display = 'none';
                // remove the init_message is todos is not empty

                if ((todos === undefined || todos.length == 0)) {
                    init_message.style.display = 'block';
                }
                
            }
        }else if(this.status == 401){
            // show info/alert box
            alert("Your session has expired. Please log in again.");
            // redirect to login page 
            window.location = "index.html";
        }
    };
    xhttp.open("GET", api_host_url+"todo/get", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhttp.setRequestHeader('X-access-token', getCookie('token'));
    xhttp.send();
}


// function for creating a todo
function create_todo(){
    // get the todo form input data
    var todo_body = document.getElementById('todo_body').value;
    // make sure it is not empty
    if(todo_body == ''){
        alert('You cant have an empty field')
        return false;
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // get the json response from the server
            var json_reponse = JSON.parse(this.responseText);
            // check if it returned an error
            if(json_reponse.error == false){
                update_todos();
            }else{
                alert("Sorry, there was an error with your request.")
            }
        }
    };
    xhttp.open("POST", api_host_url+"todo/create", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader('Access-Control-Request-Headers', 'x-requested-with');
    xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhttp.setRequestHeader('X-access-token', getCookie('token'));
    xhttp.send(JSON.stringify({body:todo_body, reminder:false}));
}


// function for marking the check box as complete
function markComplete(todo_id){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // get the json response from the server
            var json_reponse = JSON.parse(this.responseText);
            // check if it returned an error
            if(json_reponse.error == false){
                update_todos();
            }else{
                alert("Sorry, there was an error with your request.")
            }
        }
    };
    xhttp.open("PUT", api_host_url+"todo/complete", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhttp.setRequestHeader('X-access-token', getCookie('token'));
    xhttp.send(JSON.stringify({todo_id:todo_id}));
}

// function for deleting a todo
function deleteTodo(todo_id){
    // show spin loader & init_message
    spin_loader.style.display = 'block';

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // get the json response from the server
            var json_reponse = JSON.parse(this.responseText);
            // check if it returned an error
            if(json_reponse.error == false){
                update_todos();
            }else{
                alert("Sorry, there was an error with your request.")
            }
        }
    };
    xhttp.open("DELETE", api_host_url+"todo/delete", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhttp.setRequestHeader('X-access-token', getCookie('token'));
    xhttp.send(JSON.stringify({todo_id:todo_id}));
}

update_todos();