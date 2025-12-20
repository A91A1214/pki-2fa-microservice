import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def decrypt_seed(encrypted_seed_b64: str, private_key_path: str) -> str:
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    seed_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # IMPORTANT FIX 👇
    seed_hex = seed_bytes.decode().strip()

    if len(seed_hex) != 64:
        raise ValueError(f"Decrypted seed length invalid: {len(seed_hex)}")

    return seed_hex
