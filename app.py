from flask import Flask, request, jsonify
import string, random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def generate_password(length, use_letters=True, use_digits=True, use_symbols=True):
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return "Error: No character set selected!"

    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/api', methods=['GET', 'POST'])
def generate():
    if request.method == 'GET':
        # return a helpful message if you test in browser
        return jsonify({"message": "Use POST to generate a password"})

    # POST request
    print("Received form data:", request.form.to_dict())
    password = None
    error = None
    try:
        length = int(request.form.get('length', 0))
        if length <= 0:
            error = "Password length must be a positive integer."
        else:
            use_letters = request.form.get('use_letters') is not None
            use_digits = request.form.get('use_digits') is not None
            use_symbols = request.form.get('use_symbols') is not None
            password = generate_password(length, use_letters, use_digits, use_symbols)
            if password.startswith("Error:"):
                error = password
                password = None
    except ValueError:
        error = "Invalid input for password length."
    return jsonify({'password': password, 'error': error})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000)
