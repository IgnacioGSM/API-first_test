const API_URL = "http://127.0.0.1:8000/tasks";

// Obtener tareas
async function fetchTasks() {
    const response = await fetch(API_URL);
    const tasks = await response.json();

    const container = document.getElementById("taskList");
    container.innerHTML = "";

    tasks.forEach(task => {
        const card = document.createElement("div");
        card.className = "task-card";

        const title = document.createElement("div");
        title.className = "task-title";
        title.textContent = task.title;

        const desc = document.createElement("div");
        desc.className = "task-desc";
        desc.textContent = task.description || "Sin descripción";

        // 🟢 Checkbox
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.completed;

        checkbox.onchange = () => toggleTask(task);

        const status = document.createElement("div");
        status.className = "task-status " + (task.completed ? "completed" : "pending");
        status.textContent = task.completed ? "Completada" : "Pendiente";

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "delete-btn";
        deleteBtn.textContent = "Eliminar";
        deleteBtn.onclick = () => deleteTask(task.id);

        card.appendChild(title);
        card.appendChild(desc);
        card.appendChild(checkbox);
        card.appendChild(status);
        card.appendChild(deleteBtn);

        container.appendChild(card);
    });
}

// Crear tarea
async function createTask() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    if (!title) return;

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title,
            description,
            completed: false
        })
    });

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

    fetchTasks();
}

// Eliminar tarea
async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    fetchTasks();
}

// PUT lo de la checkbox
async function toggleTask(task) {
    await fetch(`${API_URL}/${task.id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            completed: !task.completed
        })
    });

    fetchTasks();
}

// Cargar tareas al iniciar
fetchTasks();