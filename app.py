import os
import uuid

from flask import Flask, render_template, request, jsonify, send_from_directory
from utils import run_python_code, run_html_code

app = Flask(__name__)
SHARE_DIR = os.path.join(os.path.dirname(__file__), "shared_codes")
os.makedirs(SHARE_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/python-lab")
def python_lab():
    return render_template("python_lab.html")

@app.route("/html-lab")
def html_lab():
    return render_template("html_lab.html")

@app.route("/run/python", methods=["POST"])
def run_python():
    code = request.json.get("code", "")
    output = run_python_code(code)
    return jsonify({"output": output})

@app.route("/run/html", methods=["POST"])
def run_html():
    html_code = request.json.get("code", "")
    preview = run_html_code(html_code)
    return jsonify({"output": preview})


@app.route("/share/html", methods=["POST"])
def share_html():
    code = request.json.get("code", "")
    uid = uuid.uuid4().hex[:8]

    filepath = os.path.join(SHARE_DIR, f"{uid}.html")

    with open(filepath, "w") as f:
        f.write(code)

    return jsonify({"url": f"/shared/html/{uid}"})




@app.route("/shared/html/<code_id>")
def shared_html(code_id):
    path = os.path.join(SHARE_DIR, f"{code_id}.html")
    if not os.path.exists(path):
        return "⛔ Code not found", 404

    with open(path) as f:
        code = f.read()

    return render_template("shared_html.html", code=code)


@app.route("/share/python", methods=["POST"])
def share_code():
    data = request.get_json()
    code = data.get("code", "")
    code_id = str(uuid.uuid4())[:8]

    filepath = os.path.join(SHARE_DIR, f"{code_id}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    return jsonify({"code_id": code_id})


@app.route("/shared/python/<code_id>")
def view_shared_code(code_id):
    filepath = os.path.join(SHARE_DIR, f"{code_id}.py")
    if not os.path.exists(filepath):
        return "❌ This shared code does not exist!", 404

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    return render_template("python_lab.html", shared_code=code)


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == "__main__":
    app.run(debug=True)
