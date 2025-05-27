from app import create_app

if __name__ == "__main__":
    app = create_app("TEST_KEY")  # ✅ only pass the AES key (Base64 string)
    app.run(debug=True)
