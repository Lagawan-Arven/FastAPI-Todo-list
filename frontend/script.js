api_url = "http://127.0.0.1:8000";

/*===============================
SIGN IN BUTTON FUNCTION
================================*/
document.getElementById("signin").addEventListener("click",function(){
    document.getElementById("login-container").style.display = "none";
    document.getElementById("signin-container").style.display = "block";
});
/*============
return button1
==============*/
document.getElementById("return-btn1").addEventListener("click",function(){
    document.getElementById("login-container").style.display = "block";
    document.getElementById("signin-container").style.display = "none";
});
/*============
confirm sign in
==============*/
document.getElementById("confirm-signin").addEventListener("click",async function(){
    const username = document.getElementById("signin-username").value;
    const password = document.getElementById("signin-password").value;

    const credentials = {username,password};

    const res = await fetch(`${api_url}/signin`,{
        method: "POST",
        body: JSON.stringify(credentials)
    });
    const response = await res.json();

    if (response.message === "Successful"){

        alert("Sign in successful!");
        document.getElementById("login-section").style.display = "none";
        document.getElementById("main").style.display = "block";

        document.getElementById("signin-username").value = "";
        document.getElementById("signin-password").value = "";

    }else if (response.message === "incorrect password"){
        alert("Incorrect password!");
        document.getElementById("signin-username").value = "";
        document.getElementById("signin-password").value = "";     
    }else if(response.message === "account does not exist"){
        alert("Account does not exist!");
        document.getElementById("signin-username").value = "";
        document.getElementById("signin-password").value = "";
    }else if(response.message === "no users yet"){
        alert("There is no users yet!");
        document.getElementById("signin-username").value = "";
        document.getElementById("signin-password").value = "";
    }
    
});

/*===============================
SIGN UP BUTTON FUNCTION
================================*/
document.getElementById("signup").addEventListener("click",function(){
    document.getElementById("login-container").style.display = "none";
    document.getElementById("signup-container").style.display = "block";
});
/*============
return button2
==============*/
document.getElementById("return-btn2").addEventListener("click",function(){
    document.getElementById("login-container").style.display = "block";
    document.getElementById("signup-container").style.display = "none";
});
/*============
confirm sign up
==============*/
document.getElementById("confirm-signup").addEventListener("click",async function(){
    const username = document.getElementById("signup-username").value;
    const password = document.getElementById("signup-password").value;
    const confirm_password = document.getElementById("confirm-password").value;

    if (password === confirm_password){
       const credentials = {username,password};

       const res = await fetch(`${api_url}/register`,{
        method: "POST",
        body: JSON.stringify(credentials)
    });
    const response = await res.json();
    if (response.message === "user added successfully!"){
        alert("Account Created Successfully!");

        document.getElementById("signup-container").style.display = "none";
        document.getElementById("signin-container").style.display = "block";
        }

    else if(response.message === "user already existed!"){
        document.getElementById("signup-username").value = "";
        document.getElementById("signup-password").value = "";
        document.getElementById("confirm-password").value = "";
    }
    }

    else{
        alert("Password did not match!");
        document.getElementById("confirm-password").value = "";       
    }
 
});


/*===============================
            LOAD ALL TODOS
================================*/
async function load_todos(){
    const res = await fetch(`${api_url}/todos`);
    const todos = await res.json();
 
    const table = document.getElementById("todo-table");
    table.innerHTML = "";

    todos.forEach(todo =>{
        const row = document.createElement("tr");
        row.innerHTML = `
        <td>${todo.id}</td>
        <td>${todo.name}</td>
        <td>${todo.priority}</td>
        <td>${todo.difficulty}</td>
        <td>${todo.status}</td>
        <td><button class="dlt-btn" onclick="delete_todo(${todo.id})">Delete</button></td>
        `;
    table.appendChild(row);
    });
}

/*===============================
            SEARCH TODOS
================================*/
/*
document.getElementById("search-todo").addEventListener("input",async function(){

    const query = this.value;

    const res = await fetch(`${api_url}/todos/search?q=${query}`);
    const todos = await res.json();
    const table = document.getElementById("todo-table");
    table.innerHTML = "";

    todos.forEach(todo =>{

        const row = document.createElement("tr");
        row.innerHTML = `
        <td>${todo.id}</td>
        <td>${todo.name}</td>
        <td>${todo.priority}</td>
        <td>${todo.difficulty}</td>
        <td>${todo.status}</td>
        <td><button class="dlt-btn" onclick="delete_todo(${todo.id})">Delete</button></td>
        `;
    table.appendChild(row);

    });   

});

/*===============================
            ADD TODO
================================*/
async function add_todo(){
    const name = document.getElementById("name").value;
    const priority = document.getElementById("priority").value;
    const difficulty = document.getElementById("difficulty").value;
    const status = document.getElementById("status").value;

    todo = {name,priority,difficulty,status};

    await fetch(`${api_url}/todos`,{
        method: "POST",
        body: JSON.stringify(todo)
    });
    alert("Todo successfully added!");
    load_todos(current_user_id);
}

/*===============================
           UPDATE TODO
================================*/
/*
async function update_todo(todo_id){
    const name = document.getElementById("name").value;
    const priority = document.getElementById("priority").value;
    const difficulty = document.getElementById("difficulty").value;
    const status = document.getElementById("status").value;

    todo = {name,priority,difficulty,status};

    await fetch(`${api_url}/todos/${todo_id}`,{
        method: "PATCH",
        body: JSON.stringify(todo)
    });
    alert("Todo successfully updated!");
    load_todos(current_user_id);   
}

/*===============================
           DELETE TODO
================================*/
/*
async function delete_todo(todo_id){
    await fetch(`${api_url}/todos/${todo_id}`,{
        method: "DELETE"
    });
    load_todos(current_user_id);
    alert("Todo deleted!");
}


/* add todo button ==> displaying the form */
    document.getElementById("add-todo").addEventListener("click",function(){
    document.getElementById("form-container").style.display = "block";
    document.getElementById("front-container").style.display = "none";
    const updateback = document.getElementById("save-todo");
    updateback.textContent = "Save todo";
    updateback.setAttribute("onclick", "add_todo()");
});
/* back button ==> switching form display to none */
document.getElementById("back").addEventListener("click",function(){
    document.getElementById("form-container").style.display = "none";
    document.getElementById("front-container").style.display = "block";
});
/* update todo button ==> displaying ID input */
document.getElementById("update-todo").addEventListener("click",function(){
    document.getElementById("id").style.display = "block";
    document.getElementById("confirm").style.display = "block";
    document.getElementById("back-confirm").style.display = "block";
    document.getElementById("update-todo").style.display = "none";
});
/* back-confirm button ==> displaying back the update button */
document.getElementById("back-confirm").addEventListener("click",function(){
    document.getElementById("id").style.display = "none";
    document.getElementById("confirm").style.display = "none";
    document.getElementById("back-confirm").style.display = "none";
    document.getElementById("update-todo").style.display = "block";
});
/* update todo confirm button ==> displaying the form */
document.getElementById("confirm").addEventListener("click",function(){
    document.getElementById("form-container").style.display = "block";
    document.getElementById("front-container").style.display = "none";
    const id = Number(document.getElementById("id").value);
    const update = document.getElementById("save-todo");
    update.textContent = "Update todo";
    update.setAttribute("onclick", `update_todo(${id})`);
});

load_todos();