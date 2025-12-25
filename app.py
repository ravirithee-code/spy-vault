@app.route("/vault", methods=["GET", "POST"])
def vault():
    message = ""

    conn = get_db_connection()  # Use the helper function
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
