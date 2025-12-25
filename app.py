import sqlite3
import os
from flask import Flask, request, redirect, render_template, send_from_directory

app = Flask(__name__)

# ---------------- DATABASE FUNCTIONS ----------------
def get_db_connection():
    conn = sqlite3.connect("spyvault.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Create files table
    c.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT
        )
    """)

    # Create chat table
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()

# Initialize database
init_db()

# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
def admin():
    conn = get_db_connection()
    
    # Fetch uploaded files
    files = conn.execute("SELECT * FROM files").fetchall()
    
    # Fetch chat messages
    chats = conn.execute("SELECT * FROM chat").fetchall()
    
    conn.close()
    
    return render_template("admin.html", files=files, chats=chats)

# ---------------- FILE DOWNLOAD ----------------
@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory("static/uploads", filename)

# ---------------- CALCULATOR (HOMEPAGE) ----------------
@app.route("/", methods=["GET", "POST"])
def calculator():
    display = ""

    if request.method == "POST":
        btn = request.form["btn"]
        display = request.form.get("display", "")

        if btn == "=":
            if display == "007":
                return redirect("/login")  # secret spy entry
            try:
                display = str(eval(display))  # normal calculation
            except:
                display = "Error"
        elif btn == "C":
            display = ""
        else:
            display += btn

    return render_template("calculator.html", display=display)

# ---------------- LOGIN PAGE ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        agent_name = request.form["agent_name"]
        agent_password = request.form["agent_password"]

        with open("agents.txt", "r") as file:
            for line in file:
                stored_name, stored_pass = line.strip().split(":")
                if agent_name == stored_name and agent_password == stored_pass:
                    return redirect("/vault")

        return "<h3>❌ ACCESS DENIED</h3>" + open("login.html").read()

    return render_template("login.html")

# ---------------- VAULT PAGE ----------------
import os
import sqlite3
from flask import Flask, request, redirect, render_template, render_template_string, flash

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/vault", methods=["GET", "POST"])
def vault():
    message = ""

    conn = sqlite3.connect("spyvault.db")
    c = conn.cursor()

    if request.method == "POST":
        action = request.form.get("action")

        # ---------------- CAESAR CIPHER ----------------
        if action == "caesar":
            text = request.form.get("caesar_text", "")
            shift = int(request.form.get("shift", 3))
            encrypted = ""
            for ch in text:
                if ch.isalpha():
                    base = ord('A') if ch.isupper() else ord('a')
                    encrypted += chr((ord(ch) - base + shift) % 26 + base)
                else:
                    encrypted += ch
            message = f"Encrypted Text: {encrypted}"

        # ---------------- MORSE CODE ----------------
        elif action == "morse":
            morse_dict = {
                'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
                'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
                'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
                'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                'Y': '-.--', 'Z': '--..',
                '1': '.----','2': '..---','3': '...--','4': '....-',
                '5': '.....','6': '-....','7': '--...','8': '---..',
                '9': '----.','0': '-----',' ': '/'
            }
            text = request.form.get("morse_text", "").upper()
            encrypted = " ".join(morse_dict.get(ch, '') for ch in text)
            message = f"Morse Code: {encrypted}"

        # ---------------- FILE UPLOAD ----------------
        elif action == "upload":
            if 'secret_file' in request.files:
                file = request.files['secret_file']
                if file.filename:
                    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                    file.save(file_path)
                    c.execute("INSERT INTO files (filename) VALUES (?)", (file.filename,))
                    conn.commit()
                    message = f"File '{file.filename}' uploaded successfully!"

        # ---------------- CHAT ----------------
        elif action == "chat":
            chat_msg = request.form.get("chat_msg", "")
            if chat_msg:
                c.execute("INSERT INTO chat (message) VALUES (?)", (chat_msg,))
                conn.commit()
                message = f"Message saved: {chat_msg}"

    conn.close()
    return render_template("vault.html", message=message)

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)






