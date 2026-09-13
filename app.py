
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pathlib import Path
import json
import os

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"

ADMIN_USER = "admin"
ADMIN_PASS = "AdminPammyza@475297"

def load_data():
    if not DATA_FILE.exists():
        return {"projects": []}
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

@app.route("/")
def home():
    data = load_data()
    return render_template("index.html", projects=data.get("projects", []))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("dashboard"))
        flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    return render_template("admin.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin"))

    data = load_data()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        image_url = request.form.get("image_url", "").strip()
        if title:
            data.setdefault("projects", []).append({
                "title": title,
                "description": description,
                "image_url": image_url
            })
            save_data(data)
            flash("เพิ่มผลงานเรียบร้อยแล้ว")
            return redirect(url_for("dashboard"))

    return render_template("dashboard.html", projects=data.get("projects", []))

@app.route("/delete/<int:index>", methods=["POST"])
def delete_project(index):
    if not session.get("admin"):
        return redirect(url_for("admin"))
    data = load_data()
    projects = data.get("projects", [])
    if 0 <= index < len(projects):
        projects.pop(index)
        save_data(data)
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
