const api_url = "http://127.0.0.1:8000";

async function load_todos(){
    const res = await fetch(`${api_url}/todos`);
    const todos = await res.json();
    const table = document.getElementById("todo-table");
    table.innerHTML = "";

    todos.forEach(todo=>{
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

async function add_todo(){
    const id = document.getElementById("id").value;
    const name = document.getElementById("name").value;
    const priority = document.getElementById("priority").value;
    const difficulty = document.getElementById("difficulty").value;
    const status = document.getElementById("status").value;

    const todo = {id: Number(id),name,priority,difficulty,status};

    await fetch(`${api_url}/todos`,{
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(todo)
    });
    load_todos();
}

async function delete_todo(id){
    await fetch(`${api_url}/todos/${id}`,{
        method: "DELETE"
    });
    load_todos();
}

load_todos();