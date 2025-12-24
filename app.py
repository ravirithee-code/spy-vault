from flask import Flask, request, redirect, render_template, render_template_string

app = Flask(__name__)

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
# ---------------- VAULT PAGE ----------------
@app.route("/vault", methods=["GET", "POST"])
def vault():
    message = ""

    if request.method == "POST":
        action = request.form.get("action")

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

    # Render vault page using Flask template and pass message
    return render_template("vault.html", message=message)

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

