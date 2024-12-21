from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST", "10.160.11.32"),
            user=os.getenv("DATABASE_USER", "todo_user"),
            password=os.getenv("DATABASE_PASSWORD", "password"),
            database=os.getenv("DATABASE_NAME", "tasks_db")
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    """Display the list of tasks."""
    connection = create_connection()
    tasks = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
        except Error as e:
            print(f"Error loading tasks: {e}")
        finally:
            connection.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task."""
    task_title = request.form.get('title')
    if task_title:
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (task_title,))
                connection.commit()
            except Error as e:
                print(f"Error saving task: {e}")
            finally:
                connection.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def mark_task_as_done(task_id):
    """Mark a task as completed."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
            connection.commit()
        except Error as e:
            print(f"Error updating task: {e}")
        finally:
            connection.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task."""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            connection.commit()
        except Error as e:
            print(f"Error deleting task: {e}")
        finally:
            connection.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
