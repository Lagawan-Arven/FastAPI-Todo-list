api_url = "http://127.0.0.1:8000";

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

document.getElementById("search-todo").addEventListener ("input",async function(){
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

async function add_todo(){
    const name = document.getElementById("name").value;
    const priority = document.getElementById("priority").value;
    const difficulty = document.getElementById("difficulty").value;
    const status = document.getElementById("status").value;

    todo = {name,priority,difficulty,status};

    await fetch(`${api_url}/todos`,{
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(todo)
    });
    load_todos();
}

async function update_todo(todo_id){
    const name = document.getElementById("name").value;
    const priority = document.getElementById("priority").value;
    const difficulty = document.getElementById("difficulty").value;
    const status = document.getElementById("status").value;

    todo = {name,priority,difficulty,status};

    await fetch(`${api_url}/todos/${todo_id}`,{
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(todo)
    });
    load_todos();   
}

async function delete_todo(todo_id){
    await fetch(`${api_url}/todos/${todo_id}`,{
        method: "DELETE"
    });
    load_todos();
}

load_todos();

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

