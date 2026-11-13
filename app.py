from flask import Flask, request, render_template, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "employee-management-secret-key"

def get_db_connection():
    conn = sqlite3.connect("employees.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection()

    employees = conn.execute(
        "SELECT * FROM employees"
    ).fetchall()

    conn.close()

    return render_template("index.html", employees=employees)

@app.route("/search")
def search_employee():
    employee_id = request.args.get("employee_id", type=int)

    conn = get_db_connection()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    conn.close()

    if employee:
        return render_template("search.html", employee=employee)

    return "Employee not found"

@app.route("/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        employee_id = request.form.get("employee_id", "").strip()
        name = request.form.get("name", "").strip()
        department = request.form.get("department", "").strip()

        if not employee_id or not name or not department:
            flash("All fields are required!", "error")
            return redirect(url_for("add_employee"))

        if not employee_id.isdigit() or int(employee_id) <= 0:
            flash("Employee ID must be a positive number!", "error")
            return redirect(url_for("add_employee"))

        employee_id = int(employee_id)

        conn = get_db_connection()

        existing_employee = conn.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        ).fetchone()

        if existing_employee:
            conn.close()
            flash("Employee ID already exists!", "error")
            return redirect(url_for("add_employee"))

        conn.execute(
            "INSERT INTO employees (id, name, department) VALUES (?, ?, ?)",
            (employee_id, name, department)
        )

        conn.commit()
        conn.close()

        flash("Employee added successfully!", "success")
        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/update/<int:employee_id>", methods=["GET", "POST"])
def update_employee(employee_id):

    conn = get_db_connection()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    if employee:

        if request.method == "POST":

            new_department = request.form["department"]

            conn.execute(
                "UPDATE employees SET department = ? WHERE id = ?",
                (new_department, employee_id)
            )

            conn.commit()
            conn.close()

            flash("Employee updated successfully!", "success")
            return redirect(url_for("home"))

        conn.close()
        return render_template("update.html")

    conn.close()
    return "Employee not found"

@app.route("/delete/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):

    conn = get_db_connection()

    try:
        employee = conn.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        ).fetchone()

        if employee:
            conn.execute(
                "DELETE FROM employees WHERE id = ?",
                (employee_id,)
        )

            conn.commit()
            flash("Employee deleted successfully!", "success")
            return redirect(url_for("home"))

        flash("Employee not found!", "error")
        return redirect(url_for("home"))
    
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
