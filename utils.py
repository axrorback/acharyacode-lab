import subprocess
import uuid
import os


def run_python_code(code):
    try:
        filename = f"sandbox/{uuid.uuid4().hex}.py"
        with open(filename, "w") as f:
            f.write(code)

        result = subprocess.run(
            ["python3", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True
        )

        os.remove(filename)
        return result.stdout or result.stderr
    except subprocess.TimeoutExpired:
        return "⏱ Kod ishlashi juda uzoq davom etdi (timeout)"
    except Exception as e:
        return str(e)


def run_html_code(code):
    # Oddiy HTML preview return qiladi
    return code  # xavfsiz preview uchun frontda `iframe` ishlatamiz