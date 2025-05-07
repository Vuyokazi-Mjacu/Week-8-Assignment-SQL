from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

# MySQL connection
db = mysql.connector.connect(
    host="127.0.0.1",  
    user="root",  # or your MySQL username
    password="Vuyo290692!",  # your MySQL password
    database="TaskManager"
)
cursor = db.cursor(dictionary=True)

app = FastAPI()

# ---------------- Models ----------------
class User(BaseModel):
    name: str
    email: str

class Task(BaseModel):
    title: str
    description: str = ""
    status: str = "pending"
    user_id: int

# ---------------- Routes: USERS ----------------
@app.post("/users/")
def create_user(user: User):
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    val = (user.name, user.email)
    cursor.execute(sql, val)
    db.commit()
    return {"id": cursor.lastrowid, "message": "User created successfully"}

@app.get("/users/")
def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# ---------------- Routes: TASKS ----------------
@app.post("/tasks/")
def create_task(task: Task):
    sql = "INSERT INTO tasks (title, description, status, user_id) VALUES (%s, %s, %s, %s)"
    val = (task.title, task.description, task.status, task.user_id)
    cursor.execute(sql, val)
    db.commit()
    return {"id": cursor.lastrowid, "message": "Task created"}

@app.get("/tasks/")
def read_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    sql = "UPDATE tasks SET title=%s, description=%s, status=%s, user_id=%s WHERE id=%s"
    val = (task.title, task.description, task.status, task.user_id, task_id)
    cursor.execute(sql, val)
    db.commit()
    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    db.commit()
    return {"message": "Task deleted"}



