from Crypto.PublicKey import RSA

def generate_rsa_keypair():
    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open("attacker_private.pem", "wb") as priv:
        priv.write(private_key)

    with open("attacker_public.pem", "wb") as pub:
        pub.write(public_key)

    print("[+] RSA Key Pair generated.")
    print("[+] Private Key -> attacker_private.pem")
    print("[+] Public Key  -> attacker_public.pem")

if __name__ == "__main__":
    generate_rsa_keypair()

